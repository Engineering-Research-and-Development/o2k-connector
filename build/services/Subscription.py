from functools import cache
from config.config import ORION_HOST, ORION_PORT, FIWARE_SERVICE, FIWARE_SERVICEPATH, \
    SUBSCRIPTION_JSON_PATH, SUBSCRIPTION_JSON_FILENAME
import requests
from config.config import logger
from services.Validator import Validator
from services.Cache import Cache

class Subscription:
    def createOrionSubscription(self):
        validator = Validator()
        url = 'http://{0}:{1}/v2/subscriptions'.format(ORION_HOST, ORION_PORT)
        headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json', 'Fiware-Service': FIWARE_SERVICE, 'Fiware-ServicePath': FIWARE_SERVICEPATH}
        jsonSubscription = open(SUBSCRIPTION_JSON_PATH + '/' + SUBSCRIPTION_JSON_FILENAME, 'r').read()
        isValid = validator.validateOrionSubscriptionJSON(jsonSubscription)
        if isValid:
            r = requests.post(url, data=jsonSubscription, headers=headers)
            if(r.status_code == 201):
                subscriptionId = str(r.headers["location"].split("/")[3])
                logger.info('Subscription success with id: ' + subscriptionId)
                cache = Cache()
                cache.setSubscriptionId(subscriptionId)
                logger.info('Saved subscription in redis: ' + str(cache.getSubscriptionId()))
            else:
                logger.error('Subscription failed ' + str(r))
        else:
            logger.error('Invalid schema for ' + SUBSCRIPTION_JSON_FILENAME)