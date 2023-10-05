from Plugins import Plugin

from Plugins.Lookups import DNSLookup, ReverseDNSLookup, WhoIs, TorExitNodeLookup, BlockListDELookup, SSLAbuseIPLookup
from Plugins.Extra import ThreatFox, InternetDB, IPScore, inQuest, MalwareBazaar, YaraScanner
from Plugins.API import URLScanIO, ShodanLookup, GreyNoise, VirusTotal

import re, socket, yaml, json, time, random, string, os
import datetime

from alive_progress import alive_bar

from pygments import highlight
from pygments.lexers.data import YamlLexer
from pygments.formatters import TerminalFormatter

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
  
  def flatten_data(self, data, prefix=''):
    flattened_data = []
    if isinstance(data, dict):
      for key, value in data.items():
        flattened_data.extend(self.flatten_data(value, prefix=f'{prefix}{key}.'))
    elif isinstance(data, list):
      for index, item in enumerate(data):
        flattened_data.extend(self.flatten_data(item, prefix=f'{prefix}{index}.'))
    else:
      flattened_data.append((prefix.rstrip('.'), data))

    return flattened_data

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
      "yara_scans": [],
      "tor_nodes": [],
      "blocklists": []
    }

    hashes = values['hashes']
    domains = values['domains']
    ips = values['ips']
    files = values['files']
    
    with alive_bar(unknown="arrows_out", monitor=False) as progress_bar:
      if hashes:
        for hash in hashes:
          print(f"[RC]: Checking hash: {hash}")
          progress_bar()
          if re.search(self._md5_pattern, hash) or re.search(self._sha1_pattern, hash) or re.search(self._sha256_pattern, hash):
            progress_bar.text("Performing VirusTotal lookup")
            virus_total_lookup = VirusTotal.VirusTotal()._performLookup(hash)
            lookups['virus_total_lookup'].append(virus_total_lookup)

            progress_bar.text("Performing MalwareBazaar lookup")
            malware_bazaar_lookup = MalwareBazaar.MalwareBazaar()._performLookup(hash)
            lookups['malware_bazaar_lookup'].append(malware_bazaar_lookup)

      if domains:
        for domain in domains:
          print(f"[RC]: Checking domain: {domain}")
          progress_bar()
          if not skip_url_scan:
            print("[RC]: urlscan not implemented yet")
          domain = re.sub("(http|https)://", "", domain)
          progress_bar.text("Performing DNS Lookup")
          dns_lookup = DNSLookup.DNSLookup()._performLookup(domain)
          lookups['dns_lookup'].append(dns_lookup)
          progress_bar.text("Performing WHOIS lookup")
          whois_lookup = WhoIs.WhoIs()._performLookup(domain)
          lookups['whois_lookup'] += whois_lookup
          try:
            ip = socket.gethostbyname(domain)
            if ip not in ips:
              ips.append(ip)
          except:
            continue

      # TODO: there is a better way to do this but it will work for now.
      # Maybe implement bulk lookup underneath module?
      if ips:
        for ip in ips:
          print(f"[RC]: Checking IP: {ip}")
          progress_bar.text("Performing reverse lookup")
          reverse_dns = ReverseDNSLookup.ReverseDNSLookup()._performLookup(ip)
          lookups['reverse_dns_lookup'].append(reverse_dns)

          progress_bar.text("Performing ThreatFox lookup")
          threatfox = ThreatFox.ThreatFox()._performLookup(ip)
          lookups['threatfox_lookup'].append(threatfox)
          
          progress_bar.text("Performing InternetDB lookup")
          internetdb_lookup = InternetDB.InternetDB()._performLookup(ip)
          lookups['internetdb_lookup'].append(internetdb_lookup)
          
          if ip not in lookups['whois_lookup']:
            progress_bar.text("Performing WHOIS lookup")
            whois_lookup = WhoIs.WhoIs()._performLookup(ip)
            lookups['whois_lookup'] += whois_lookup

          progress_bar.text("Performing GreyNoise lookup")
          grey_noise = GreyNoise.GreyNoise()._performLookup(ip)
          lookups['greynoise_lookup'].append(grey_noise)

          progress_bar.text("Performing Shodan lookup")
          shodan_lookup = ShodanLookup.ShodanLookup()._performLookup(ip)
          lookups['shodan_lookup'].append(shodan_lookup)

          progress_bar.text("Performing IPScore lookup")
          ip_score = IPScore.IPScore()._performLookup(ip)
          lookups['ip_score_geo_ip'].append(ip_score)
          
          progress_bar.text("Checking against Tor exit nodes")
          tor = TorExitNodeLookup.TorExitNodeLookup()._performLookup(ip)
          lookups['tor_nodes'].append(tor)

          progress_bar.text("Checking against blocklists")
          blocklistde = BlockListDELookup.BlockListDELookup()._performLookup(ip)
          lookups['blocklists'].append({"blocklistde": blocklistde})
          
          sslabuse_ip = SSLAbuseIPLookup.SSLAbuseIPLookup()._performLookup(ip)
          lookups['blocklists'].append({'sslabuse_ip': sslabuse_ip})
      
    if files:
      print("[RC]: performing yara scans...this may take some time...")
      for file in files:
        detections = YaraScanner.YaraScanner().scanFile(file)
        lookups['yara_scans'].append(detections)

    print("---=== Results ===---")
    print(highlight(yaml.dump(lookups, sort_keys=False), YamlLexer(), TerminalFormatter()))

    # TODO Formatting could be better than just a YAML dump.
    # print("---=== Flattened ===---")
    # for key in lookups.keys():
    #   print(f"{key}:")
    #   for index in lookups[key]:
    #     print(f'  - {index}:')
    #     print(f"    - {self.flatten_data(lookups[key][index])}")

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