import cherrypy
from services.Subscription import Subscription
from services.Watcher import Watcher
from services.Api import Notification, cherrypy
from config.config import subscriptionsIds


if __name__ == '__main__':

  subscription = Subscription()
  subscription.createOrionSubscription()
  
  watcher = Watcher()
  watcher.run()
  cherrypy.quickstart(Notification())