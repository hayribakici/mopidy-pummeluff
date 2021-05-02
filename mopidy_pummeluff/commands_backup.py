'''
CLI Interface of this extension
'''

import logging
from threading import Event

from mopidy import commands

from .registry import REGISTRY
from .threads.tag_reader import TagReader


logger = logging.getLogger(__name__)



class PummeluffCommand(commands.Command):
    def __init__(self):
        super().__init__()
        self.add_child("register", RegisterCommand())
        # self.add_child("unregister", UnregisterCommand())
        self.add_child("list", ListCommand())

class RegisterCommand(commands.Command):
    help = "Registers an action. Usage register <action_class> <alias> <parameter>"

    def __init__(self):
        super().__init__()
        self.add_argument("action_class", action = 'store', type = int,
                            dest ="action_class", default = None, requred = True, nargs = 1)
        self.add_argument("alias", action = 'store',
                            dest ="alias", default = None, nargs = 1)
        self.add_argument("parameter", action = 'store',
                            dest ="parameter", default = None, nargs = 1)
        self.stop_event = Event()                            
        self.action_class = None
        self.alias = None
        self.parameter = None


    def success_event(self, action):
        '''
        Called when a card was successfully read.
        '''
        REGISTRY.register(action_class=self.action_class,
                        uid=action.uid, parameter=self.parameter)
        self.stop_event.set()


    def run(self, args, config):
        '''
        Runs.
        '''
        for arg in args:
                logger.info(f"{arg}")
        
        self.action_class = args.action_class
        self.alias = args.alias
        self.parameter = args.paramter

        tag_reader = TagReader(stop_event=self.stop_event, success_event=self.success_event)
        # Calling the tag reader synchronously. Blocks the UI until user gives card.
        tag_reader.run()
        return 0


class ListCommand(commands.Command):

    def run(self, args, config):
        '''
        Runs.
        '''

        for tag in REGISTRY.values():
            logger.info(f"{tag} -> {tag.as_dict()}")

        return 0
