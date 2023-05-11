from Plugins import Plugin

import requests

class UnShortenURL(Plugin.Plugin):
  def __init__(self, url: str = None, name = "UnShorten URL"):
    super().__init__(name)
    self._url = url.strip() if url is not None else None

  def run(self):
    print("\n --------------------------------- ")
    print("   U R L   U N S H O R T E N E R  ")
    print(" --------------------------------- ")
    if self._url == None:
      self._url = str(input('Enter URL: ').strip())
    req = requests.get(str('https://unshorten.me/s/' + self._url))
    print(req.text)