from Plugins import Plugin

from Plugins.Lookups import DNSLookup, ReverseDNSLookup, WhoIs
from Plugins.Extra import ThreatFox, InternetDB, IPScore, inQuest, MalwareBazaar
from Plugins.API import URLScanIO, ShodanLookup, GreyNoise, VirusTotal

import re, socket

class ReputationCheck(Plugin.Plugin):
  def __init__(self, value: str = None, name: str = 'ReputationCheck'):
    super().__init__(name)
    self._value = value
    self._ip_pat = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    self._md5_pattern = r"\b([a-fA-F\d]{32})\b"
    self._sha1_pattern = r"\b([a-fA-F\d]{40})\b"
    self._sha256_pattern = r"\b([a-fA-F\d]{64})\b"

  def _performCheck(self, value, skip_url_scan = False):
    if re.search(self._md5_pattern, value) or re.search(self._sha1_pattern, value) or re.search(self._sha256_pattern, value):
      print("Hash detected")
      VirusTotal.VirusTotal(value).run()
      MalwareBazaar.MalwareBazaar(value).run()
      return

    if not self._ip_pat.match(value):
      if not skip_url_scan:  
        URLScanIO.URLScanIO(value).run()
      value = re.sub("(http|https)://", "", value)
      print("Domain detected, attemting to resolve...")
      DNSLookup.DNSLookup(value).run()
      try:
        value = socket.gethostbyname(value)
      except:
        print(f"IP for '{value}' was not found")
        return
              
    ReverseDNSLookup.ReverseDNSLookup(value).run()
    ThreatFox.ThreatFox(value).run()
    InternetDB.InternetDB(value).run()
    WhoIs.WhoIs(value).run()
    GreyNoise.GreyNoise(value).run()
    ShodanLookup.ShodanLookup(value).run()
    IPScore.IPScore(value).run()

    # These take some time to complete.
    inQuest.inQuest(value).run()

  def run(self):
    print("\n -------------------------------------------- ")
    print("        R E P U T A T I O N  C H E C K        ")
    print(" -------------------------------------------- ")
    if self._value == None:
      self._value = input('Enter IP/Domain/Hash (MD5/SHA1/SHA256): ').strip()

    self._performCheck(self._value)