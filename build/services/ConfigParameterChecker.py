import config.config as config



def checkDBParameters(DatabaseType: str):
    
    match DatabaseType:
        case "kafka":
            return __checkKafkaParameters__()
        case "minio":
            return __checkMinioParameters__()
        case "postgres":
            return __checkPostgreSQLParameters__()
        case "mysql":
            return __checkMySQLParameters__()
        case "mongodb":
            return __checkMongoDBParameters__()
        case "influx":
            return __checkInfluxDBParameters__()
        case _:
            config.logger.warn("DB not Compatible")
            return False
        
def __checkMongoDBParameters__():

    if config.MONGODB_URL == "":
        config.logger.warn("MongoDB connection configuration not present or incorrect")
        return False
    return True

def __checkPostgreSQLParameters__():
    if((config.POSTGRES_PASS == "") or (config.POSTGRES_PORT <= 0)):
        config.logger.warn("PostgreSQL connection configuration not present or incorrect")
        return False
    return True

def __checkMySQLParameters__():
    if((config.MYSQL_ROOT_PASS == "") or (config.MYSQL_PORT <= 0)):
        config.logger.warn("MySQL connection configuration not present or incorrect")
        return False
    return True

def __checkMinioParameters__():
    if((config.MINIO_PASS == "") or (config.MINIO_USERNAME == "") or (config.MINIO_PORT <= 0)):
        config.logger.warn("Minio connection configuration not present or incorrect")
        return False
    return True

def __checkKafkaParameters__():
    if((config.BOOTSTRAP_SERVERS == "") or (config.SCHEMA_URL == "")):
        config.logger.warn("Kafka connection configuration not present or incorrect")
        return False
    return True

def __checkInfluxDBParameters__():
    if((config.INFLUX_ORG == "") or (config.INFLUX_TOKEN == "") or (config.INFLUX_URL == "")):
        config.logger.warn("InfluxDB connection configuration not present or incorrect")
        return False
    return True
    