from Plugins import Plugin

import urllib.parse

class URLDecoder(Plugin.Plugin):
  def __init__(self, url: str = None, name = "URL Decoder"):
    super().__init__(name)
    self.name = name
    self._url = url.strip() if url is not None else None

  def run(self):
    print("\n --------------------------------- ")
    print("       U R L   D E C O D E R      ")
    print(" --------------------------------- ")
    if self._url == None:
      self._url = str(input(" Enter URL: ")).strip()

    decodedUrl = urllib.parse.unquote(self._url)
    print(decodedUrl)