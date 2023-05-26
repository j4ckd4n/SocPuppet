from Plugins import Plugin
from shodan import Shodan

import os

class ShodanLookup(Plugin.Plugin):
  def __init__(self, value: str = None, name: str = 'ShodanLookup'):
    super().__init__(name)
    self._value = value
    self._api_key = os.getenv("SHODAN_API_KEY")

  # TODO: This is broken, seems like the exception being thrown is "banner" and nothing else. May need to convert to 
  def _performLookup(self, value) -> dict:
    if self._api_key == None:
      return {
        value:{
          'err': "No SHODAN_API_KEY environment value set."
        }
      }

    try:
      shodan = Shodan(self._api_key)
      host = shodan.host(value)
      data_out = {
        value: {
          "ip": value,
          "organization": host.get("org", "n/a"),
          "operating_system": host.get("os", "n/a"),
          "additional_data": {}
        }
      }

      for item in host['data']:
        data_out[value]['additional_data'] = {
          "port": item['port'],
          "banner": item['banner']
        }
      return data_out
    except Exception as e:
      print(e)
      return {
        value: {
          'err': e
        }
      }

  def run(self):
    print("\n ------------------------------- ")
    print("        S H O D A N . I O        ")
    print(" ------------------------------- ")
    if self._api_key == None:
      print("No SHODAN_API_KEY environment value set.")
      return
    
    if self._value == None:
      self._value = input('Enter an IP to lookup: ').strip()

    host = self._performLookup(self._value)[self._value]
    if "err" in host.keys():
      print(f"Lookup failed: {host['err']}")
      return
    
    print("""
IP:               %s
Organization:     %s
Operating System: %s""" % (host['ip'], host['organization'], host['operating_system']))

    print("Banner Info:")
    for item in host['additional_data']:
      print(f"  Port: {item['port']}")
      print(f"    Banner: \n{item['data']}")
      print() # ❤ i think we need some space...
