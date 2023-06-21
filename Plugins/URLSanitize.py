from Plugins import Plugin

import re

class URLSanitize(Plugin.Plugin):
  def __init__(self, url: str = None, name: str = 'URLSanitize'):
    super().__init__(name)
    self._url = url

  def _sanitize(self, url) -> str:
    x = re.sub(r"\.", "[.]", url)
    x = re.sub("http://", "hxxp://", x)
    x = re.sub("https://", "hxxps://", x)
    return x

  def run(self):
    print("\n --------------------------------- ")
    print(" U R L   S A N I T I S E   T O O L ")
    print(" --------------------------------- ")
    if self._url == None:
      self._url = input('Enter URL to sanitize: ').strip()

    print("\n" + self._sanitize(self._url))