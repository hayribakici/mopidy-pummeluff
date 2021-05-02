'''
Wrapper class around tag_reader.
'''
from threading import Event
from logging import getLogger
from time import time

from .registry import REGISTRY
from .actions.base import EmptyAction
from .threads.tag_reader import TagReader
from .sound import play_sound

LOGGER = getLogger(__name__)

class ActionHandler():

    def __init__(self, action_event):
        self.action_event = action_event
        self.stop_event = Event()
        self.tag_reader = TagReader(self.success_event)

    def success_event(self, uid):
        '''
        Handle the scanned tag / retreived UID.

        :param str uid: The UID
        '''
        try:
            action = REGISTRY[str(uid)]
            LOGGER.info('Triggering action of registered tag')
            play_sound('success.wav')

        except KeyError:
            LOGGER.info('Tag is not registered, thus doing nothing')
            play_sound('fail.wav')
            action = EmptyAction(uid=uid)

        action.scanned = time()
        TagReader.latest = action
        self.action_event(action)

    def start(self):
        self.tag_reader.start()

    def stop(self):
        self.tag_reader.stop()
