from functools import cache
from config.config import ORION_HOST, ORION_PORT, FIWARE_SERVICE, FIWARE_SERVICEPATH, \
    SUBSCRIPTION_JSON_PATH, SUBSCRIPTION_JSON_FILENAME, subscriptionsIds
import requests
from config.config import logger
from services.Validator import Validator

class Subscription:
    def createOrionSubscription(self):
        if len(subscriptionsIds) > 0:
            logger.error('Cannot create a new subscription, already exists: ' + str(subscriptionsIds))
            return
        validator = Validator()
        url = 'http://{0}:{1}/v2/subscriptions'.format(ORION_HOST, ORION_PORT)
        headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json', \
            'Fiware-Service': FIWARE_SERVICE, 'Fiware-ServicePath': FIWARE_SERVICEPATH}
        jsonSubscription = open(SUBSCRIPTION_JSON_PATH + '/' + SUBSCRIPTION_JSON_FILENAME, 'r').read()
        isValid = validator.validateOrionSubscriptionJSON(jsonSubscription)
        if isValid:
            r = requests.post(url, data=jsonSubscription, headers=headers)
            if(r.status_code == 201):
                subscriptionId = str(r.headers["location"].split("/")[3])
                logger.info('Subscription success with id: ' + subscriptionId)
                subscriptionsIds.append(subscriptionId)
                logger.info('Saved subscription in cache: ' + str(subscriptionsIds))
            else:
                logger.error('Subscription failed ' + str(r))
        else:
            logger.error('Invalid schema for ' + SUBSCRIPTION_JSON_FILENAME)
    
    def updateOrionSubscription(self):
        if subscriptionsIds is None or len(subscriptionsIds) <= 0:
            logger.error('Cannot update subscription, create a new one first.')
            return
        subscriptionId = subscriptionsIds[0]
        validator = Validator()
        url = 'http://{0}:{1}/v2/subscriptions/{2}'.format(ORION_HOST, ORION_PORT, subscriptionId)
        headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json', 'Fiware-Service': FIWARE_SERVICE, 'Fiware-ServicePath': FIWARE_SERVICEPATH}
        jsonSubscription = open(SUBSCRIPTION_JSON_PATH + '/' + SUBSCRIPTION_JSON_FILENAME, 'r').read()
        isValid = validator.validateOrionSubscriptionJSON(jsonSubscription)
        if isValid:
            r = requests.post(url, data=jsonSubscription, headers=headers)
            if(r.status_code == 201):
                subscriptionId = str(r.headers["location"].split("/")[3])
                logger.info('Subscription success with id: ' + subscriptionId)
                subscriptionsIds[0] = subscriptionId
                logger.info('Saved subscription in cache: ' + str(subscriptionsIds))
            else:
                logger.error('Subscription failed ' + str(r))
        else:
            logger.error('Invalid schema for ' + SUBSCRIPTION_JSON_FILENAME)