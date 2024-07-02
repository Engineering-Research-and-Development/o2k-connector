import config.config as config
import traceback
from config.config import logger
from keycloak.keycloak_openid import KeycloakOpenID

class KeycloakManager:
    
    def __init__(self):

        try:
            if config.KEYCLOAK_GRANT_TYPE == "client_credentials":
                self.keycloak_server = KeycloakOpenID(
                    server_url=config.KEYCLOAK_URL + "auth/",
                    realm_name=config.KEYCLOAK_REALM,
                    client_id=config.KEYCLOAK_CLIENT_ID,
                    client_secret_key=config.KEYCLOAK_CLIENT_SECRET,
                )
            else:
                self.keycloak_server = KeycloakOpenID(
                    server_url=config.KEYCLOAK_URL + "auth/",
                    realm_name=config.KEYCLOAK_REALM,
                    client_id=config.KEYCLOAK_CLIENT_ID
                )
            logger.info("Connected with keycloak")
        except Exception:
            logger.error(traceback.print_exc())

    def getAccessToken(self):
        if config.KEYCLOAK_GRANT_TYPE == "client_credentials":
            return self.keycloak_server.token(grant_type=config.KEYCLOAK_GRANT_TYPE).get("access_token", None)
        else:
            return self.keycloak_server.token(grant_type=config.KEYCLOAK_GRANT_TYPE, username=config.KEYCLOAK_USERNAME, password=config.KEYCLOAK_PASSWORD).get("access_token", None)

def checkIDMParameters(IDM: str):
    match IDM:
        case "keycloak":
            return __checkKeycloakParameters__()
        case _:
            config.logger.warn("IDM not Compatible")
            return False

def __checkKeycloakParameters__():

    if config.ENABLE_KEYCLOAK_AUTH == False:
        config.logger.warn("Keycloak authentication not Enabled")
        return False
    
    if ((config.KEYCLOAK_URL == "") or 
        (config.KEYCLOAK_CLIENT_ID == "") or 
        (config.KEYCLOAK_REALM == "") or 
        (config.KEYCLOAK_CLIENT_SECRET == "" and config.KEYCLOAK_GRANT_TYPE == "client_credentials") or
        ((config.KEYCLOAK_USERNAME == "" or config.KEYCLOAK_PASSWORD == "") and config.KEYCLOAK_GRANT_TYPE == "password")):

        config.logger.warn("Keycloak connection configuration not present or incorrect")
        return False
    return True