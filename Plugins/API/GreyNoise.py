from Plugins import Plugin

import os, requests, yaml

class GreyNoise(Plugin.Plugin):
  def __init__(self, ip: str = None, name: str = 'GreyNoise'):
    super().__init__(name)
    self._ip = ip
    self._api_key = os.getenv("GREYNOISE_API_KEY")
    self._url = "https://api.greynoise.io/v3/community/"

  def _performLookup(self, ip) -> dict:
    if self._api_key == None:
      return {
        ip: {
          "err": "No GREYNOISE_API_KEY environment value set."
        }
      }

    headers = {
      "accept": "application/json",
      "key": self._api_key
    }
    
    res = requests.get(f'{self._url}{ip}', headers=headers)
    data = res.json()
    if res.status_code != 200:
      if res.status_code == 404:
        err = {
          "err": data['message']
        }
      elif res.status_code == 429:
        err = {
          "err": f"Rate-limit hit. Plan: {data['plan']}"
        }
      else:
        err = {
          "err": f"Lookup failed: {res.status_code}/{data['message']}"
        }
      return {ip : err}
    
    return {
      f"{ip}": {
        "observed_scanner": data['noise'],
        "known_good": data['riot'],
        "classification": data['classification'],
        "name": data['name'],
        "link": data['link'],
        "last_seen": data['last_seen'],
        "message": data['message']
      }
    }

  def run(self):
    print("\n ------------------------------- ")
    print("        G R E Y N O I S E        ")
    print(" ------------------------------- ")

    if self._api_key == None:
      print("No GREYNOISE_API_KEY environment value set.")
      return

    if self._ip == None:
      self._ip = input('Enter IP: ').strip()
    
    data = self._performLookup(self._ip)

    if "err" in data[self._ip].keys():
      print(f"""
IP:       {data[self._ip]}
Error:    {data[self._ip]['err']}      
""")
      return

    print(f"""
IP:                         {data['ip']}
Observed Scanning the Web:  {data['noise']}
Known Good:                 {data['riot']}
Classification:             {data['classification']}
Name:                       {data['name']}
Link:                       {data['link']}
Last Seen:                  {data['last_seen']}
Message:                    {data['message']}
""")