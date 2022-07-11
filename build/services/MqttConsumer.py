import paho.mqtt.client as mqtt
import json
from config.config import MQTT_HOST, MQTT_PORT, MQTT_TOPIC, KAFKA_TOPIC, FIWARE_SERVICE, FIWARE_SERVICEPATH, ORION_VERSION
from config.config import logger
from services.Producer import Producer

producer = Producer()


class MQTTConsumer:
    def __init__(self, message_format='json', schema=None):

        client = mqtt.Client()
        client.on_connect = self.on_connect

        if ORION_VERSION == "V2":
            client.on_message = self.on_message
        else:
            client.on_message = self.on_message_ld

        client.connect(MQTT_HOST, MQTT_PORT, 60)
        logger.debug('Connected to mqtt instance at host:' + str(MQTT_HOST) + ", port: " + str(MQTT_PORT) )
        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        client.loop_forever()

    # The callback for when the client receives a CONNACK response from the server.

    def on_connect(self, client, userdata, flags, rc):
        logger.debug("Connected with result code "+str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(MQTT_TOPIC)
        logger.debug('mqtt subscription to topic: ' + MQTT_TOPIC)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        logger.debug('V2 mqtt notification incoming')
        service = str(FIWARE_SERVICE).lower()
        service_path = str(FIWARE_SERVICEPATH).replace('/', '').lower()

        for data in json.loads(msg.payload)['data']:

            entity = data['id'].lower()
            entity_type = data['type'].lower()

            ngsi_topic = KAFKA_TOPIC
            if KAFKA_TOPIC is None:
                # V2 Topic generation strategy
                ngsi_topic = service + "_" +  service_path + "_" + entity + "_" + entity_type

            ngsi_message = data

            logger.debug("Producing data records to topic: " + str(ngsi_topic))
            logger.info(ngsi_message)

            producer.produce(topic=ngsi_topic, message=ngsi_message)

    # The LD callback for when a PUBLISH message is received from the server.
    def on_message_ld(self, client, userdata, msg):
        logger.debug('LD mqtt notification incoming')

        for data in json.loads(msg.payload)['data']:

            ngsi_topic = KAFKA_TOPIC
            if KAFKA_TOPIC is None:
                # LD Topic generation strategy
                ngsi_topic = data['id'].replace(':', '_').lower()

            ngsi_message = data

            logger.debug("Producing data records to topic: " + str(ngsi_topic))
            logger.debug(ngsi_message)

            producer.produce(topic=ngsi_topic, message=ngsi_message)