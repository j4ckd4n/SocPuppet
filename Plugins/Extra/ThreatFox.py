from Plugins import Plugin

import requests, json

class ThreatFox(Plugin.Plugin):
  def __init__(self, query: str = None, name: str = "Threat Fox Lookup"):
    super().__init__(name)

    self._query = query
    self._url = "https://threatfox-api.abuse.ch/api/v1/"

  def _performLookup(self, query) -> dict:
    data = {
      "query": "search_ioc",
      "search_term": query
    }

    res = requests.post(self._url, data=json.dumps(data)).json()
    if "no_result" in res['query_status']:
      print(res['data'])
      return {
        query: {
          "err": res['data']
        }
      }
    
    content = res['data'][0]

    return {
      query: content
    }


  def run(self):
    print("\n ------------------------------- ")
    print("        T H R E A T F O X        ")
    print(" ------------------------------- ")
    if self._query == None:
      self._query = input("Enter an IP/URL: ").strip()
    
    content = self._performLookup(self._query)[self._query]

    if "err" in content.keys():
      print(f"Lookup error: {content['err']}")
    
    print(f"""
IoC: {content['ioc']}
Confidence: {content['confidence_level']}
Threat Type: {content['threat_type']}
Threat Type Description: {content['threat_type_desc']}

Malware: {content['malware_printable']}
Malware Alias: {content['malware_alias']}
Malpedia: {content['malware_malpedia']}

First Seen: {content['first_seen']}
Reporter: {content['reporter']}
    """)

    if content['tags']:
      print("Tags:")
      for tag in content['tags']:
        print(f"    - {tag}")
    
    if content['malware_samples']:
      print("Malware Samples:")
      for sample in content['malware_samples']:
        print(f"""
  - SHA256: {sample['sha256_hash']}
  - Malware Bazaar Link: {sample['malware_bazaar']}
        """)
