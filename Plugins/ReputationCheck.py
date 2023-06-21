from Plugins import Plugin

from Plugins.Lookups import DNSLookup, ReverseDNSLookup, WhoIs
from Plugins.Extra import ThreatFox, InternetDB, IPScore, inQuest, MalwareBazaar, YaraScanner
from Plugins.API import URLScanIO, ShodanLookup, GreyNoise, VirusTotal

import re, socket, yaml, json, time, random, string, os
import datetime

from alive_progress import alive_bar

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
      "inquest_lookup": [],
      "yara_scans": []
    }

    hashes = values['hashes']
    domains = values['domains']
    ips = values['ips']
    files = values['files']
    
    with alive_bar(unknown="arrows_out", monitor=False) as progress_bar:
      if hashes:
        print("[RC]: Checking Hashes...")
        for hash in hashes:
          progress_bar()
          if re.search(self._md5_pattern, hash) or re.search(self._sha1_pattern, hash) or re.search(self._sha256_pattern, hash):
            virus_total_lookup = VirusTotal.VirusTotal()._performLookup(hash)
            lookups['virus_total_lookup'].append(virus_total_lookup)
            malware_bazaar_lookup = MalwareBazaar.MalwareBazaar()._performLookup(hash)
            lookups['malware_bazaar_lookup'].append(malware_bazaar_lookup)

      if domains:
        print("[RC]: Checking domains...")
        for domain in domains:
          progress_bar()
          if not skip_url_scan:
            print("[RC]: urlscan not implemented yet")
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
        print("[RC]: Checking IPs...")
        print("[RC]: performing reverse lookups")
        for ip in ips:
          reverse_dns = ReverseDNSLookup.ReverseDNSLookup()._performLookup(ip)
          lookups['reverse_dns_lookup'].append(reverse_dns)
          progress_bar()
        print("[RC]: performing threatfox lookups")
        for ip in ips:
          threatfox = ThreatFox.ThreatFox()._performLookup(ip)
          lookups['threatfox_lookup'].append(threatfox)
          progress_bar()
          self._jitter_sleep((0, 5))
        print("[RC]: performing internetdb lookups")
        for ip in ips:
          internetdb_lookup = InternetDB.InternetDB()._performLookup(ip)
          lookups['internetdb_lookup'].append(internetdb_lookup)
          progress_bar()
          self._jitter_sleep((0, 5))
        print("[RC]: performing whois lookups")
        for ip in ips:
          whois_lookup = WhoIs.WhoIs()._performLookup(ip)
          lookups['whois_lookup'].append(whois_lookup)
          progress_bar()
        print("[RC]: performing greynoise lookups")
        for ip in ips:
          grey_noise = GreyNoise.GreyNoise()._performLookup(ip)
          lookups['greynoise_lookup'].append(grey_noise)
          progress_bar()
          self._jitter_sleep((0, 5))
        print("[RC]: performing shodan lookups")
        for ip in ips:
          shodan_lookup = ShodanLookup.ShodanLookup()._performLookup(ip)
          lookups['shodan_lookup'].append(shodan_lookup)
          progress_bar()
          self._jitter_sleep((0, 5))
        print("[RC]: performing ipscore lookups")
        for ip in ips:
          ip_score = IPScore.IPScore()._performLookup(ip)
          lookups['ip_score_geo_ip'].append(ip_score)
          progress_bar()
          self._jitter_sleep((0, 5))

          # These take some time to complete.
        print("[RC]: performing inquest lookups...this may take some time...")
        for ip in ips:
          inquest_lookup = inQuest.inQuest()._performLookup(ip)
          lookups['inquest_lookup'].append(inquest_lookup)
          progress_bar()
      
    if files:
      print("[RC]: performing yara scans...this may take some time...")
      for file in files:
        detections = YaraScanner.YaraScanner().scanFile(file)
        lookups['yara_scans'].append(detections)

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
      self._value = input('Note: You can specify multiple values separated by ","\nEnter IP/Domain/Hash (MD5/SHA1/SHA256): ').strip()

    lookup_dict = {
      "ips": [],
      "hashes": [],
      'files': [],
      'domains': []
    }

    if "," in self._value:
      item_array = self._value.split(',')
      for item in item_array:
        item = item.strip()
        if re.search(self._md5_pattern, item) or re.search(self._sha1_pattern, item) or re.search(self._sha256_pattern, item):
          lookup_dict['hashes'].append(item)
        elif not self._ip_pat.match(item):
          lookup_dict['domains'].append(item)
        else:
          lookup_dict['ips'].append(item)
    else:
      if re.search(self._md5_pattern, self._value) or re.search(self._sha1_pattern, self._value) or re.search(self._sha256_pattern, self._value):
        lookup_dict['hashes'].append(self._value)
      elif not self._ip_pat.match(self._value):
        lookup_dict['domains'].append(self._value)
      else:
        lookup_dict['ips'].append(self._value)

    print(lookup_dict)

    self._performListLookup(lookup_dict)