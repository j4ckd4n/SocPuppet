from Plugins import Plugin

import Plugins.Config as Config

import yara, requests, os, tkinter.filedialog, yaml

from alive_progress import alive_bar

class YaraScanner(Plugin.Plugin):
  def __init__(self, file_path: str = None, name: str = 'YaraScanner'):
    super().__init__(name)
    self._file_path = file_path
    self._local_yara_cache_path = os.path.join(os.getenv("TMP"), ".yara_cache")
    self._local_temp_file_cache = os.path.join(os.getenv("TMP"), ".yara_download_cache")
    self._github_token = os.getenv("GITHUB_TOKEN")

  def _getRuleLinks(self) -> dict:
    rules = Config.config['yara_sources']
    return rules

  # may have to convert this to a recursive rule in case of folders being within folders...
  def _getGithubRuleLinks(self, owner, repo, path) -> list:
    if path == "__root__":
      url = f"https://api.github.com/repos/{owner}/{repo}/contents"
    else:
      url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    if self._github_token:
      res = requests.get(url, headers={"Authorization": f"Bearer {self._github_token}"})
    else:
      res = requests.get(url)
    if res.status_code != 200:
      print(f"Failed to query github: {res.content}")
      return None
    
    download_links = []
    for item in res.json():
      if item['name'].endswith(".yar"):
        download_links.append(item['download_url'])
      
    return download_links

  def _downloadRules(self, rule_links) -> list:
    rules = []
    with alive_bar(len(rule_links), title="Downloading rules", bar="smooth") as bar:
      for rlink in rule_links:
        rule = requests.get(rlink)
        bar()
        if rule.status_code != 200:
          print(f'Failed to pull fule from: {rlink}')
          continue
        with open(os.path.join(self._local_temp_file_cache, rlink.split('/')[-1]), "w+") as f:
          f.write(rule.text)
        bar.text(f"'{rlink.split('/')[-1]}' rule was downloaded.")
        rules.append((rlink, rule.text))
    return rules

  def _compileRules(self, rules) -> list:
    if not os.path.exists(self._local_yara_cache_path):
      os.mkdir(self._local_yara_cache_path)

    compiled_rules_path_list = []
    with alive_bar(len(rules), title="Compiling rules", bar="smooth") as bar:
      for rule_link, rule in rules:
        try:
          compiled = yara.compile(source=rule)
        except yara.SyntaxError as e:
          print(f"Err: YARA Syntax error for rule \"{rule_link.split('/')[-1]}\": {e}")
          continue
        rule_path = os.path.join(self._local_yara_cache_path, rule_link.split('/')[-1])
        compiled.save(rule_path)
        bar.text(f"'{rule_link.split('/')[-1]}' was compiled")
        compiled_rules_path_list.append(rule_path)
        bar()
    return compiled_rules_path_list
  
  def _getCompiledRules(self) -> list:
    if not os.path.exists(self._local_yara_cache_path):
      return None
    
    compiled_rules_path_list = []
    dir_list = os.listdir(self._local_yara_cache_path)
    print("Getting YARA rules")
    with alive_bar(bar="smooth") as spinner:
      for item in dir_list:
        if item.endswith(".yar"):
          compiled_rules_path_list.append(os.path.join(self._local_yara_cache_path, item))
        spinner()
    return compiled_rules_path_list

  def scanFile(self, filepath: str) -> dict:
    file_name = os.path.split(filepath)[1]
    if not os.path.exists(self._local_yara_cache_path):
      rule_sources = self._getRuleLinks()

      rule_links = []
      for source in rule_sources:
        for path in source['paths']:
          new_rules = self._getGithubRuleLinks(source['owner'], source['repo'], path)
          if new_rules == None:
            continue
          rule_links = rule_links + self._getGithubRuleLinks(source['owner'], source['repo'], path)

      if not os.path.exists(self._local_temp_file_cache):
        os.mkdir(self._local_temp_file_cache)
        rule_list = self._downloadRules(rule_links)
        if not rule_list:
          print("Failed to download rules. Exiting...")
          return
      else:
        print("Using local download cache for compilation")
        files = os.listdir(self._local_temp_file_cache)
        rule_list = []
        for file in files:
          if file.endswith(".yar"):
            rule_list.append(os.path.join(self._local_temp_file_cache, file))
      print("Compiling and saving rules...")
      compiled_rules = self._compileRules(rule_list)
    else:
      compiled_rules = self._getCompiledRules()

    print(f"Performing YARA scan against: {filepath}")
    with alive_bar(len(compiled_rules), bar="smooth") as bar:
      match_list = []
      for compiled_rule in compiled_rules:
        yara_scanner = yara.load(compiled_rule)
        matches = yara_scanner.match(filepath)
        if matches:
          match_list.append(matches)
        bar()
    
    print()

    if match_list:
      output = {file_name: {}}
      for matches in match_list:
        for match in matches:
          output[file_name][f'rule_{match.rule}'] = {"tags": [], 'strings': {}}
          for tag in match.tags:
            output[file_name][f'rule_{match.rule}']['tags'].append(f'{tag}')
          for string in match.strings:
            output[file_name][f'rule_{match.rule}']['strings'][f'{string.identifier}'] = []
            for instance in string.instances:
              output[file_name][f'rule_{match.rule}']['strings'][f'{string.identifier}'].append(f'{instance}')
      return output
    return {file_name: "no detections"}

  def run(self):
    if self._file_path == None:
      self._file_path = tkinter.filedialog.askopenfilename(initialdir="/", title="Select .msg file")

    output = self.scanFile(self._file_path)
    if output:
      print(yaml.dump(output))
    else:
      print("No matches found...")