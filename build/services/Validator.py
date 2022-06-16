from config.config import logger
import json
import jsonschema
from jsonschema import validate
from config.config import SUBSCRIPTION_SCHEMA_FILE_PATH


class Validator:
    def validateOrionSubscriptionJSON(self, jsonString):
        try:
            jsonData = json.loads(jsonString)
            jsonSchema = json.loads(open(SUBSCRIPTION_SCHEMA_FILE_PATH, 'rb').read())
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
        logger.info("Valid subscription schema.")
        return True