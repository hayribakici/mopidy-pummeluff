'''
CLI Interface of this extension.
'''

import logging
from mopidy import commands
from .registry import REGISTRY
from .actions import ACTIONS


logger = logging.getLogger(__name__)


class PummeluffCommand(commands.Command):
    '''
    Main Command class.
    '''
    def __init__(self):
        super().__init__()
        self.add_child("list", ListCommand())
        self.add_child("actions", ActionsCommand())

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
        logger.info("\n".join([str(i) + ": " + action for i, action in enumerate(ACTIONS)]))
