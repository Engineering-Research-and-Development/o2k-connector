"""Environment Variables and Logger Provider"""

import os
import logging
import sys

# Environment Variables
LOG_LEVEL = os.getenv('LOG_LEVEL')
if LOG_LEVEL is None:
    print("LOG_LEVEL env is missing. Reverting back to default value.")
    LOG_LEVEL = "INFO"

LOGS_PATH = os.getenv('LOGS_PATH')
if LOGS_PATH is None:
    print("LOGS_PATH env is missing. Reverting back to default value.")
    LOGS_PATH = "../logs"

O2K_HOST = os.getenv('O2K_HOST')
if O2K_HOST is None:
    print("O2K_HOST env is missing. Reverting back to default value.")
    O2K_HOST = "0.0.0.0"

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
if SCHEMA_URL == "":
    print("SCHEMA_URL env is missing.")

BOOTSTRAP_SERVERS = os.getenv('BOOTSTRAP_SERVERS')
if BOOTSTRAP_SERVERS == "":
    print("BOOTSTRAP_SERVERS env is missing.")

KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')
if KAFKA_TOPIC is None:
    print("KAFKA_TOPIC env is missing. Reverting back to default kafka topic generation procedure.")

ORION_HOST = os.getenv('ORION_HOST')
if ORION_HOST is None:
    print("ORION_HOST env is missing. Reverting back to default value.")
    ORION_HOST = "localhost"

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
    FIWARE_SERVICE = "opcua_car"

FIWARE_SERVICEPATH = os.getenv('FIWARE_SERVICEPATH')
if FIWARE_SERVICEPATH is None:
    print("FIWARE_SERVICEPATH env is missing. Reverting back to default value.")
    FIWARE_SERVICEPATH = "/demo"

MQTT_HOST = os.getenv('MQTT_HOST')
if MQTT_HOST is None:
    print("MQTT_HOST env is missing. Reverting back to default value.")
    MQTT_HOST = "localhost"

MQTT_PORT = os.getenv('MQTT_PORT')
if MQTT_PORT is None:
    print("MQTT_PORT env is missing. Reverting back to default value.")
    MQTT_PORT = 1883
else:
    try:
        MQTT_PORT = int(MQTT_PORT)
    except ValueError:
        print("MQTT_PORT env could not be casted into Integer. Reverting back to default value.")
        MQTT_PORT = 1883

MQTT_TOPIC = os.getenv('MQTT_TOPIC')
if MQTT_TOPIC is None:
    print("MQTT_TOPIC env is missing. Reverting back to default mqtt topic generation procedure.")

SUBSCRIPTION_JSON_PATH = os.getenv('SUBSCRIPTION_JSON_PATH')
if SUBSCRIPTION_JSON_PATH is None:
    print("SUBSCRIPTION_JSON_PATH env is missing. Reverting back to default value.")
    SUBSCRIPTION_JSON_PATH = "../conf"

SUBSCRIPTION_JSON_FILENAME = os.getenv('SUBSCRIPTION_JSON_FILENAME')
if SUBSCRIPTION_JSON_FILENAME is None:
    print("SUBSCRIPTION_JSON_FILENAME env is missing. Reverting back to default value.")
    SUBSCRIPTION_JSON_FILENAME = "subscription.json"

SUBSCRIPTION_JSON_FILENAME_LD = os.getenv('SUBSCRIPTION_JSON_FILENAME_LD')
if SUBSCRIPTION_JSON_FILENAME_LD is None:
    print("SUBSCRIPTION_JSON_FILENAME_LD env is missing. Reverting back to default value.")
    SUBSCRIPTION_JSON_FILENAME_LD = "subscription-ld.json"

