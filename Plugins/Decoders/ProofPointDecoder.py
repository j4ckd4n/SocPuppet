from Plugins import Plugin

import re
import urllib.parse
import html

class ProofPointDecoder(Plugin.Plugin):
  def __init__(self, url: str = None, name = "ProofPoint Decoder"):
    super().__init__(name)
    self.name = name
    self._url = url.strip() if url is not None else None
    self._url_re = r'https://urldefense.proofpoint.com/(v[0-9])/'
    self._urlv3_re = r'urldefense.com/(v3)/'
  
  def decodev1(self, rewrittenurl):
    match = re.search(r'u=(.+?)&k=', rewrittenurl)

    linksFoundList = []

    if match:
      urlencodedurl = match.group(1)
      htmlencodedurl = urllib.parse.unquote(urlencodedurl)
      url = html.unescape(htmlencodedurl)
      url = re.sub("http://", "", url)
      if url not in linksFoundList:
        linksFoundList.append(url)
    return linksFoundList

  def decodev2(self, rewrittenurl):
    match = re.search(r'u=(.+?)&[dc]=', rewrittenurl)

    linksFoundList = []

    if match:
      specialencodedurl = match.group(1)
      trans = str.maketrans('-_', '%/')
      urlencodedurl = specialencodedurl.translate(trans)
      htmlencodedurl = urllib.parse.unquote(urlencodedurl)
      url = html.unescape(htmlencodedurl)
      url = re.sub("http://", "", url)
      if url not in linksFoundList:
        linksFoundList.append(url)
    return linksFoundList

  def decodev3(self, rewrittenurl):
    match = re.search(r'v3/__(?P<url>.+?)__;', rewrittenurl)
    linksFoundList = []
    if match:
      url = match.group('url')
      if re.search(r'\*(\*.)?', url):
        url = re.sub('\*', '+', url)
        if url not in linksFoundList:
          linksFoundList.append(url)
    return linksFoundList

  def run(self):
    print("\n --------------------------------- ")
    print(" P R O O F P O I N T D E C O D E R ")
    print(" --------------------------------- ")
    if self._url == None:
      self._url = str(input("Enter URL to decode: ")).strip()

    print(self._url)
    match = re.search(self._url_re, self._url)
    matchv3 = re.search(self._urlv3_re, self._url)
    if match:
      if match.group(1) == 'v1':
        links = self.decodev1(self._url)
        for each in links:
          print('\nDecoded Link: %s' % each)
      elif match.group(1) == 'v2':
        links = self.decodev2(self._url)
        for each in links:
          print('\nDecoded Link: %s' % each)
    
    if matchv3 is not None:
      if matchv3.group(1) == 'v3':
        links = self.decodev3(self._url)
        for each in links:
          print('\nDecoded Link: %s' % each)
      else:
        print('No valid URL found in input: ', self._url)
