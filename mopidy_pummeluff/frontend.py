'''
Python module for Mopidy Pummeluff frontend.
'''

__all__ = (
    'PummeluffFrontend',
)

from threading import Event
from logging import getLogger

import pykka
from mopidy import core as mopidy_core

from .threads import GPIOHandler
from .action_handler import ActionHandler
from .actions.base import EmptyAction


LOGGER = getLogger(__name__)


class PummeluffFrontend(pykka.ThreadingActor, mopidy_core.CoreListener):
    '''
    Pummeluff frontend which basically reacts to GPIO button pushes and touches
    of RFID tags.
    '''

    def __init__(self, config, core):  # pylint: disable=unused-argument
        super().__init__()
        self.core           = core
        self.gpio_handler   = GPIOHandler(core=core)
        self.action_handler = ActionHandler(action_event=self.action_event)

    def action_event(self, action):
        '''
        Invoke the action that was stored in the registry.
        '''
        if not isinstance(action, EmptyAction):
            action(self.core)

    def on_start(self):
        '''
        Start GPIO handler & tag reader threads.
        '''
        self.gpio_handler.start()
        self.action_handler.start()

    def on_stop(self):
        '''
        Set threading stop event to tell GPIO handler & tag reader threads to
        stop their operations.
        '''
        self.gpio_handler.stop()
        self.action_handler.stop()
