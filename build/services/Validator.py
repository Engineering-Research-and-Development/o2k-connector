from config.config import logger
import json
import jsonschema
from jsonschema import validate
from config.config import ORION_VERSION, ORION_SUBSCRIPTION, SUBSCRIPTION_JSON_PATH, SUBSCRIPTION_SCHEMA_FILE_PATH, SUBSCRIPTION_SCHEMA_FILE_PATH_LD, SUBSCRIPTION_SCHEMA_FILE_PATH_MQTT

class Validator:
    def validateOrionSubscriptionJSON(self, jsonString):
        try:
            jsonData = json.loads(jsonString)
            jsonSchema = ""
            if ORION_SUBSCRIPTION == "mqtt":
                jsonSchema = json.loads(open(SUBSCRIPTION_JSON_PATH + '/' + SUBSCRIPTION_SCHEMA_FILE_PATH_MQTT, 'rb').read()) if ORION_VERSION=="V2" \
                    else json.loads(open(SUBSCRIPTION_JSON_PATH + '/' + SUBSCRIPTION_SCHEMA_FILE_PATH_LD, 'rb').read())
            else:
                jsonSchema = json.loads(open(SUBSCRIPTION_JSON_PATH + '/' + SUBSCRIPTION_SCHEMA_FILE_PATH, 'rb').read()) if ORION_VERSION=="V2" \
                    else json.loads(open(SUBSCRIPTION_JSON_PATH + '/' + SUBSCRIPTION_SCHEMA_FILE_PATH_LD, 'rb').read())

            validate(instance=jsonData, schema=jsonSchema)

        except jsonschema.exceptions.ValidationError as validationErr:
            logger.error(validationErr)
            return False
        except jsonschema.exceptions.SchemaError as schemaErr:
            logger.error(schemaErr)
            return False
        except Exception as err:
            logger.error(err)
            return False
        logger.debug("Valid subscription schema.")
        return True