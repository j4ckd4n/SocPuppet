from Plugins import Plugin
from shodan import Shodan

import os

class ShodanLookup(Plugin.Plugin):
  def __init__(self, value: str = None, name: str = 'ShodanLookup'):
    super().__init__(name)
    self._value = value
    self._api_key = os.getenv("SHODAN_API_KEY")

  def run(self):
    print("\n ------------------------------- ")
    print("        S H O D A N . I O        ")
    print(" ------------------------------- ")
    if self._api_key == None:
      print("No SHODAN_API_KEY environment value set.")
      return
    
    if self._value == None:
      self._value = input('Enter an IP to lookup: ').strip()

    try:
      shodan = Shodan(self._api_key)
      host = shodan.host(self._value)
      print("""
      IP: %s
      Organization: %s
      Operating System: %s
      """ % (host['ip_str'], host.get("org", 'n/a'), host.get('os', 'n/a')))

      print(" Banner Info:")
      for item in host['data']:
        print("\tPort: {}\n\tBanner: {}".format(item['port'], item['data']))
    except Exception as e:
      print(e)
