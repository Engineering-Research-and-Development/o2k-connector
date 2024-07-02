import struct as _struct
from json import dumps
from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.error import SerializationError
import influxdb_client.domain
import influxdb_client.domain.bucket
import config.config as config 
from config.config import logger
from abc import ABC, abstractmethod
import psycopg2
import traceback
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import pymongo

class Serializer():
    def __init__(self, codec='utf_8'):
        self.codec = codec

    def __call__(self, obj, ctx):
        if obj is None:
            return None
        try:
            return dumps(obj).encode(self.codec)
        except _struct.error as e:
            raise SerializationError(str(e))

class AbstractProucer(ABC):

    @abstractmethod
    def produce(self, topic, message, key=1):
        pass

class KafkaProducer(AbstractProucer):
    def __init__(self, message_format='json', schema=None):

        if message_format == 'json':
            serializer = Serializer()

        elif message_format == 'avro':
            schema_str = schema

            schema_registry_conf = {'url': config.SCHEMA_URL}
            schema_registry_client = SchemaRegistryClient(schema_registry_conf)
            serializer = AvroSerializer(schema_registry_client, schema_str)

        producer_conf = {'bootstrap.servers': config.BOOTSTRAP_SERVERS,
                         'key.serializer': StringSerializer('utf_8'),
                         'value.serializer': serializer,
                         'queue.buffering.max.messages': 1000000}

        if config.KAFKA_ENABLE_SSL == True or config.KAFKA_ENABLE_SSL == 'true':
            producer_conf['security.protocol'] = 'SSL'
            producer_conf['ssl.ca.location'] = config.KAFKA_SSL_CA
            producer_conf['ssl.key.location'] = config.KAFKA_SSL_KEY
            producer_conf['ssl.certificate.location'] = config.KAFKA_SSL_CERTIFICATE

        self.producer = SerializingProducer(producer_conf)

    def delivery_report(self, err, msg):
        if err is not None:
            logger.error("Delivery failed for Machine record {}: {}".format(msg.key(), err))
        else:
            logger.debug('Order record {} successfully produced to {} [{}] at offset {}'.format(
                msg.key(), msg.topic(), msg.partition(), msg.offset()))

    def produce(self, topic, message, key=1):
        if type(message) == dict:
            df_dict = [message]
        else:
            df_dict = message.to_dict('records')

        for row in df_dict:
            if config.MULTIPLE_SUBSCRIPTIONS == "true" and config.FLATTEN == "true":
                flatten_row = {}
                flatten_row['id'] = row['id']
                flatten_row['type'] = row['type']

                keysList = list(row.keys())
                attr_names = [a for a in keysList if a not in ['id', 'type']]
                if len(attr_names) == 1:
                    flatten_row['attr_name'] = attr_names[0]
                    flatten_row['attr_data'] = row[attr_names[0]]
                row = flatten_row
            self.producer.poll(0.0)
            try:
                self.producer.produce(topic=topic, key=str(key), value=row, on_delivery=self.delivery_report)
                # self.producer.produce(topic=topic, key=str(key) , value=row)
            except KeyboardInterrupt:
                break

        self.producer.flush()

