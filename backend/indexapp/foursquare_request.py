from __future__ import absolute_import

import requests


class Foursquare_Req:

    def __init__(self, client_id, client_secret, version):
        self.c_id = client_id
        self.c_secret = client_secret
        self.c_version = version
        self.results = {}

    def veneus(self, query, near):
        prm = {'query': query,
                'near': near,
                'client_id': self.c_id,
                'client_secret': self.c_secret,
                'v': self.c_version
               }

        r = requests.get('https://api.foursquare.com/v2/venues/search', params=prm)
        self.results = r.json()  # take it as an json object
        return self.results

    def get_places(self):
        return self.results['response']['venues']

    def get_meta(self):  # to see if we are getting the unsuccessful data
        return self.results['meta']