SUBSCRIPTION_JSON_FILENAME_MQTT = os.getenv('SUBSCRIPTION_JSON_FILENAME_MQTT')
if SUBSCRIPTION_JSON_FILENAME_MQTT is None:
    print("SUBSCRIPTION_JSON_FILENAME_MQTT env is missing. Reverting back to default value.")
    SUBSCRIPTION_JSON_FILENAME_MQTT = "subscription-mqtt.json"

SUBSCRIPTION_JSON_FILENAME_MQTT_LD = os.getenv('SUBSCRIPTION_JSON_FILENAME_MQTT_LD')
if SUBSCRIPTION_JSON_FILENAME_MQTT_LD is None:
    print("SUBSCRIPTION_JSON_FILENAME_MQTT_LD env is missing. Reverting back to default value.")
    SUBSCRIPTION_JSON_FILENAME_MQTT_LD = "subscription-mqtt-ld.json"

MULTIPLE_SUBSCRIPTIONS = os.getenv('MULTIPLE_SUBSCRIPTIONS')
if MULTIPLE_SUBSCRIPTIONS is None:
    print("MULTIPLE_SUBSCRIPTIONS env is missing. Reverting back to default value.")
    MULTIPLE_SUBSCRIPTIONS = "false"

FLATTEN = os.getenv('FLATTEN')
if FLATTEN is None:
    print("FLATTEN env is missing. Reverting back to default value.")
    FLATTEN = "false"

SUBSCRIPTION_SCHEMA_FILE_PATH = os.getenv('SUBSCRIPTION_SCHEMA_FILE_PATH')
if SUBSCRIPTION_SCHEMA_FILE_PATH is None:
    print("SUBSCRIPTION_SCHEMA_FILE_PATH env is missing. Reverting back to default value.")
    SUBSCRIPTION_SCHEMA_FILE_PATH = "../conf/subscription.schema.json"

SUBSCRIPTION_SCHEMA_FILE_PATH_LD = os.getenv('SUBSCRIPTION_SCHEMA_FILE_PATH_LD')
if SUBSCRIPTION_SCHEMA_FILE_PATH_LD is None:
    print("SUBSCRIPTION_SCHEMA_FILE_PATH_LD env is missing. Reverting back to default value.")
    SUBSCRIPTION_SCHEMA_FILE_PATH_LD = "../conf/subscription-ld.schema.json"

SUBSCRIPTION_SCHEMA_FILE_PATH_MQTT = os.getenv('SUBSCRIPTION_SCHEMA_FILE_PATH_MQTT')
if SUBSCRIPTION_SCHEMA_FILE_PATH_MQTT is None:
    print("SUBSCRIPTION_SCHEMA_FILE_PATH_MQTT env is missing. Reverting back to default value.")
    SUBSCRIPTION_SCHEMA_FILE_PATH_MQTT = "../conf/subscription-mqtt.schema.json"

ORION_VERSION = os.getenv('ORION_VERSION')
if ORION_VERSION is None:
    print("ORION_VERSION env is missing. Reverting back to default value.")
    ORION_VERSION = "V2"

ORION_SUBSCRIPTION = os.getenv('ORION_SUBSCRIPTION')
if ORION_SUBSCRIPTION is None:
    print("ORION_SUBSCRIPTION env is missing. Reverting back to default value.")
    ORION_SUBSCRIPTION = "http"

KAFKA_ENABLE_SSL = os.getenv('KAFKA_ENABLE_SSL')
if KAFKA_ENABLE_SSL is None:
    print("KAFKA_ENABLE_SSL env is missing. Reverting back to default value.")
    KAFKA_ENABLE_SSL = False

KAFKA_SSL_CA = os.getenv('KAFKA_SSL_CA')
if KAFKA_SSL_CA is None:
    print("KAFKA_SSL_CA env is missing. Reverting back to default value.")
    KAFKA_SSL_CA = "/o2k-connector/Certificates/CARoot.pem"

