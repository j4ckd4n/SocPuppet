from Plugins import Plugin

import urllib.parse

class SafeLinksDecoder(Plugin.Plugin):
  def __init__(self, url: str = None, name: str = "Safe Links Decoder"):
    super().__init__(name)
    self._url = url.strip() if url is not None else None

  def run(self):
    print("\n --------------------------------- ")
    print(" S A F E L I N K S   D E C O D E R  ")
    print(" --------------------------------- ")
    if self._url == None:
      self._url = str(input('Enter URL: ').strip())
    dcUrl = urllib.parse.unquote(self._url)
    dcUrl = dcUrl.replace('https://nam02.safelinks.protection.outlook.com/?url=', '')
    print(dcUrl)