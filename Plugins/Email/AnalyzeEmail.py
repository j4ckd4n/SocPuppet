from Plugins import Plugin, ReputationCheck
from Plugins.Decoders import ProofPointDecoder
from Plugins import ReputationCheck
from Plugins.Extra import YaraScanner

import tkinter.filedialog, os, re, extract_msg, random, string, hashlib

class AnalyzeEmail(Plugin.Plugin):
  def __init__(self, path: str = None, name: str = 'AnalyzeEmail'):
    super().__init__(name)
    # TODO: fix...this is ugly 
    self._proofPointDecoder: ProofPointDecoder.ProofPointDecoder = ProofPointDecoder.ProofPointDecoder()
    self._reputationCheck: ReputationCheck.ReputationCheck = ReputationCheck.ReputationCheck()
    self._yaraScanner: YaraScanner.YaraScanner = YaraScanner.YaraScanner()
    self._path = path
    self._buf_size = 65536 # reading the file in chunks to ensure we don't overload memory during hash generation.

  def _extractLinks(self, data) -> list:
    print("\nExtracting Links...")
    try:
      link_list = []
      match = r"((www\.|http://|https://)(www\.)*.*?(?=(www\.|http://|https://|$)))"
      a = re.findall(match, data, re.M | re.I)

      if len(a) == 0:
        return None

      for b in a:
        match = re.search(r'https://urldefense.proofpoint.com/(v[0-9])/', b[0])
        if match:
          if match.group(1) == 'v1':
            links = self._proofPointDecoder.decodev1(b[0])
          elif match.group(1) == 'v2':
            links = self._proofPointDecoder.decodev2(b[0])
          elif match.group(1) == 'v3':
            links = self._proofPointDecoder.decodev3(b[0])
          else:
            continue
          for link in links:
            if link not in link_list:
              link_list.append(link)
        else:
          if b[0] not in link_list:
            link_list.append(b[0])
      return link_list
    except Exception as e:
      print(f"Err: {e}")
      return None

  def _extractEmails(self, data) -> list:
    print("\nExtracting Emails...")
    email_list = []
    try:
      match = r'([\w0-9._-]+@[\w0-9._-]+\.[\w0-9_-]+)'
      a = re.findall(match, data, re.M | re.I)

      if len(a) == 0:
        return None
      
      for b in a:
        if b not in email_list:
          email_list.append(b)
      
      return email_list
    except Exception as e:
      print(f"Err: {e}")
      return None

  def _extractIP(self, data) -> list:
    try:
      print("\nExtracting IP...")
      found_ips = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', data)

      if len(found_ips) == 0:
        return None
      
      return found_ips
    except Exception as e:
      print(f"Err: {e}")
      return None

  def _isPrivate(self, ip) -> bool:
    priv_lo = re.compile("^127\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    priv_24 = re.compile("^10\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    priv_20 = re.compile("^192\.168\.\d{1,3}.\d{1,3}$")
    priv_16 = re.compile("^172.(1[6-9]|2[0-9]|3[0-1]).[0-9]{1,3}.[0-9]{1,3}$")

    res = priv_lo.match(ip) or priv_24.match(ip) or priv_20.match(ip) or priv_16.match(ip)
    return True if res else False

  def _random_temp_path(self, length = 16) -> str:
    random_name = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(length))
    temp_path = f"temp_{random_name}"
    return os.path.join(os.getenv("TEMP"), temp_path)

  def run(self):
    print("\n ------------------------------- ")
    print("    E M A I L  A N A L Y S I S    ")
    print(" -------------------------------- ")
    file = tkinter.filedialog.askopenfilename(initialdir="/", title="Select .msg file")
    try:
      msg = extract_msg.openMsg(file)
    except extract_msg.exceptions.StandardViolationError as e:
      print("Err: Incorrect or corrupted file selected.")
      return

    print("\nExtracting headers...")
    print("  FROM:      ", str(msg.sender))
    print("  TO:        ", str(msg.to))
    print("  SUBJECT:   ", str(msg.subject))
    print("  CC:        ", str(msg.cc))
    print("  BCC:       ", str(msg.bcc))
    print("  Sent On:   ", str(msg.date))

    links = self._extractLinks(msg.body)
    if links is not None:
      for link in links:
        print(f"- {link}")
    else:
      print("No links found")
    
    emails = self._extractEmails(msg.body)
    if emails is not None:
      for email in emails:
        print(f"- {email}")
    else:
      print("No emails found")

    ips = self._extractIP(msg.body)
    if ips is not None:
      for ip in ips:
        print(f"- {ip}")
    else:
      print("No IPs found")

    print() # ❤ we just need some space

    attachment_paths = []
    if len(msg.attachments) != 0:
      user_in = input("Would you like to extract the attachments from the email? (Be careful with this cause attachments may contain malicious code)?\n(y/n): ")
      if user_in.lower() == "y":
        temp_path = self._random_temp_path()
        os.mkdir(temp_path)
        for attachment in msg.attachments:
          attachment_file_path = attachment.save()
          attachment_name = os.path.basename(attachment_file_path)
          new_file_path = os.path.join(temp_path, attachment_name)
          os.rename(attachment_file_path, new_file_path)
          print(f"- Attachment {attachment_name} saved to: {temp_path}")
          attachment_paths.append(new_file_path)
      print() # ❤ we just need some space

    user_in = input("Would you like to perform analysis on any gathered URLs, Email domains, and attachments (This may take some time)?\n(y/n): ")
    if user_in.lower() == "y":
      self._yaraScanner.scanFile(file)

      items_to_lookup = {
        "domains": [],
        "ips": [],
        "hashes": []
      }

      # need to be rewritten to support for a combined reputation check.
      # not enough time to write this.
      if emails:
        print("Gathering domains...")
        for email in emails:
          domain = email.split('@')[1]
          if domain not in items_to_lookup['domains']:
            items_to_lookup['domains'].append(domain)
      
      if ips:
        print('Gathering IPs...')
        for ip in ips:
          if ip not in items_to_lookup['ips']:
            if not self._isPrivate(ip):
              items_to_lookup['ips'].append(ip)
      
      if attachment_paths:
        print('Gathering attachments...')
        for attachment in attachment_paths:
          print(f"\nCalculating SHA1 value for {attachment}: ", end="")
          sha1 = hashlib.sha1()
          with open(attachment, 'rb') as f:
            while data := f.read(self._buf_size):
              sha1.update(data)
          hash = str(sha1.hexdigest())
          print(hash)
          if hash not in items_to_lookup['hashes']:
            items_to_lookup['hashes'].append(hash)
      
      self._reputationCheck._performListLookup(items_to_lookup, True)
      
      print("Performing reputation check on gathered information")
      user_in = input("Perform Yara scans on attachments? (Warning this may take some time to complete)\n(y/n):")
      if user_in.lower() == "y":
        for attachment in attachment_paths:
          self._yaraScanner.scanFile(attachment)