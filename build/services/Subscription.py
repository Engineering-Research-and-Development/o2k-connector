import json
import copy
from config.config import ORION_HOST, ORION_PORT, FIWARE_SERVICE, FIWARE_SERVICEPATH, \
    SUBSCRIPTION_JSON_PATH, SUBSCRIPTION_JSON_FILENAME, SUBSCRIPTION_JSON_FILENAME_LD, MULTIPLE_SUBSCRIPTIONS
import requests
from config.config import logger
from services.Validator import Validator


class Subscription:
    subscriptionsIds = []

    def sendPATCHSubscriptionV2Request(self, url, data, headers, subscriptionId):
        r = requests.patch(url + '/' + subscriptionId, data=data, headers=headers)
        if r.status_code == 204:
            logger.info('Subscription updated with id: ' + subscriptionId)
        else:
            logger.error('Subscription failed ' + str(r.content))

    def sendPOSTSubscriptionV2Request(self, url, data, headers):
        r = requests.post(url, data=data, headers=headers)
        if r.status_code == 201:
            subscriptionId = str(r.headers["location"].split("/")[3])
            logger.info('Subscription success with id: ' + subscriptionId)
            self.subscriptionsIds.append(subscriptionId)
            logger.info('Saved subscription in cache: ' + str(self.subscriptionsIds))
        else:
            logger.error('Subscription failed ' + str(r.content))

    def splitAttrsForSubscription(self, jsonSubscription):
        jsonSubscriptions = []

        entities = jsonSubscription["subject"]["entities"]
        if len(entities) > 1:
            logger.error('Cannot create separate subscriptions with more than a single entity')
            return
        else:
            condition_attrs = jsonSubscription["subject"]["condition"]["attrs"]
            attrs = jsonSubscription["notification"]["attrs"]
            if len(condition_attrs) != len(attrs):
                logger.error('Attributes to subscribe do not match')
                return
            for attr in attrs:
                tempJsonSubscription = copy.deepcopy(dict(jsonSubscription))
                tempJsonSubscription["subject"]["condition"]["attrs"] = ["{0}".format(attr)]
                tempJsonSubscription["notification"]["attrs"] = ["{0}".format(attr)]
                jsonSubscriptions.append(tempJsonSubscription)
            return jsonSubscriptions

    # V2
    def createOrionSubscription(self):
        if len(self.subscriptionsIds) > 0:
            logger.error('Cannot create a new subscription, already exists: ' + str(self.subscriptionsIds))
            return
        validator = Validator()
        url = 'http://{0}:{1}/v2/subscriptions'.format(ORION_HOST, ORION_PORT)
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json',
                   'Fiware-Service': FIWARE_SERVICE, 'Fiware-ServicePath': FIWARE_SERVICEPATH}
        jsonSubscription = open(SUBSCRIPTION_JSON_PATH + '/' + SUBSCRIPTION_JSON_FILENAME, 'r').read()
        isValid = validator.validateOrionSubscriptionJSON(jsonSubscription)
        if isValid:
            if MULTIPLE_SUBSCRIPTIONS == "true":
                jsonSubscriptions = self.splitAttrsForSubscription(json.loads(jsonSubscription))
                for jsonSub in jsonSubscriptions:
                    self.sendPOSTSubscriptionV2Request(url, json.dumps(jsonSub), headers)
            else:
                self.sendPOSTSubscriptionV2Request(url, jsonSubscription, headers)
        else:
            logger.error('Invalid schema for ' + SUBSCRIPTION_JSON_FILENAME)

    def updateOrionSubscription(self):
        if self.subscriptionsIds is None or len(self.subscriptionsIds) <= 0:
            logger.error('Cannot update subscription, create a new one first.')
            return
        subscriptionId = self.subscriptionsIds[0]
        validator = Validator()
        url = 'http://{0}:{1}/v2/subscriptions'.format(ORION_HOST, ORION_PORT)
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Fiware-Service': FIWARE_SERVICE,
                   'Fiware-ServicePath': FIWARE_SERVICEPATH}
        jsonSubscription = open(SUBSCRIPTION_JSON_PATH + '/' + SUBSCRIPTION_JSON_FILENAME, 'r').read()
        isValid = validator.validateOrionSubscriptionJSON(jsonSubscription)
        if isValid:
            if MULTIPLE_SUBSCRIPTIONS == "true":
                jsonSubscriptions = self.splitAttrsForSubscription(json.loads(jsonSubscription))
                for index, jsonSub in enumerate(jsonSubscriptions):
                    self.sendPATCHSubscriptionV2Request(url, json.dumps(jsonSub), headers, subscriptionId)
            else:
                self.sendPATCHSubscriptionV2Request(url, jsonSubscription, headers, subscriptionId)
        else:
            logger.error('Invalid schema for ' + SUBSCRIPTION_JSON_FILENAME)

    # LD
    def createOrionLDSubscription(self):
        if len(self.subscriptionsIds) > 0:
            logger.error('Cannot create a new subscription, already exists: ' + str(self.subscriptionsIds))
            return
        validator = Validator()
        url = 'http://{0}:{1}/ngsi-ld/v1/subscriptions'.format(ORION_HOST, ORION_PORT)
        headers = {'Accept': 'application/json', 'Content-Type': 'application/ld+json'}
        jsonSubscription = open(SUBSCRIPTION_JSON_PATH + '/' + SUBSCRIPTION_JSON_FILENAME_LD, 'r').read()
        isValid = validator.validateOrionSubscriptionJSON(jsonSubscription)
        if isValid:
            r = requests.post(url, data=jsonSubscription, headers=headers)
            if r.status_code == 201:
                subscriptionId = str(r.headers["location"].split("/")[-1])
                logger.info('Subscription success with id: ' + subscriptionId)
                self.subscriptionsIds.append(subscriptionId)
                logger.info('Saved subscription in cache: ' + str(self.subscriptionsIds))
            else:
                logger.error('Subscription failed ' + str(r.content))
        else:
            logger.error('Invalid schema for ' + SUBSCRIPTION_JSON_FILENAME_LD)

    def updateOrionLDSubscription(self):
        if self.subscriptionsIds is None or len(self.subscriptionsIds) <= 0:
            logger.error('Cannot update subscription, create a new one first.')
            return
        subscriptionId = self.subscriptionsIds[0]
        # Delete existing subscription request
        url = 'http://{0}:{1}/ngsi-ld/v1/subscriptions/{2}'.format(ORION_HOST, ORION_PORT, subscriptionId)
        headers = {'Accept': 'application/json'}
        r = requests.delete(url, headers=headers)
        if r.status_code == 204:
            logger.info('Subscription deleted with id: ' + subscriptionId)
            self.subscriptionsIds = []
            logger.info('Removed subscription from cache: ' + str(self.subscriptionsIds))
            # Create new subscription request
            self.createOrionLDSubscription()
        else:
            logger.error('Delete subscription failed ' + str(r.content))
