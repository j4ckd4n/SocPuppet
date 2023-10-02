from Plugins import Plugin

import yaml, requests

class TorExitNodeLookup(Plugin.Plugin):
  def __init__(self, value: str = None, name: str = 'TorExitNodeLookup'):
    super().__init__(name)
    self._value = value
    self._url = 'https://raw.githubusercontent.com/SecOps-Institute/Tor-IP-Addresses/master/tor-exit-nodes.lst'

  def _performLookup(self, value) -> dict:
    output = []
    res = requests.get(self._url)
    if res.status_code != 200:
      return {
        value:{
          'err': res
        }
      }
    
    results = res.content.decode(encoding="utf-8").split('\n')
    if value in results:
      return {
        value: "Address identified is a Tor exit node."
      }
    else:
      return {
        value: "Address does not appear to be part of the Tor network"
      }
  
  def run(self):
    print("\n ------------------------------------------------- ")
    print("        T O R  E X I T  N O D E  L O O K U P        ")
    print(" -------------------------------------------------- ")

    if self._value == None:
      self._value = input('Enter an IP address: ').strip()

    print(yaml.dump(self._performLookup(self._value)))