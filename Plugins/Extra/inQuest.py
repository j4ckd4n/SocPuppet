from Plugins import Plugin

import requests

class inQuest(Plugin.Plugin):
  def __init__(self, value: str = None, name: str = 'inQuest'):
    super().__init__(name)
    self._value = value
    self._stop = 5
    self._url = "https://labs.inquest.net/"

  # TODO: remove duplicate queries in run() and make it call _performLookup().
  def _performLookup(self, value) -> dict:
    headers = {
      "Accept": "application/json"
    }

    res = requests.get(f"{self._url}api/repdb/search", params={'keyword': value}, headers=headers)

    if res.status_code != 200:
      return {
        value: {
          "err": res.json()['error']
        }
      }
    
    data_arr = res.json()['data']

    if len(data_arr) == 0:
      return {
        value: {
          'err': "lookup did not return any results"
        }
      }

    iocs = {}
    for idx, ioc in enumerate(data_arr):
      if idx > self._stop:
        break
      iocs[f"ioc_{idx+1}"] = {
        'data': ioc['data'],
        'data_type': ioc['data_type'],
        'derived': ioc['derived'],
        'derived_type': ioc['derived_type'],
        'source': ioc['source'],
        'source_url': ioc['source_url']
      }

    return iocs

  def run(self):
    print("\n --------------------------- ")
    print("        i n Q u e s t        ")
    print(" --------------------------- ")
    print(" This may take a while...")
    if self._value == None:
      self._value = input('Enter IP: ').strip()

    headers = {
      "Accept": "application/json"
    }

    res = requests.get(f"{self._url}api/repdb/search", params={'keyword': self._value}, headers=headers)
  
    print() # i think we need some space 💔
  
    if res.status_code != 200:
      print(f"  Failed lookup: {res.status_code}\n Error: {res.json()['error']}")
      return
  
    data_arr = res.json()['data']

    if(len(data_arr) == 0):
      print("  Lookup did not return any results.\n")
      return

    for idx, ioc in enumerate(data_arr):
      if(idx > self._stop):
        print(" Cutting off due to the amount of data pulled.")
        break
      print(f"--== Item #{idx + 1} ==--")
      print(f"""
Data:         {ioc['data']}
Data Type:    {ioc['data_type']}
Derived:      {ioc['derived']}
Derived Type: {ioc['derived_type']}
Source:       {ioc['source']}
Source URL:   {ioc['source_url']}  
    """)
