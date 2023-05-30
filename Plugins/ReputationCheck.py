from Plugins import Plugin

from Plugins.Lookups import DNSLookup, ReverseDNSLookup, WhoIs
from Plugins.Extra import ThreatFox, InternetDB, IPScore, inQuest, MalwareBazaar
from Plugins.API import URLScanIO, ShodanLookup, GreyNoise, VirusTotal

import re, socket, yaml, json, time, random, string, os
import datetime

class ReputationCheck(Plugin.Plugin):
  def __init__(self, value: str = None, name: str = 'ReputationCheck'):
    super().__init__(name)
    self._value = value
    self._ip_pat = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    self._md5_pattern = r"\b([a-fA-F\d]{32})\b"
    self._sha1_pattern = r"\b([a-fA-F\d]{40})\b"
    self._sha256_pattern = r"\b([a-fA-F\d]{64})\b"

  def _jitter_sleep(self, jitter_range):
    sleep_time = random.uniform(*jitter_range)
    time.sleep(sleep_time)

  def _random_temp_path(self, length = 16) -> str:
    random_name = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(length))
    temp_path = f"temp_{random_name}"
    return os.path.join(os.getenv("TEMP"), temp_path)

  def _performCheck(self, value, skip_url_scan = False):
    lookups = {}
    if re.search(self._md5_pattern, value) or re.search(self._sha1_pattern, value) or re.search(self._sha256_pattern, value):
      print("Hash detected")
      print("Performing VirusTotal lookup...")
      virus_total_lookup = VirusTotal.VirusTotal()._performLookup(value)
      lookups['virus_total_lookup'] = virus_total_lookup

      print("Performing Malware Bazaar lookup...")
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
    
    print("Performing Revese DNS lookup...")
    reverse_dns = ReverseDNSLookup.ReverseDNSLookup()._performLookup(value)
    lookups['reverse_dns_lookup'] = reverse_dns

    print("Performing ThreatFox lookup...")
    threatfox = ThreatFox.ThreatFox()._performLookup(value)
    lookups['threatfox_lookup'] = threatfox

    print("Performing InternetDB lookup...")
    internetdb_lookup = InternetDB.InternetDB()._performLookup(value)
    lookups['internetdb_lookup'] = internetdb_lookup

    print("Performing WHOIS lookup...")
    whois_lookup = WhoIs.WhoIs()._performLookup(value)
    lookups['whois_lookup'] = whois_lookup

    print("Performing GreyNoise lookup...")
    grey_noise = GreyNoise.GreyNoise()._performLookup(value)
    lookups['greynoise_lookup'] = grey_noise

    print("Performing Shodan lookup...")
    shodan_lookup = ShodanLookup.ShodanLookup()._performLookup(value)
    lookups['shodan_lookup'] = shodan_lookup

    print("Performing IPScore lookup...")
    ip_score = IPScore.IPScore()._performLookup(value)
    lookups['ip_score_geo_ip'] = ip_score

    # These take some time to complete.
    print("Performing inQuest lookup...this may take a while...")
    inquest_lookup = inQuest.inQuest()._performLookup(value)
    lookups['inquest_lookup'] = inquest_lookup

    print(yaml.dump(lookups))
  
  def _performListLookup(self, values: dict, skip_url_scan = False):
    lookups = {
      "virus_total_lookup": [],
      "malware_bazaar_lookup": [],
      "dns_lookup": [],
      "reverse_dns_lookup": [],
      "threatfox_lookup": [],
      "internetdb_lookup": [],
      "whois_lookup": [],
      "greynoise_lookup": [],
      "shodan_lookup": [],
      "ip_score_geo_ip": [],
      "inquest_lookup": []
    }

    hashes = values['hashes']
    domains = values['domains']
    ips = values['ips']

    if hashes:
      print("Checking Hashes...")
      for hash in hashes:
        if re.search(self._md5_pattern, hash) or re.search(self._sha1_pattern, hash) or re.search(self._sha256_pattern, hash):
          virus_total_lookup = VirusTotal.VirusTotal()._performLookup(hash)
          lookups['virus_total_lookup'].append(virus_total_lookup)
          malware_bazaar_lookup = MalwareBazaar.MalwareBazaar()._performLookup(hash)
          lookups['malware_bazaar_lookup'].append(malware_bazaar_lookup)

    if domains:
      print("Checking domains...")
      for domain in domains:
        if not skip_url_scan:
          print("urlscan not implemented yet")
        domain = re.sub("(http|https)://", "", domain)
        dns_lookup = DNSLookup.DNSLookup()._performLookup(domain)
        lookups['dns_lookup'].append(dns_lookup)
        try:
          ip = socket.gethostbyname(domain)
          if ip not in ips:
            ips.append(ip)
        except:
          continue
    
    # TODO: there is a better way to do this but it will work for now.
    # Maybe implement bulk lookup underneath module?
    if ips:
      print("Checking IPs...")
      print("performing reverse lookups")
      for ip in ips:
        reverse_dns = ReverseDNSLookup.ReverseDNSLookup()._performLookup(ip)
        lookups['reverse_dns_lookup'].append(reverse_dns)
      print("performing threatfox lookups")
      for ip in ips:
        threatfox = ThreatFox.ThreatFox()._performLookup(ip)
        lookups['threatfox_lookup'].append(threatfox)
        self._jitter_sleep((0, 5))
      print("performing internetdb lookups")
      for ip in ips:
        internetdb_lookup = InternetDB.InternetDB()._performLookup(ip)
        lookups['internetdb_lookup'].append(internetdb_lookup)
        self._jitter_sleep((0, 5))
      print("performing whois lookups")
      for ip in ips:
        whois_lookup = WhoIs.WhoIs()._performLookup(ip)
        lookups['whois_lookup'].append(whois_lookup)
      print("performing greynoise lookups")
      for ip in ips:
        grey_noise = GreyNoise.GreyNoise()._performLookup(ip)
        lookups['greynoise_lookup'].append(grey_noise)
        self._jitter_sleep((0, 5))
      print("performing shodan lookups")
      for ip in ips:
        shodan_lookup = ShodanLookup.ShodanLookup()._performLookup(ip)
        lookups['shodan_lookup'].append(shodan_lookup)
        self._jitter_sleep((0, 5))
      print("performing ipscore lookups")
      for ip in ips:
        ip_score = IPScore.IPScore()._performLookup(ip)
        lookups['ip_score_geo_ip'].append(ip_score)
        self._jitter_sleep((0, 5))

        # These take some time to complete.
      print("performing inquest lookups...this may take some time...")
      for ip in ips:
        inquest_lookup = inQuest.inQuest()._performLookup(ip)
        lookups['inquest_lookup'].append(inquest_lookup)
    
    print("---=== Results ===---")
    print(yaml.dump(lookups))

    user_in = str(input("Save results? (y/n): "))
    if user_in.lower() == 'y':
      save_location = self._random_temp_path()
      os.mkdir(save_location)
      file_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.yaml")

      with open(os.path.join(save_location, file_name), 'w') as f:
        yaml.dump(lookups, f)

      print(f"File saved: {os.path.join(save_location, file_name)}")

  def run(self):
    print("\n -------------------------------------------- ")
    print("        R E P U T A T I O N  C H E C K        ")
    print(" -------------------------------------------- ")
    if self._value == None:
      self._value = input('Enter IP/Domain/Hash (MD5/SHA1/SHA256): ').strip()

    self._performCheck(self._value)