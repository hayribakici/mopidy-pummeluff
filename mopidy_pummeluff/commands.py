'''
CLI Interface of this extension.
'''

import logging
from threading import Event
from mopidy import commands
from .actions import ACTIONS
from .registry import REGISTRY
# from .actions.base import EmptyAction
# from .threads.tag_reader import MockTagReader
from .threads.tag_reader import TagReader


logger = logging.getLogger(__name__)


class PummeluffCommand(commands.Command):
    '''
    Main Command class.
    '''
    def __init__(self):
        super().__init__()
        self.add_child("list", ListCommand())
        self.add_child("actions", ActionsCommand())
        self.add_child("register", RegisterCommand())
        self.add_child("unregister", UnregisterCommand())

    def run(self, *args, **kwargs):
        pass


class ListCommand(commands.Command):
    '''
    Prints out the stored tags and their appropriate values on the terminal.
    '''
    def run(self, *args, **kwargs):
        '''
        Prints out the stored tags and values on the terminal.
        '''

        for tag in REGISTRY.values():
            logger.info("%s -> %s",tag, tag.as_dict())

        return 0

class ActionsCommand(commands.Command):
    '''
    Command for listing the available actions.
    '''
    def run(self, *args, **kwargs):
        '''
        Prints out the available actions on the terminal.
        '''
        logger.info(ACTIONS.keys())

class RegisterCommand(commands.Command):
    '''
    Command for registering a tag.
    '''

    def __init__(self):
        super().__init__()
        self.add_argument("--action",
            action="store",
            type=str,
            dest="action",
            required=True,
            default=None,
            help="The index of the action")
        self.add_argument("--alias",
            action="store",
            type=str,
            dest="alias",
            default=None,
            help="The alias of this tag")
        self.add_argument("--param",
            action="store",
            type=str,
            dest="param",
            default=None,
            help="The paramter value of this tag")
        self.action_class = ""
        self.alias = ""
        self.param = ""
        self.tag_reader = TagReader(self.success_event)

    def success_event(self, uid):
        REGISTRY.register(action_class=self.action_class,
            uid=uid,
            alias=self.alias,
            parameter=self.param)
        self.tag_reader.stop()
        

    def run(self, args, kwargs):
        '''
        Registering a tag.
        '''
        self.action_class = args.action
        self.alias = args.alias
        self.param = args.param
        self.tag_reader.start()


class UnregisterCommand(commands.Command):
    '''
    Command for unregistereing a tag.
    '''
    def __init__(self):
        super().__init__()
        self.add_argument("--uid",
            action="store",
            type=str,
            dest="uid",
            default=None,
            help="The uid to unregister")

    def run(self, args, kwargs):
        '''
        Unregistering a tag.
        '''
        REGISTRY.unregister(uid=args.uid)
