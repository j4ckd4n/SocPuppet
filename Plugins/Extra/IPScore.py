from Plugins import Plugin

import requests, json

class IPScore(Plugin.Plugin):
  def __init__(self, ip: str = None, name: str = 'IPScore'):
    super().__init__(name)
    self._ip = ip
    self._url = "https://ip-score.com/json"


  def run(self):
    print("\n ---------------------------------------- ")
    print("        I P S C O R E (Geo Lookup)        ")
    print(" ---------------------------------------- ")
    if self._ip == None:
      self._ip = input('Enter IP to lookup location: ').strip()

    js_dict = {
      "ip": self._ip
    }

    res = requests.post(self._url, data=js_dict)

    if res.status_code != 200:
      print(f"Lookup failed: {res.content}")
      return
    
    data = res.json()

    if data['status'] is not True:
      print(f"Lookup failed: {data}")
      return 
    
    geoip = data['geoip2']

    print(f"""
IP: {data['ip']}
Location: {geoip['city'], geoip['region'], geoip['country']}
ISP: {data['isp']}
Organization: {data['org']}
ASN: {data['asn']}
    """)
