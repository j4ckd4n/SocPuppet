from Plugins import Plugin

from Plugins.Lookups import DNSLookup, ReverseDNSLookup, WhoIs
from Plugins.Extra import ThreatFox, InternetDB, IPScore, inQuest, MalwareBazaar
from Plugins.API import URLScanIO, ShodanLookup, GreyNoise, VirusTotal

import re, socket, yaml, json

class ReputationCheck(Plugin.Plugin):
  def __init__(self, value: str = None, name: str = 'ReputationCheck'):
    super().__init__(name)
    self._value = value
    self._ip_pat = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    self._md5_pattern = r"\b([a-fA-F\d]{32})\b"
    self._sha1_pattern = r"\b([a-fA-F\d]{40})\b"
    self._sha256_pattern = r"\b([a-fA-F\d]{64})\b"

  def _performCheck(self, value, skip_url_scan = False):
    lookups = {}
    if re.search(self._md5_pattern, value) or re.search(self._sha1_pattern, value) or re.search(self._sha256_pattern, value):
      print("Hash detected")
      virus_total_lookup = VirusTotal.VirusTotal()._performLookup(value)
      lookups['virus_total_lookup'] = virus_total_lookup
      malware_bazaar_lookup = MalwareBazaar.MalwareBazaar()._performLookup(value)
      lookups['malware_bazaar_lookup'] = malware_bazaar_lookup
      return
    
    if not self._ip_pat.match(value):
      if not skip_url_scan:  
        URLScanIO.URLScanIO(value).run()
      value = re.sub("(http|https)://", "", value)
      print("Domain detected, attemting to resolve...")
      dns_lookup = DNSLookup.DNSLookup()._performLookup(value)
      lookups['dns_lookup'] = dns_lookup
      try:
        value = socket.gethostbyname(value)
      except:
        print(f"IP for '{value}' was not found")
        return
    
    reverse_dns = ReverseDNSLookup.ReverseDNSLookup()._performLookup(value)
    lookups['reverse_dns_lookup'] = reverse_dns
    threatfox = ThreatFox.ThreatFox()._performLookup(value)
    lookups['threatfox_lookup'] = threatfox
    internetdb_lookup = InternetDB.InternetDB()._performLookup(value)
    lookups['internetdb_lookup'] = internetdb_lookup
    whois_lookup = WhoIs.WhoIs()._performLookup(value)
    lookups['whois_lookup'] = whois_lookup
    grey_noise = GreyNoise.GreyNoise()._performLookup(value)
    lookups['greynoise_lookup'] = grey_noise
    shodan_lookup = ShodanLookup.ShodanLookup()._performLookup(value)
    lookups['shodan_lookup'] = shodan_lookup
    ip_score = IPScore.IPScore()._performLookup(value)
    lookups['ip_score_geo_ip'] = ip_score

    # These take some time to complete.
    inquest_lookup = inQuest.inQuest()._performLookup(value)
    lookups['inquest_lookup'] = inquest_lookup

    print(yaml.dump(lookups))
  
  def _performListLookup(self, values: list, skip_url_scan = False):
    lookups = {}
    for item in values:
      print(f"Performing lookup on: {item}")
      if re.search(self._md5_pattern, item) or re.search(self._sha1_pattern, item) or re.search(self._sha256_pattern, value):
        virus_total_lookup = VirusTotal.VirusTotal()._performLookup(item)
        lookups['virus_total_lookup'] = virus_total_lookup
        malware_bazaar_lookup = MalwareBazaar.MalwareBazaar()._performLookup(item)
        lookups['malware_bazaar_lookup'] = malware_bazaar_lookup
        continue
      
      if not self._ip_pat.match(item):
        if not skip_url_scan:
          print("urlscan not implemented yet")
        item = re.sub("(http|https)://", "", item)
        dns_lookup = DNSLookup.DNSLookup()._performLookup(item)
        lookups['dns_lookup'] = dns_lookup
        try:
          value = socket.gethostbyname(item)
        except:
          continue

      reverse_dns = ReverseDNSLookup.ReverseDNSLookup()._performLookup(value)
      lookups['reverse_dns_lookup'] = reverse_dns
      threatfox = ThreatFox.ThreatFox()._performLookup(value)
      lookups['threatfox_lookup'] = threatfox
      internetdb_lookup = InternetDB.InternetDB()._performLookup(value)
      lookups['internetdb_lookup'] = internetdb_lookup
      whois_lookup = WhoIs.WhoIs()._performLookup(value)
      lookups['whois_lookup'] = whois_lookup
      grey_noise = GreyNoise.GreyNoise()._performLookup(value)
      lookups['greynoise_lookup'] = grey_noise
      shodan_lookup = ShodanLookup.ShodanLookup()._performLookup(value)
      lookups['shodan_lookup'] = shodan_lookup
      ip_score = IPScore.IPScore()._performLookup(value)
      lookups['ip_score_geo_ip'] = ip_score

      # These take some time to complete.
      inquest_lookup = inQuest.inQuest()._performLookup(value)
      lookups['inquest_lookup'] = inquest_lookup

  def run(self):
    print("\n -------------------------------------------- ")
    print("        R E P U T A T I O N  C H E C K        ")
    print(" -------------------------------------------- ")
    if self._value == None:
      self._value = input('Enter IP/Domain/Hash (MD5/SHA1/SHA256): ').strip()

    self._performCheck(self._value)