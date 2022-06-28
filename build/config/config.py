"""Environment Variables and Logger Provider"""

import os 
import logging

# Environment Variables
LOG_LEVEL = os.getenv('LOG_LEVEL')
if LOG_LEVEL is None:
    print("LOG_LEVEL env is missing. Reverting back to default value.")
    LOG_LEVEL="INFO"

LOGS_PATH = os.getenv('LOGS_PATH')
if LOGS_PATH is None:
    print("LOGS_PATH env is missing. Reverting back to default value.")
    LOGS_PATH="../logs"

O2K_HOST = os.getenv('O2K_HOST')
if O2K_HOST is None:
    print("O2K_HOST env is missing. Reverting back to default value.")
    O2K_HOST="0.0.0.0"

O2K_PORT = os.getenv('O2K_PORT')
if O2K_PORT is None:
    print("O2K_PORT env is missing. Reverting back to default value.")
    O2K_PORT = 5050
else:
    try:
        O2K_PORT = int(O2K_PORT)
    except ValueError:
        print("O2K_PORT env could not be casted into Integer. Reverting back to default value.")
        O2K_PORT = 5050

SCHEMA_URL = os.getenv('SCHEMA_URL')
if SCHEMA_URL is None:
    print("SCHEMA_URL env is missing. Reverting back to default value.")
    SCHEMA_URL="http://schema-registry:8081"

BOOTSTRAP_SERVERS = os.getenv('BOOTSTRAP_SERVERS')
if BOOTSTRAP_SERVERS is None:
    print("BOOTSTRAP_SERVERS env is missing. Reverting back to default value.")
    BOOTSTRAP_SERVERS = "localhost:9092,localhost:9093,localhost:9094"

ORION_HOST = os.getenv('ORION_HOST')
if ORION_HOST is None:
    print("ORION_HOST env is missing. Reverting back to default value.")
    ORION_HOST="localhost"

ORION_PORT = os.getenv('ORION_PORT')
if ORION_PORT is None:
    print("ORION_PORT env is missing. Reverting back to default value.")
    ORION_PORT = 1026
else:
    try:
        ORION_PORT = int(ORION_PORT)
    except ValueError:
        print("ORION_PORT env could not be casted into Integer. Reverting back to default value.")
        ORION_PORT = 1026

FIWARE_SERVICE = os.getenv('FIWARE_SERVICE')
if FIWARE_SERVICE is None:
    print("FIWARE_SERVICE env is missing. Reverting back to default value.")
    FIWARE_SERVICE="opcua_car"

FIWARE_SERVICEPATH = os.getenv('FIWARE_SERVICEPATH')
if FIWARE_SERVICEPATH is None:
    print("FIWARE_SERVICEPATH env is missing. Reverting back to default value.")
    FIWARE_SERVICEPATH="/demo"

SUBSCRIPTION_JSON_PATH = os.getenv('SUBSCRIPTION_JSON_PATH')
if SUBSCRIPTION_JSON_PATH is None:
    print("SUBSCRIPTION_JSON_PATH env is missing. Reverting back to default value.")
    SUBSCRIPTION_JSON_PATH="../conf"

SUBSCRIPTION_JSON_FILENAME="subscription.json"

MULTIPLE_SUBSCRIPTIONS = os.getenv('MULTIPLE_SUBSCRIPTIONS')
if MULTIPLE_SUBSCRIPTIONS is None:
    print("MULTIPLE_SUBSCRIPTIONS env is missing. Reverting back to default value.")
    MULTIPLE_SUBSCRIPTIONS="false"

SUBSCRIPTION_SCHEMA_FILE_PATH = os.getenv('SUBSCRIPTION_SCHEMA_FILE_PATH')
if SUBSCRIPTION_SCHEMA_FILE_PATH is None:
    print("SUBSCRIPTION_SCHEMA_FILE_PATH env is missing. Reverting back to default value.")
    SUBSCRIPTION_SCHEMA_FILE_PATH="../conf/subscription.schema.json"

SUBSCRIPTION_SCHEMA_FILE_PATH_LD = os.getenv('SUBSCRIPTION_SCHEMA_FILE_PATH_LD')
if SUBSCRIPTION_SCHEMA_FILE_PATH_LD is None:
    print("SUBSCRIPTION_SCHEMA_FILE_PATH_LD env is missing. Reverting back to default value.")
    SUBSCRIPTION_SCHEMA_FILE_PATH_LD="../conf/subscription-ld.schema.json"

ORION_VERSION = os.getenv('ORION_VERSION')
if ORION_VERSION is None:
    print("ORION_VERSION env is missing. Reverting back to default value.")
    ORION_VERSION="V2"

# Logger
DEFAULT_LOG_FILENAME = "logs.log"

logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)
formatter = logging.Formatter('%(asctime)s | %(filename)s->%(funcName)s():%(lineno)s | %(levelname)s | %(message)s')

file_handler = logging.FileHandler(LOGS_PATH + "/" + DEFAULT_LOG_FILENAME)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)