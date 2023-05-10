from Plugins import Plugin

#from unfurl import core

class UnFurlURL(Plugin.Plugin):
  def __init__(self, url: str = None, name: str = 'UnFurlURL'):
    super().__init__(name)
    self._url = url

  def run(self):
    print("  Not functional at this time. Sorry 😢💔")
    return

    if self._url == None:
      self._url = input(' Enter a URL: ').strip()

    #unfurl_instance = core.Unfurl()
    #unfurl_instance.add_to_queue(data_type='url', key=None, value=self._url)
    #unfurl_instance.parse_queue()
    #print(unfurl_instance.generate_text_tree())
