from services.Subscription import Subscription
from services.MqttConsumer import MQTTConsumer
from services.Watcher import Watcher
from services.Api import Notification, cherrypy
from config.config import ORION_VERSION, ORION_SUBSCRIPTION

if __name__ == '__main__':

    subscription = Subscription()
    if ORION_SUBSCRIPTION == 'mqtt':
        if ORION_VERSION == 'LD':
            subscription.createOrionMQTTLDSubscription()
        else:
            subscription.createOrionMQTTSubscription()
    else:
        if ORION_VERSION == 'LD':
            subscription.createOrionLDSubscription()
        else:
            subscription.createOrionSubscription()

    watcher = Watcher()
    watcher.run(subscription)

    if ORION_SUBSCRIPTION == 'mqtt':
        mqttConsumer = MQTTConsumer()
    else:
        cherrypy.quickstart(Notification())
