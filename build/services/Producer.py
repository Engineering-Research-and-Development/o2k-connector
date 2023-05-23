import struct as _struct
from json import dumps
from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.error import SerializationError
from config.config import SCHEMA_URL, BOOTSTRAP_SERVERS, MULTIPLE_SUBSCRIPTIONS, FLATTEN, KAFKA_ENABLE_SSL, KAFKA_SSL_CA, KAFKA_SSL_KEY, KAFKA_SSL_CERTIFICATE
from config.config import logger


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


class Producer:
    def __init__(self, message_format='json', schema=None):

        if message_format == 'json':
            serializer = Serializer()

        elif message_format == 'avro':
            schema_str = schema

            schema_registry_conf = {'url': SCHEMA_URL}
            schema_registry_client = SchemaRegistryClient(schema_registry_conf)
            serializer = AvroSerializer(schema_registry_client, schema_str)

        producer_conf = {'bootstrap.servers': BOOTSTRAP_SERVERS,
                         'key.serializer': StringSerializer('utf_8'),
                         'value.serializer': serializer,
                         'queue.buffering.max.messages': 1000000}

        if KAFKA_ENABLE_SSL == True or KAFKA_ENABLE_SSL == 'true':
            producer_conf['security.protocol'] = 'SSL'
            producer_conf['ssl.ca.location'] = KAFKA_SSL_CA
            producer_conf['ssl.key.location'] = KAFKA_SSL_KEY
            producer_conf['ssl.certificate.location'] = KAFKA_SSL_CERTIFICATE

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
            if MULTIPLE_SUBSCRIPTIONS == "true" and FLATTEN == "true":
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
