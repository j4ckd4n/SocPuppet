from Plugins import Plugin

import requests, requests_cache
import yaml

from datetime import timedelta

class SSLAbuseIPLookup(Plugin.Plugin):
  def __init__(self, ip: str = None, name: str = 'SSLAbuseIPLookup'):
    super().__init__(name)
    self._ip = ip
    self._url = "https://sslbl.abuse.ch/blacklist/sslipblacklist.txt"

  def _performLookup(self, value) -> dict:
    requests_cache.install_cache("sslabuse_ip_cache", expire_after=timedelta(hours=1))
    res = requests.get(self._url)

    if res.status_code != 200:
      return {
        value: {
          "err": res.content
        }
      }
    
    results = res.content.decode(encoding='utf-8').split('\r\n')
    
    if value in results:
      return {
        value: "Found in SSLAbuse IP Blocklist."
      }
    
    return {
      value: "Address is not part of SSLAbuse IP Blocklist"
    }

  def run(self):
    if self._ip == None:
      self._ip = input('Enter IP for lookup: ').strip()

    lookup = self._performLookup(self._ip)
    print(yaml.dump(lookup))
    