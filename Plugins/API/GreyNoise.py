from Plugins import Plugin

import os, requests

class GreyNoise(Plugin.Plugin):
  def __init__(self, ip: str = None, name: str = 'GreyNoise'):
    super().__init__(name)
    self._ip = ip
    self._api_key = os.getenv("GREYNOISE_API_KEY")
    self._url = "https://api.greynoise.io/v3/community/"

  def run(self):
    print("\n ------------------------------- ")
    print("        G R E Y N O I S E        ")
    print(" ------------------------------- ")

    if self._api_key == None:
      print("No GREYNOISE_API_KEY environment value set.")
      return

    if self._ip == None:
      self._ip = input('Enter IP:').strip()

    headers = {
      "accept": "applicatio"
    }
    
    res = requests.get(f'{self._url}{self._ip}', headers=headers)
    data = res.json()
    if res.status_code != 200:
      if res.status_code == 404:
        print(f"\nIP: {self._ip}\nMessage: {data['message']}\n")
      elif res.status_code == 429:
        print(f"\nLookup failed: Limit Exceeded\nPlan: {data['plan']}\nRate Limit: {data['rate-limit']}\nMessage: {data['message']}\n")
      else:
        print(f"\nLookup failed: {res.status_code}/{data['message']}\n")
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