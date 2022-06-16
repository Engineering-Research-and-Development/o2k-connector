import cherrypy
from multiprocessing import Process
from services.Producer import Producer
from services.Subscription import Subscription
from services.Watcher import Watcher
from services.Api import Notification, cherrypy

def runWatcher():
    watcher = Watcher()
    watcher.run()

def exposeApi():
    cherrypy.quickstart(Notification())

def runInParallel(*fns):
  proc = []
  for fn in fns:
    p = Process(target=fn)
    p.start()
    proc.append(p)
  for p in proc:
    p.join()

if __name__ == '__main__':
    subscription = Subscription()
    subscription.createOrionSubscription()
    # Start watchdog on SUBSCRIPTION_JSON_FILENAME
    runInParallel(runWatcher, exposeApi)