from Plugins import Plugin

import re
import socket

class DNSLookup(Plugin.Plugin):
  def __init__(self, dns: str = None, name: str = 'DNSLookup'):
    super().__init__(name)
    self._dns = dns

  def _performLookup(self, dns) -> dict:
    dns = re.sub("(http|https)://", "", dns)
    try:
      dns_resolution = socket.gethostbyname(dns)
    except:
      dns_resolution = "No IP association found."

    return {
      f"{dns}": {
        "dns_resolution": dns_resolution
      }
    }

  def run(self):
    print("\n -------------------------------- ")
    print("        D N S  L O O K U P        ")
    print(" -------------------------------- ")
    if self._dns == None:
      self._dns = input('Enter DNS value: ').strip()

    self._dns = re.sub("(http|https)://", "", self._dns)
    lookup = self._performLookup(self._dns)
    print(f"\nLookup returned: {lookup[self._dns]['dns_resolution']}")