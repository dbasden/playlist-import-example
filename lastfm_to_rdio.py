#! /usr/bin/env python

'''Simple importer of loved tracks from last.fm to a Rdio playlist

This glue code written by David Basden
'''

import json
import urllib

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
		while True:
			d = self.api_call('user.getlovedtracks', user=user, page=page, limit=limit)
			for track in d['lovedtracks']['track']:
				yield (track['artist']['name'], track['name'])

			attr = d['lovedtracks']['@attr']
			if int(attr['page']) >= int(attr['totalPages']):
				break


if __name__ == "__main__":
	lastfm = LastFmLink('1db991b8f9e0b37d79aea6191b4d5cc7')
	for artist,title in lastfm.get_loved_tracks('notarealbear'):
		print title,'by',artist
	
