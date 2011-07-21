#! /usr/bin/env python

'''Simple importer of loved tracks from last.fm to a Rdio playlist

This glue code by David Basden
'''

import json
import urllib
import sys
import logging
from playlistcreator import PlaylistCreator

logging.basicConfig(level=logging.ERROR)

PLAYLIST_NAME =		'Last Heard'
PLAYLIST_DESCRIPTION =	'Loved tracks from last.fm'

class LastFmLink(object):
	def __init__(self, apikey, apiurl='http://ws.audioscrobbler.com/2.0/'):
		self.apikey = apikey
		self.apiurl = apiurl
		assert self.apiurl[:7] == 'http://' or selfapiurl[:8] == 'https://'
	def api_call(self, method, **argd):
		'''do an API call to last.fm
		Uses the JSON format of the API, and then demarshals it into python objects
		'''
		req = [('method',method),('api_key',self.apikey)] + argd.items() + [('format','json')]
		f = urllib.urlopen(self.apiurl, data=urllib.urlencode(req))
		response = "".join(f.readlines())
		f.close()
		return json.loads(response)
	def get_loved_tracks(self, user, page=1, limit=50):
		'''yield 2tuples of loved tracks as (artist, title)
		Much more data is exposed by the API, but we don't use it
		'''
		page = 1
		while True:
			d = self.api_call('user.getlovedtracks', user=user, page=page, limit=limit)
			for track in d['lovedtracks']['track']:
				yield (track['artist']['name'], track['name'])

			if page == 1:
				totalPages = int(d['lovedtracks']['@attr']['totalPages'])
			if page >= totalPages:
				break
			page += 1

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print >> sys.stderr, sys.argv[0],'<lastfm username>'
		exit(1)
	username = sys.argv[1]

	lastfm = LastFmLink('1db991b8f9e0b37d79aea6191b4d5cc7')
	rdio = PlaylistCreator()
	if not rdio.authenticated:
		print "You need to authenticate to Rdio. Run ./authenticate.py then try again"
		sys.exit(1)

	print "Getting loved tracks for %s from last.fm" %(username,)
	tracks = list(lastfm.get_loved_tracks(username))
	print "Putting them into playlist '%s' on your Rdio account" % (PLAYLIST_NAME,)
	rdio.make_playlist(PLAYLIST_NAME, PLAYLIST_DESCRIPTION, tracks)
