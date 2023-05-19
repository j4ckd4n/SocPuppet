from Plugins import Plugin, ReputationCheck
from Plugins.Decoders import ProofPointDecoder
from Plugins import ReputationCheck

import tkinter.filedialog, os, re

try:
  import win32com.client
except:
  print("Can't install Win32com package")

class AnalyzeEmail(Plugin.Plugin):
  def __init__(self, path: str = None, name: str = 'AnalyzeEmail'):
    super().__init__(name)
    self._proofPointDecoder: ProofPointDecoder.ProofPointDecoder = ProofPointDecoder.ProofPointDecoder()
    self._reputationCheck: ReputationCheck.ReputationCheck = ReputationCheck.ReputationCheck()
    self._path = path

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

  def run(self):
    print("\n ------------------------------- ")
    print("    E M A I L  A N A L Y S I S    ")
    print(" -------------------------------- ")
    try:
      file = tkinter.filedialog.askopenfilename(initialdir="/", title="Select file")
      with open(file, encoding='Latin-1') as f:
        msg = f.read()

      file2 = file.replace(' ', '')
        
      os.rename(file, file2)
      outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
      msg = outlook.OpenSharedItem(file)
    except Exception as e:
      print(f'Failure opening file: {e}')

    print("\nExtracting headers...")
    try:
      print("  FROM:      ", str(msg.SenderName), ", ", str(msg.SenderEmailAddress))
      print("  TO:        ", str(msg.To))
      print("  SUBJECT:   ", str(msg.Subject))
      print("  NameBehalf:", str(msg.SentOnBehalfOfName))
      print("  CC:        ", str(msg.CC))
      print("  BCC:       ", str(msg.BCC))
      print("  Sent On:   ", str(msg.SentOn))
      print("  Created:   ", str(msg.CreationTime))
      msg_body = str(msg.Body)
    except Exception as e:
      print(f'  Header Error: {e}')
      f.close()
    
    links = self._extractLinks(msg_body)
    if links is not None:
      for link in links:
        print(f"- {link}")
    else:
      print("No links found")
    
    emails = self._extractEmails(msg_body)
    if emails is not None:
      for email in emails:
        print(f"- {email}")
    else:
      print("No emails found")

    ips = self._extractIP(msg_body)
    if ips is not None:
      for ip in ips:
        print(f"- {ip}")
    else:
      print("No IPs found")

    user_in = input("Would you like to perform analysis on any gathered URLs and/or Email domains (This may take some time)?\n(y/n): ")
    if user_in.lower() == "y":
      print("\nChecking domains...")
      domains = []
      for email in emails:
        domain = email.split('@')[1]
        if domain not in domains:
          print(f"#### Checking domain: {domain} ####")
          domains.append(domain)
          self._reputationCheck._performCheck(domain, skip_url_scan=True)
      print("-" * 10)
      
      print('\nChecking IPs...')
      checked_ips = []
      for ip in ips:
        if ip not in checked_ips:
          if not self._isPrivate(ip):
            print(f"\n#### Checking IP: {ip} ####")
            checked_ips.append(ip)
            self._reputationCheck._performCheck(ip)
          else:
            print(f"- {ip} is a private address, skipping...")
          checked_ips.append(ip)