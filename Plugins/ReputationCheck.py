from Plugins import Plugin

from Plugins.DNS import DNSLookup, ReverseDNSLookup, WhoIs
from Plugins.Extra import ThreatFox, InternetDB, IPAPI, inQuest, MalwareBazaar
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

  def run(self):
    print("\n -------------------------------------------- ")
    print("        R E P U T A T I O N  C H E C K        ")
    print(" -------------------------------------------- ")
    if self._value == None:
      self._value = input('Enter IP/Domain/Hash (MD5/SHA1/SHA256): ').strip()

    if re.search(self._md5_pattern, self._value) or re.search(self._sha1_pattern, self._value) or re.search(self._sha256_pattern, self._value):
      print("Hash detected")
      VirusTotal.VirusTotal(self._value).run()
      MalwareBazaar.MalwareBazaar(self._value).run()
      return

    if not self._ip_pat.match(self._value):  
      URLScanIO.URLScanIO(self._value).run()
      self._value = re.sub("(http|https)://", "", self._value)
      print("Domain detected, attemting to resolve...")
      DNSLookup.DNSLookup(self._value).run()
      try:
        self._value = socket.gethostbyname(self._value)
      except:
        print(f"IP for '{self._value}' was not found")
        return
              
    ReverseDNSLookup.ReverseDNSLookup(self._value).run()
    ThreatFox.ThreatFox(self._value).run()
    InternetDB.InternetDB(self._value).run()
    WhoIs.WhoIs(self._value).run()
    GreyNoise.GreyNoise(self._value).run()
    ShodanLookup.ShodanLookup(self._value).run()
    IPAPI.IPAPI(self._value).run()

    # These take some time to complete.
    inQuest.inQuest(self._value).run()