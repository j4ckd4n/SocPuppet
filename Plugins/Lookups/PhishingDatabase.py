from Plugins import Plugin

import requests
import re
import yaml

class PhishingDatabase(Plugin.Plugin):
  def __init__(self, ioc: str = None, name: str = 'PhishingDatabase'):
    super().__init__(name)
    self.ioc = ioc
    self.pd_links_active = "https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-links-ACTIVE.txt"
    self.pd_domains_active = "https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-domains-ACTIVE.txt"
    self.pd_ips_active = "https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-IPs-ACTIVE.txt"

    self._ip_pat = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

  def _performRequest(self, url) -> list:
    res = requests.get(url)
    if res.status_code != 200:
      return None

    return res.content.decode(encoding="utf-8").split('\n')


  def _performLookup(self, value) -> dict:
    if re.search(self._ip_pat, value):
      arr = self._performRequest(self.pd_ips_active)

      if value in arr:
        return {
          value: "Value found in a Phishing Database."
        }
      
      return {
        value: "Value not observed used for phishing"
      }
    else:
      arr = []
      arr += self._performRequest(self.pd_links_active)
      arr += self._performRequest(self.pd_domains_active)

      matches = [item for item in arr if value in item]
      
      if len(matches) <= 0:
        return {
          value: "Value not observed used for phishing"
        }
      
      return {
        value: "Observed to be used for phishing."
      }

  def run(self):
    if self.ioc == None:
      self.ioc = input('Enter a domain/IP:').strip()

    print(yaml.dump(self._performLookup(self.ioc)))