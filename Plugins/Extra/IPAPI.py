from Plugins import Plugin

import requests

class IPAPI(Plugin.Plugin):
  def __init__(self, ip: str = None, name: str = 'IPAPI'):
    super().__init__(name)
    self._ip = ip
    self._url = "http://ip-api.com/json/"

  def run(self):
    print("\n ------------------------------------ ")
    print("        I P A P I (Geo Lookup)        ")
    print(" ------------------------------------ ")
    if self._ip == None:
      self._ip = input('Enter IP to locate: ').strip()

    res = requests.get(f"{self._url}{self._ip}?fields=21221105")
    if res.status_code != 200:
      if res.status_code == 429:
        print(f"\nLookup failed: Exceeded Lookup Usage.\n\tTime until reset: {res.headers['X-Ttl']}\n")
      else:
        print(f"\nLookup failed: {res.status_code}\n")
      return
    
    data = res.json()
    print(f"""
Location:     {data['city']}, {data['country']}, {data['zip']}
ISP:          {data['isp']}
Organization: {data['org']}
AS:           {data['as']}
Mobile:       {data['mobile']}
Proxy:        {data['proxy']}
Hosting:      {data['hosting']}
  """)