from Plugins import Plugin

import requests, json

class IPScore(Plugin.Plugin):
  def __init__(self, ip: str = None, name: str = 'IPScore'):
    super().__init__(name)
    self._ip = ip
    self._url = "https://ip-score.com/json"

  # TODO: Simplify
  def _performLookup(self, value) -> dict:
    js_dict = {
      "ip": value
    }

    res = requests.post(self._url, data=js_dict)

    if res.status_code != 200:
      return {
        value: {
          "err": f"Lookup failed: {res.content}"
        }
      }
    
    data = res.json()
    if data['status'] is not True:
      return {
        value: {
          "err": f"Lookup failed: {data}"
        }
      }

    geoip = data['geoip2']
    return {
      value: {
        "data": data,
        "geoip": geoip
      }
    }

  def run(self):
    print("\n ---------------------------------------- ")
    print("        I P S C O R E (Geo Lookup)        ")
    print(" ---------------------------------------- ")
    if self._ip == None:
      self._ip = input('Enter IP to lookup location: ').strip()

    lookup = self._performLookup(self._ip)
    data = lookup[self._ip]['data']
    geoip = lookup[self._ip]['geoip']

    print(f"""
IP: {data['ip']}
Location: {geoip['city'], geoip['region'], geoip['country']}
ISP: {data['isp']}
Organization: {data['org']}
ASN: {data['asn']}
    """)
