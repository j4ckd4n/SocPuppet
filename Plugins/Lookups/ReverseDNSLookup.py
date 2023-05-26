from Plugins import Plugin

import socket

class ReverseDNSLookup(Plugin.Plugin):
  def __init__(self, ip: str = None, name: str = 'ReverseDNSLookup'):
    super().__init__(name)
    self._ip = ip

  def _performLookup(self, ip) -> dict:
    try:
      s = socket.gethostbyaddr(ip)
      resolved_domain = s[0]
    except:
      resolved_domain = "No associated domain found"
    
    return {
      f"{ip}": {
        "resolved_domain": resolved_domain
      }
    }

  def run(self):
    print("\n ---------------------------------- ")
    print("        D N S  R E V E R S E        ")
    print(" ---------------------------------- ")
    if self._ip == None:
      self._ip = input('Enter IP to check: ').strip()

    lookup = self._performLookup(self._ip)
    print(f"\nLookup returned: {lookup[self._ip]['resolved_domain']}")
