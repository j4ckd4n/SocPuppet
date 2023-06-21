from Plugins import Plugin

import requests
import os

class ShodanLookup(Plugin.Plugin):
  def __init__(self, value: str = None, name: str = 'ShodanLookup'):
    super().__init__(name)
    self._value = value
    self._api_key = os.getenv("SHODAN_API_KEY")
    self._shodan_api_host = "https://api.shodan.io/shodan/host"

  def _performLookup(self, value) -> dict:
    if self._api_key == None:
      return {
        value: {
          'err': "No SHODAN_API_KEY environment value set."
        }
      }
    
    res = requests.get(f"{self._shodan_api_host}/{value}?key={self._api_key}")
    if res.status_code != 200:
      return {
        value: {
          'err': res.content
        }
      }
    
    host = res.json()
    data_out = {
      value: {
        "organization": host['org'] if "org" in host.keys() else "n/a",
        "isp": host['isp'] if 'isp' in host.keys() else "n/a",
        "asn": host['asn'] if 'asn' in host.keys() else "n/a",
        "operating_system": host['data']['os'] if "os" in host['data'] else "n/a",
        "additional_data": []
      }
    }
    
    for data in host['data']: 
      data_out[value]['additional_data'].append({
        "port": data['port'] if 'port' in data else "n/a",
        "banner": data['data'][:64] if 'data' in data else "n/a"
      })

    return data_out


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
Operating System: %s""" % (self._value, host['organization'], host['operating_system']))

    print("Banner Info:")
    for item in host['additional_data']:
      print(f"  Port: {item['port']}")
      print(f"    Banner: \n{item['banner']}")
      print() # ❤ i think we need some space...