KAFKA_SSL_KEY = os.getenv('KAFKA_SSL_KEY')
if KAFKA_SSL_KEY is None:
    print("KAFKA_SSL_KEY env is missing. Reverting back to default value.")
    KAFKA_SSL_KEY = "/o2k-connector/Certificates/key.pem"

KAFKA_SSL_CERTIFICATE = os.getenv('KAFKA_SSL_CERTIFICATE')
if KAFKA_SSL_CERTIFICATE is None:
    print("KAFKA_SSL_CERTIFICATE env is missing. Reverting back to default value.")
    KAFKA_SSL_CERTIFICATE = "/o2k-connector/Certificates/certificate.pem"

#PostgreSQL Configuration

POSTGRES_HOSTNAME = os.getenv('POSTGRES_HOSTNAME')
if POSTGRES_HOSTNAME == "":
    print("POSTGRES_HOSTNAME env is missing. Reverting back to default value.")
    POSTGRES_HOSTNAME = "localhost"

POSTGRES_PORT = os.getenv('POSTGRES_PORT')
if POSTGRES_PORT == "":
    print("POSTGRES_PORT env is missing. Reverting back to default value.")
    POSTGRES_PORT = 5432
else:
    try:
        POSTGRES_PORT = int(POSTGRES_PORT)
    except ValueError:
        print("POSTGRES_PORT env could not be casted into Integer. Reverting back to default value.")
        POSTGRES_PORT = 5432

POSTGRES_USERNAME = os.getenv('POSTGRES_USERNAME')
if POSTGRES_USERNAME == "":
    print("POSTGRES_USERNAME env is missing. Reverting back to default value.")
    POSTGRES_USERNAME = "postgres"

POSTGRES_PASS = os.getenv('POSTGRES_PASS')
if POSTGRES_PASS == "":
    print("POSTGRES_PASS env is missing.")

#MongoDB Configuration

MONGODB_URL = os.getenv('MONGODB_URL')
if MONGODB_URL == "":
    print("MONGODB_URL env is missing.")

#Minio Configuration

MINIO_HOSTNAME = os.getenv('MINIO_HOSTNAME')
if MINIO_HOSTNAME == "":
    print("MINIO_HOSTNAME env is missing. Reverting back to default value.")
    MINIO_HOSTNAME = "localhost"

MINIO_PORT = os.getenv('MINIO_PORT')
if MINIO_PORT == "":
    print("MINIO_PORT env is missing. Reverting back to default value.")
    MINIO_PORT = 9000
else:
    try:
        MINIO_PORT = int(MINIO_PORT)
    except ValueError:
        print("MINIO_PORT env could not be casted into Integer. Reverting back to default value.")
        MINIO_PORT = 9000

MINIO_USERNAME = os.getenv('MINIO_USERNAME')
if MINIO_USERNAME == "":
    print("MINIO_USERNAME env is missing.")

MINIO_PASS = os.getenv('MINIO_PASS')
if MINIO_PASS == "":
    print("MINIO_PASS env is missing.")

#MySQL Configuration

MYSQL_HOSTNAME = os.getenv('MYSQL_HOSTNAME')
if MYSQL_HOSTNAME == "":
    print("MYSQL_HOSTNAME env is missing. Reverting back to default value.")
    MYSQL_HOSTNAME = "localhost"

MYSQL_PORT = os.getenv('MYSQL_PORT')
if MYSQL_PORT == "":
    print("MYSQL_PORT env is missing. Reverting back to default value.")
    MYSQL_PORT = 3306
else:
    try:
        MYSQL_PORT = int(MYSQL_PORT)
    except ValueError:
        print("MYSQL_PORT env could not be casted into Integer. Reverting back to default value.")
        MYSQL_PORT = 3306

MYSQL_USERNAME = os.getenv('MYSQL_USERNAME')
if MYSQL_USERNAME == "":
    print("MYSQL_USERNAME env is missing")

MYSQL_ROOT_PASS = os.getenv('MYSQL_ROOT_PASS')
if MYSQL_ROOT_PASS == "":
    print("MYSQL_ROOT_PASS env is missing")

