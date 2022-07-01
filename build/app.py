from services.Subscription import Subscription
from services.Watcher import Watcher
from services.Api import Notification, cherrypy
from config.config import ORION_VERSION

if __name__ == '__main__':

    subscription = Subscription()
    if ORION_VERSION == 'LD':
        subscription.createOrionLDSubscription()
    else:
        subscription.createOrionSubscription()

    watcher = Watcher()
    watcher.run(subscription)
    cherrypy.quickstart(Notification())
