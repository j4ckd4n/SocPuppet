from Plugins import Plugin

import requests, requests_cache
import yaml

from datetime import timedelta

class BlockListDELookup(Plugin.Plugin):
  def __init__(self, ip: str = None, name: str = 'BlockListDELookup'):
    super().__init__(name)
    self._ip = ip
    self._url = "https://lists.blocklist.de/lists/all.txt"

  def _performLookup(self, value) -> dict:
    output = []
    requests_cache.install_cache("request_cache", expire_after=timedelta(hours=1))
    res = requests.get(self._url)

    if res.status_code != 200:
      return {
        value: {
          "err": res.content
        }
      }
    
    results = res.content.decode(encoding='utf-8').split('\n')
    if value in results:
      return {
        value: "Found in BlockListDE!"
      }
    
    return {
      value: "Address is not part of the BlockListDE listing."
    }

  def run(self):
    if self._ip == None:
      self._ip = input('Enter IP to lookup: ').strip()

    lookup = self._performLookup(self._ip)
    print(yaml.dump(lookup))