import struct as _struct
from json import dumps
from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.error import SerializationError
from config.config import SCHEMA_URL, BOOTSTRAP_SERVERS
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

        self.producer = SerializingProducer(producer_conf)

    def delivery_report(self, err, msg):
        if err is not None:
            logger.error("Delivery failed for Machine record {}: {}".format(msg.key(), err))
        else:
            logger.info('Order record {} successfully produced to {} [{}] at offset {}'.format(
                msg.key(), msg.topic(), msg.partition(), msg.offset()))

    def produce(self, topic, message, key=1):
        if type(message) == dict:
            df_dict = [message]
        else:
            df_dict = message.to_dict('records')

        for row in df_dict:
            self.producer.poll(0.0)
            try:
                self.producer.produce(topic=topic, key=str(key), value=row, on_delivery=self.delivery_report)
                # self.producer.produce(topic=topic, key=str(key) , value=row)
            except KeyboardInterrupt:
                break

        self.producer.flush()
