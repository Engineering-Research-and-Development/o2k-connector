from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime, timedelta
from config.config import SUBSCRIPTION_JSON_PATH, ORION_VERSION
from config.config import logger


# Watcher workaround for Windows Docker not triggering file changes
# https://github.com/cosmtrek/air/issues/190

class EventHandler(FileSystemEventHandler):
    subscription = None

    def __init__(self, subscription):
        self.subscription = subscription
        self.last_modified = datetime.now()

    def on_modified(self, event):
        if datetime.now() - self.last_modified < timedelta(seconds=1):
            return
        else:
            self.last_modified = datetime.now()
            logger.debug(f'event type: {event.event_type}  path : {event.src_path}')
            if ORION_VERSION == 'V2':
                self.subscription.updateOrionSubscription()
            else:
                self.subscription.updateOrionLDSubscription()


class Watcher:
    def run(self, subscription):
        logger.debug('Starting Watchdog')
        logger.debug('Watching dir: ' + SUBSCRIPTION_JSON_PATH)
        event_handler = EventHandler(subscription)
        observer = Observer()
        observer.schedule(event_handler, SUBSCRIPTION_JSON_PATH, recursive=True)
        observer.start()
