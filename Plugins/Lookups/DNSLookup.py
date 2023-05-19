from Plugins import Plugin

import re
import socket

class DNSLookup(Plugin.Plugin):
  def __init__(self, dns: str = None, name: str = 'DNSLookup'):
    super().__init__(name)
    self._dns = dns

  def run(self):
    print("\n -------------------------------- ")
    print("        D N S  L O O K U P        ")
    print(" -------------------------------- ")
    if self._dns == None:
      self._dns = input('Enter DNS value: ').strip()

    self._dns = re.sub("(http|https)://", "", self._dns)
    try:
      s = socket.gethostbyname(self._dns)
      print('\nDomain resolved to: %s' % s)
    except:
      print("IP for '%s' wa not found" % s)