# GRETA
# Modulo: psycopg2
# Struttura: Database -> Schema -> Tabella
class PostgreSQLProducer(AbstractProucer):

    # quali sono le operazioni compiute da ogni metodo? Quali sono i dati in input?
    # i dati vengono inviati ai datastore dal metodo produce? 
    # dovremmo usare psycopg2?
    def __init__(self):

        try:
            self.client = psycopg2.connect(user=config.POSTGRES_USERNAME,
                                           password=config.POSTGRES_PASS,
                                           host=config.POSTGRES_HOSTNAME,
                                           port=config.POSTGRES_PORT)
            logger.info("Connected with postgres")
            self.client.autocommit = True
            
        except Exception:
            logger.error(traceback.print_exc())

    def produce(self, message, Tenant, servicePath):

        cursor = self.client.cursor()
        
        servicePath = servicePath[1:]

        tableName = servicePath + "_" + message["id"]

        CREATE_SHEMA_QUERY = "CREATE SCHEMA IF NOT EXISTS {};".format(Tenant)
        CREATE_TABLE_QUERY = "CREATE TABLE IF NOT EXISTS {}.{} (RECIVE_TIME TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP, ENTITY_ID TEXT, ENTITY_TYPE TEXT, ATTR_NAME TEXT, ATTR_TYPE TEXT, ATTR_VALUE TEXT);".format(Tenant, tableName)
        
        cursor.execute(CREATE_SHEMA_QUERY)
        cursor.execute(CREATE_TABLE_QUERY)
        
        entity_id = message.pop("id")
        entity_type = message.pop("type")

        for key in message:
            attribute = message[key]
            cursor.execute("""INSERT INTO {}.{} (ENTITY_ID, ENTITY_TYPE, ATTR_NAME, ATTR_TYPE, ATTR_VALUE) VALUES (%s, %s, %s, %s, %s);""".format(Tenant, tableName),(entity_id, entity_type, key, attribute["type"], str(attribute["value"]).replace("'",'"')))
        
        cursor.close()

    def delivery_report(self, err, msg):
        pass

# GRETA, MDT
# Modulo: pyMongo
# Struttura: Database -> Collection -> Document
class MongoDBProducer(AbstractProucer):

    # Instaturare connessione col database e tenerla attiva
    def __init__(self):
        try:
            self.client = pymongo.MongoClient(config.MONGODB_URL)
            logger.info("Connected with Mongo")
        except Exception:
            logger.error(traceback.print_exc())

    # Invio delle informazioni al database 
    def produce(self, message, Tenant, servicePath):
        
        database = self.client[Tenant]
        collection = database[servicePath + "_" + message.pop("id")]
        collection.insert_one(message)


# GRETA, MDT
# Modulo: minio
# Struttura: Server -> Bucket -> file
class MinioProducer(AbstractProucer):

    # 
    def __init__(self):
        #self.client = Minio("play.minio.io:9000", 
                        #    access_key="Q3AM3UQ867SPQQA43P2F",
                        #    secret_key="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",
                        #    region="my-region",
                        #)
        pass

    def produce(self, topic, message, key=1):
        #if not client.bucket_exists(decidere come chiamare i bucket):
        #    self.client.make_bucket(decidere come chiamare i bucket)
        #result = client.fput_object("my-bucket", "my-object", "my-filename",)
        #
        pass

# DT
# Modulo: MySQL Connector
# Struttura Database -> Tabella
class MySQLProducer(AbstractProucer):

    # 
    def __init__(self):
        pass

    def produce(self, topic, message, key=1):
        pass



# DT
# Modulo: influxdb-client
# Struttura: Organization(???)->Bucket(DB)->Measurement(Tabella)
class InfluxDBProducer(AbstractProucer):

     
    def __init__(self):
        try:
            self.client = influxdb_client.InfluxDBClient(url=config.INFLUX_URL, token=config.INFLUX_TOKEN, org=config.INFLUX_ORG)
            logger.info("Connected with Influx")
        except Exception:
            logger.error(traceback.print_exc())

    def produce(self, message, Tenant, servicePath):

        bucket_api = self.client.buckets_api()
        write_api = self.client.write_api(write_options=SYNCHRONOUS)

        servicePath = servicePath[1:]

        entity_id = message.pop("id")
        entity_type = message.pop("type")

        if bucket_api.find_bucket_by_name(Tenant) is None:
            bucket_api.create_bucket(bucket_name=Tenant, org_id=config.INFLUX_ORG)

        for key in message:
            attribute = message[key]
            value = attribute["value"]
            valueToInsert = ''
            if(isinstance(value, list)):
                for v in value:
                    if valueToInsert == '':
                        valueToInsert = valueToInsert + str(v)
                    else:
                        valueToInsert = valueToInsert + ", " + str(v)
            else:
                valueToInsert = value
            
            p = influxdb_client.Point(servicePath + "_" + entity_id).tag("Attr_type", attribute["type"]).field(key, valueToInsert)
            write_api.write(bucket=Tenant, org=config.INFLUX_ORG, record=p)