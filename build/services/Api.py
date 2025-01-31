import cherrypy
import requests
import json
from config.config import O2K_HOST, O2K_PORT, KAFKA_TOPIC, FIWARE_SERVICE, FIWARE_SERVICEPATH, ENABLE_KEYCLOAK_AUTH, KEYCLOAK_URL
from config.config import logger
from services.Producer import KafkaProducer, MinioProducer, PostgreSQLProducer, InfluxDBProducer, MongoDBProducer
from services.ConfigParameterChecker import checkDBParameters
from services.IdentityManager import checkIDMParameters, KeycloakManager
import os


cherrypy.config.update({'server.socket_host': O2K_HOST})
cherrypy.config.update({'server.socket_port': O2K_PORT})

class Notification(object):

    def __init__(self):
        if checkDBParameters("kafka") == True:
            self.kafkaProducer = KafkaProducer()
        if checkDBParameters("minio") == True:
            self.minioProducer = MinioProducer()
        if checkDBParameters("postgres") == True:
            self.postgresProducer = PostgreSQLProducer()
        if checkDBParameters("influx") == True:
            self.influxProducer = InfluxDBProducer()
        if checkDBParameters("mongodb") == True:
            self.mongoDBProducer = MongoDBProducer()

        if ENABLE_KEYCLOAK_AUTH:
            if checkIDMParameters("keycloak") == True:
                self.keycloakManager = KeycloakManager()
        


    def _cp_dispatch(self, vpath):
        if len(vpath) == 2:
            if vpath[0] == "notify":
                if vpath[1] == "kafka":
                    return self.notifyKafka
                elif vpath[1] == "minio":
                    return self.notifyMinio
                elif vpath[1] == "postgres":
                    return self.notifyPostgres
                elif vpath[1] == "influx":
                    return self.notifyInflux
                elif vpath[1] == "mongo":
                    return self.notifyMongo
                elif vpath[1] == "keycloak":
                    return self.notifyMinioUsingKeycloak
            elif vpath[0] == "notifyld":
                if vpath[1] == "kafka":
                    return self.notifyldKafka
                elif vpath[1] == "minio":
                    return self.notifyldMinio
                elif vpath[1] == "postgres":
                    return self.notifyldPostgres
                elif vpath[1] == "influx":
                    return self.notifyldInflux
                elif vpath[1] == "mongo":
                    return self.notifyldMongo
                elif vpath[1] == "keycloak":
                    return self.notifyldMinioUsingKeycloak

        return self

    @cherrypy.expose
    @cherrypy.tools.json_out() 
    @cherrypy.tools.json_in()
    def notifyKafka(self, request):
        if checkDBParameters("kafka") == False:
            raise cherrypy.HTTPError(503, "kafka producer for NGSI-V2 not configured")
        logger.debug('V2 http notification for Kafka incoming')
        input_json = cherrypy.request.json

        service = str(FIWARE_SERVICE).lower()
        service_path = str(FIWARE_SERVICEPATH).replace('/', '').lower()

        for data in input_json['data']:

            entity = data['id'].lower()
            entity_type = data['type'].lower()

            ngsi_topic = KAFKA_TOPIC
            if KAFKA_TOPIC is None:
                # V2 Topic generation strategy
                ngsi_topic = service + "_" + service_path + "_" + entity + "_" + entity_type

            ngsi_message = data

            logger.debug("Producing data records to topic: " + str(ngsi_topic))
            logger.debug(ngsi_message)

            self.kafkaProducer.produce(topic=ngsi_topic, message=ngsi_message)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def notifyldKafka(self, request):
        if checkDBParameters("kafka") == False:
            raise cherrypy.HTTPError(503, "kafka producer for NGSI-LD not configured")
        logger.debug('LD http notification for Kafka incoming')
        input_json = cherrypy.request.json

        for data in input_json['data']:

            ngsi_topic = KAFKA_TOPIC
            if KAFKA_TOPIC is None:
                # LD Topic generation strategy
                ngsi_topic = data['id'].replace(':', '_').lower()

            ngsi_message = data

            logger.debug("Producing data records to topic: " + str(ngsi_topic))
            logger.debug(ngsi_message)

            self.kafkaProducer.produce(topic=ngsi_topic, message=ngsi_message)
    
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def notifyMinio(self, request):
        if checkDBParameters("minio") == False:
            raise cherrypy.HTTPError(503)
        logger.debug('V2 http notification for Minio incoming')

        headers = cherrypy.request.headers 
        input_json = cherrypy.request.json

        service = str(headers["fiware-service"]).lower()
        service_path = str(headers["fiware-servicepath"]).replace('/', '_').lower()

        #mappare i caratteri vietati da minio con underscore

        #for data in input_json['data']:

            #for attribute in data:
                #

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def notifyldMinio(self, request):
        if checkDBParameters("minio") == False:
            raise cherrypy.HTTPError(503)
        logger.debug('LD http notification for Minio incoming')

    
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def notifyPostgres(self, request):
        print(cherrypy.request.json)
        if checkDBParameters("postgres") == False:
            raise cherrypy.HTTPError(503, "postgress producer for NGSI-V2 not configured")
        logger.debug('V2 http notification for Postgres incoming')

        headers = cherrypy.request.headers 
        input_json = cherrypy.request.json

        service = str(headers["fiware-service"]).lower()
        service_path = str(headers["fiware-servicepath"]).replace('/', '_').lower()

        for data in input_json['data']:

            ngsi_message = data

            ngsi_message["id"] = ngsi_message["id"].replace("-","_").replace(":","_")

            logger.debug("Sending data to Postgres")
            logger.debug(ngsi_message) 
            
            self.postgresProducer.produce(ngsi_message, service, service_path)


    @cherrypy.expose
    @cherrypy.tools.json_in()
    def notifyldPostgres(self, request):
        if checkDBParameters("postgres") == False:
            raise cherrypy.HTTPError(503, "postgress producer for NGSI-LD not configured")
        logger.debug('LD http notification for Postgres incoming')

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def notifyInflux(self, request):
        if checkDBParameters("influx") == False:
            raise cherrypy.HTTPError(503, "influxDB producer for NGSI-V2 not configured")
        logger.debug('V2 http notification for InfluxDB incoming')

        input_json = cherrypy.request.json
        headers = cherrypy.request.headers 

        service = str(headers["fiware-service"]).lower()
        service_path = str(headers["fiware-servicepath"]).replace('/', '_').lower()

        for data in input_json['data']:

            ngsi_message = data

            ngsi_message["id"] = ngsi_message["id"].replace("-","_").replace(":","_")

            logger.debug("Sending data to Influx")
            logger.debug(ngsi_message) 

            self.influxProducer.produce(ngsi_message, service, service_path)

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def notifyldInflux(self, request):
        if checkDBParameters("influx") == False:
            raise cherrypy.HTTPError(503, "influxDB producer for NGSI-LD not configured")
        logger.debug('LD http notification for InfluxDB incoming')
    
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def notifyMongo(self, request):
        if checkDBParameters("mongodb") == False:
            raise cherrypy.HTTPError(503, "mongoDB producer for NGSI-V2 not configured")
        logger.debug('V2 http notification for Mongo incoming')

        input_json = cherrypy.request.json
        headers = cherrypy.request.headers 

        service = str(headers["fiware-service"]).lower()
        service_path = str(headers["fiware-servicepath"]).replace('/', '_').lower()

        for data in input_json['data']:

            ngsi_message = data

            ngsi_message["id"] = ngsi_message["id"].replace("-","_").replace(":","_")

            logger.debug("Sending data to Mongo")
            logger.debug(ngsi_message) 

            self.mongoDBProducer.produce(ngsi_message, service, service_path)
        
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def notifyldMongo(self, request):
        if checkDBParameters("mongodb") == False:
            raise cherrypy.HTTPError(503, "mongoDB producer for NGSI-LD not configured")
        logger.debug('LD http notification for Mongo incoming')
    
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def notifyMinioUsingKeycloak(self, request):
        if checkIDMParameters("keycloak") == False:
            raise cherrypy.HTTPError(503, "keycloak manager for NGSI-V2 not configured")

        input_json = cherrypy.request.json
        headers = cherrypy.request.headers 
        access_token = self.keycloakManager.getAccessToken()
        
        service = str(headers["fiware-service"]).lower()
        service_path = str(headers["fiware-servicepath"]).replace('/', '_').lower()
        service_path = service_path[1:]
        

        for data in input_json['data']:

            body = {
                "name": data["name"]["value"] + "." + data["FileType"]["value"], 
                "tags": [service, service_path]
            }
            body = json.dumps(body)
            upl_url = KEYCLOAK_URL + "api/v1/files/upload-url"
            response = requests.post(url=upl_url, headers={'Authorization': f"Bearer {access_token}"}, data=body)
            response_json = response.json()

            files = {
                'key': (None, response_json["s3"]["fields"]["key"]),
                'policy': (None, response_json["s3"]["fields"]["policy"]),
                'x-amz-algorithm': (None, response_json["s3"]["fields"]["x-amz-algorithm"]),
                'x-amz-credential': (None, response_json["s3"]["fields"]["x-amz-credential"]),
                'x-amz-date': (None, response_json["s3"]["fields"]["x-amz-date"]),
                'x-amz-signature': (None, response_json["s3"]["fields"]["x-amz-signature"]),
                'file': open(data["FileLocation"]["value"], 'rb'),
            }

            response = requests.post(response_json["s3"]["url"], files=files)

            ack_url = KEYCLOAK_URL + "api/v1/files/{}/status".format(response_json["id"])
            
            response = requests.patch(url=ack_url, headers={'Authorization': f"Bearer {access_token}"})

        
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def notifyldMinioUsingKeycloak(self, request):
        if checkIDMParameters("keycloak") == False:
            raise cherrypy.HTTPError(503, "keycloak manager for NGSI-LD not configured")