SKIP_AUTO_SUBSCRIPTION = os.getenv('SKIP_AUTO_SUBSCRIPTION')
if SKIP_AUTO_SUBSCRIPTION == "":
    print("SKIP_AUTO_SUBSCRIPTION env is missing. Reverting back to default value.")
    SKIP_AUTO_SUBSCRIPTION = False
else:
    try:
        SKIP_AUTO_SUBSCRIPTION = bool(SKIP_AUTO_SUBSCRIPTION)
    except ValueError:
        print("SKIP_AUTO_SUBSCRIPTION env could not be casted into Boolean. Reverting back to default value.")
        SKIP_AUTO_SUBSCRIPTION = False

# InfluxDB Configuration

INFLUX_URL = os.getenv('INFLUX_URL')
if INFLUX_URL == "":
    print("INFLUX_URL env is missing.")

INFLUX_ORG = os.getenv('INFLUX_ORG')
if INFLUX_ORG == "":
    print("INFLUX_ORG env is missing.")

INFLUX_TOKEN = os.getenv('INFLUX_TOKEN')
if INFLUX_TOKEN == "":
    print("INFLUX_TOKEN env is missing.")

# Keycloak Configuration

ENABLE_KEYCLOAK_AUTH = os.getenv('ENABLE_KEYCLOAK_AUTH')
if ENABLE_KEYCLOAK_AUTH == "":
    print("ENABLE_KEYCLOAK_AUTH env is missing. Reverting back to default value.")
    ENABLE_KEYCLOAK_AUTH = False
else:
    try:
        ENABLE_KEYCLOAK_AUTH = bool(ENABLE_KEYCLOAK_AUTH)
    except ValueError:
        print("ENABLE_KEYCLOAK_AUTH env could not be casted into Boolean. Reverting back to default value.")
        ENABLE_KEYCLOAK_AUTH = False

KEYCLOAK_GRANT_TYPE = os.getenv('KEYCLOAK_GRANT_TYPE')
if KEYCLOAK_GRANT_TYPE == "":
    print("KEYCLOAK_GRANT_TYPE env is missing. Reverting back to default value.")
    KEYCLOAK_GRANT_TYPE = "client_credentials"

KEYCLOAK_URL = os.getenv('KEYCLOAK_URL')
if KEYCLOAK_URL == "":
    print("KEYCLOAK_URL env is missing.")

KEYCLOAK_CLIENT_ID = os.getenv('KEYCLOAK_CLIENT_ID')
if KEYCLOAK_CLIENT_ID == "":
    print("KEYCLOAK_CLIENT_ID env is missing.")

KEYCLOAK_REALM = os.getenv('KEYCLOAK_REALM')
if KEYCLOAK_REALM == "":
    print("KEYCLOAK_REALM env is missing.")

KEYCLOAK_USERNAME = os.getenv('KEYCLOAK_USERNAME')
if KEYCLOAK_USERNAME == "":
    print("KEYCLOAK_USERNAME env is missing.")

KEYCLOAK_PASSWORD = os.getenv('KEYCLOAK_PASSWORD')
if KEYCLOAK_PASSWORD == "":
    print("KEYCLOAK_PASSWORD env is missing.")

KEYCLOAK_CLIENT_SECRET = os.getenv('KEYCLOAK_CLIENT_SECRET')
if KEYCLOAK_CLIENT_SECRET == "":
    print("KEYCLOAK_CLIENT_SECRET env is missing.")

# Logger
DEFAULT_LOG_FILENAME = "logs.log"

logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)
formatter = logging.Formatter('%(asctime)s | %(filename)s->%(funcName)s():%(lineno)s | %(levelname)s | %(message)s')

file_handler = logging.FileHandler(LOGS_PATH + "/" + DEFAULT_LOG_FILENAME)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(ch)
