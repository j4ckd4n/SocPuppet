from Plugins import Plugin

import requests

class InternetDB(Plugin.Plugin):
  def __init__(self, value: str = None, name: str = 'InternetDB'):
    super().__init__(name)
    self._value = value

    self._url = "https://internetdb.shodan.io/"

  def _performLookup(self, value) -> dict:
    res = requests.get("{}{}".format(self._url, self._value))
    if res.status_code != 200:
      if res.status_code == 404:
        return {
          value: {
            'err': res.json()['detail']
          }
        }
      return {
        value:{
          'err': f"Lookup failed: {res.text}"
        }
      }
    
    host = res.json()
    return {
      value: host
    }

  def run(self):
    print("\n --------------------------------- ")
    print("        I N T E R N E D D B        ")
    print(" --------------------------------- ")
    print("\tFree tool by Shodan")
    if self._value == None:
      self._value = input('\nEnter IP: ').strip()

    host = self._performLookup(self._value)[self._value]

    if "err" in host.keys():
      print(host['err'])
      return
    
    print()
    if "detail" in host.keys():
      print(host["detail"])
      return

    print(f"IP: {host['ip']}")

    # this can be slimmed down
    if host['ports'] is not None:
      print("Open Ports: ", end="")
      for port in host['ports']:
        print("%s " % port, end="")

    if host['tags']:
      print("\n\nTags:")
      for tag in host['tags']:
        print("\t{}".format(tag))

    if host["cpes"]:
      print("\nCPEs:")
      for cpe in host['cpes']:
        print('\t%s' % cpe)

    if host['vulns']:
      print("\nVulns: ")
      for vuln in host['vulns']:
        print('\t%s' % vuln)
    
    if host['hostnames']:
      print("\nHostnames: ")
      for hostname in host["hostnames"]:
        print('  - %s' % hostname)