import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime, timedelta
from config.config import SUBSCRIPTION_JSON_PATH, SUBSCRIPTION_JSON_FILENAME
from config.config import logger
from services.Subscription import Subscription

# Watcher workaround for Windows Docker not triggering file changes
# https://github.com/cosmtrek/air/issues/190

subscription = Subscription()

class EventHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_modified = datetime.now()

    def on_modified(self, event):
        if datetime.now() - self.last_modified < timedelta(seconds=1):
            return
        else:
            self.last_modified = datetime.now()
            logger.info(f'event type: {event.event_type}  path : {event.src_path}')
            if SUBSCRIPTION_JSON_FILENAME in event.src_path:
                subscription.createOrionSubscription()

class Watcher:
    def run(self):
        logger.info('Starting Watchdog')
        logger.info('Watching dir: ' + SUBSCRIPTION_JSON_PATH + '/' + SUBSCRIPTION_JSON_FILENAME)
        event_handler = EventHandler()
        observer = Observer()
        observer.schedule(event_handler, SUBSCRIPTION_JSON_PATH, recursive=True)
        observer.start()
