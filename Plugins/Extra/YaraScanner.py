from Plugins import Plugin

import Plugins.Config as Config

import yara, requests, os

class YaraScanner(Plugin.Plugin):
  def __init__(self, file_path: str = None, name: str = 'YaraScanner'):
    super().__init__(name)
    self._file_path = file_path
    self._local_yara_cache_path = os.path.join(os.getenv("TMP"), ".yara_cache") # not used yet but could be useful later on to prevent consistent pulling of data.

  def _getRuleLinks(self) -> dict:
    rules = Config.config['yara_sources']
    return rules

  # may have to convert this to a recursive rule in case of folders being within folders...
  def _getGithubRules(self, owner, repo, path) -> list:
    if path == "__root__":
      url = f"https://api.github.com/repos/{owner}/{repo}/contents"
    else:
      url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    res = requests.get(url)
    if res.status_code != 200:
      return None
    
    download_links = []
    for item in res.json():
      if item['name'].endswith(".yar"):
        download_links.append(item['download_url'])
      
    return download_links

  def scanFile(self, filepath: str):
    if filepath.endswith(".msg") or filepath.endswith(".eml"):
      rule_sources = self._getRuleLinks()['email']
    else:
      rule_sources = self._getRuleLinks()['file']

    rule_links = []
    for source in rule_sources:
      for path in source['paths']:
        new_rules = self._getGithubRules(source['owner'], source['repo'], path)
        if new_rules == None:
          continue
        rule_links = rule_links + self._getGithubRules(source['owner'], source['repo'], path)


    print(f"Performing YARA scan against: {filepath}")
    for rule_link in rule_links:
      rule = requests.get(rule_link)
      if rule.status_code != 200:
        print(f"Failed to pull rule from: {rule_link}")
        continue

      try:
        compiled = yara.compile(source=rule.text) # precompiling the rules and placing them
      except yara.SyntaxError as e:
        print(f"Err: Yara Syntax error for rule \"{rule_link.split('/')[-1]}\": {e} ")
        continue
      matches = compiled.match(filepath)

      if matches:
        print("\nMatches found:")
        for match in matches:
          print(f"- Rule name: {match.rule}")
          print(f"  - Tags: {match.tags}")
          for string in match.strings:
            print("  - Strings:")
            print(f"    - Identifier: {string.identifier}")
            print(f"    - Instances: {string.instances}")
          print()

  def run(self):
    if self._file_path == None:
      self._file_path = input('Enter the full path for a file to scan: ').strip()

    self.scanFile(self._file_path)