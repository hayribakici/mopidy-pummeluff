'''
Python module for Mopidy Pummeluff tracklist tag.
'''

__all__ = (
    'Latest',
)

from logging import getLogger

from .base import Action

LOGGER = getLogger(__name__)


class Latest(Action):
    '''
    Replaces the tracklist with the track that has been added last.
    '''

    @classmethod
    def execute(cls, core, uri):  # pylint: disable=arguments-differ
        '''
        Replace tracklist and play the latest.

        :param mopidy.core.Core core: The mopidy core instance
        :param str uri: An URI for the tracklist replacement
        '''
        LOGGER.info('Replacing tracklist with latest the URI "%s"', uri)

        playlists = [playlist.uri for playlist in core.playlists.as_list().get()]

        if uri in playlists:
            uris = [item.uri for item in core.playlists.get_items(uri).get()]
        else:
            uris = [uri]
            
        if len(uris) > 0:
           uris = [uris[-1]]
        
        core.tracklist.clear()
        core.tracklist.add(uris=uris)
        
        # tracks = core.tracklist.get_tracks().get()
        # for track in tracks:
        #    LOGGER.info("Name: %s, Date: %s", track.name, track.date)
        
        # for uri in uris[0::9]:
        LOGGER.info(uris)
        
        core.playback.play()
        
