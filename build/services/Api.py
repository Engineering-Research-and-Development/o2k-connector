import cherrypy
from config.config import O2K_HOST, O2K_PORT, KAFKA_TOPIC
from config.config import logger
from services.Producer import Producer

cherrypy.config.update({'server.socket_host': O2K_HOST})
cherrypy.config.update({'server.socket_port': O2K_PORT})

producer = Producer()

class Notification(object):

  @cherrypy.expose
  @cherrypy.tools.json_out()
  @cherrypy.tools.json_in()
  def notify(self):
    input_json = cherrypy.request.json
    input_headers = cherrypy.request.headers

    service = input_headers['Fiware-Service'].lower()
    service_path = input_headers['Fiware-Servicepath'].replace('/','').lower()

    for data in input_json['data']:
        
        entity = data['id'].lower()
        entity_type = data['type'].lower()

        ngsi_topic = KAFKA_TOPIC
        if KAFKA_TOPIC is None :
          # V2 Topic generation strategy
          ngsi_topic = service + "_" + service_path + "_" + entity + "_" + entity_type

        ngsi_message = data

        logger.info("Producing data records to topic: " + str(ngsi_topic))
        logger.info(ngsi_message)

        producer.produce(topic=ngsi_topic, message=ngsi_message)
  
  @cherrypy.expose
  @cherrypy.tools.json_out()
  @cherrypy.tools.json_in()
  def notifyld(self):
    input_json = cherrypy.request.json

    for data in input_json['data']:
        
        subscriptionId = data['subscriptionId'].replace(':','_').lower()

        # LD Topic generation strategy
        ngsi_topic = subscriptionId
        ngsi_message = data

        logger.info("Producing data records to topic: " + str(ngsi_topic))
        logger.info(ngsi_message)

        producer.produce(topic=ngsi_topic, message=ngsi_message)