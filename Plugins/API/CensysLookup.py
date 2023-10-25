from Plugins import Plugin
from censys.search import CensysHosts
from censys.common.exceptions import *

import yaml

class CensysLookup(Plugin.Plugin):
  def __init__(self, value: str = None, name: str = 'CensysLookup'):
    super().__init__(name)
    self._value = value
    self._censys = None
    try:
      self._censys = CensysHosts()
    except CensysException as e:
      print("Ensure that the API ID and API secret environment variables are set.")
      return

  def _performLookup(self, value) -> dict:
    data = {
      'services': {},
      'location': {},
      'asn': {},
      'os': {},
      'labels': []
    }
    try:
      host = self._censys.view(value)

      # get services
      if 'services' in host:
        for service in host['services']:
          if service['service_name'].lower() == "rdp":
            data['services'].update({service['service_name']: {
              "port": service['port'],
              "transport_protocol": service['transport_protocol'],
              "common_name": service['tls']['certificates']['leaf_data']['subject_dn']
            }})
          elif service['service_name'].lower() == "http" or service['service_name'].lower() == "smb":
            data['services'].update({service['service_name']: {
              "port": service['port'],
              "transport_protocol": service['transport_protocol'],
              "banner": service['banner']
            }})
          else:
            data['services'].update({service['service_name']: {
              "port": service['port'],
              "transport_protocol": service['transport_protocol']
            }})

      if 'location' in host:
        data['location'].update(host['location'])

      if 'autonomous_system' in host:
        data['asn'].update(host['autonomous_system'])

      if 'operating_system' in host:
        data['os'].update({
          "product": host['operating_system']['product'] if 'product' in host['operating_system'] else 'n/a',
          "vendor": host['operating_system']['vendor'] if 'vendor' in host['operating_system'] else 'n/a',
          "version": host['operating_system']['version'] if 'version' in host['operating_system'] else 'n/a',
          "uniform_resource_identifier": host['operating_system']['uniform_resource_identifier'] if 'uniform_resource_identifier' in host['operating_system'] else 'n/a'
        })

      if 'labels' in host:
        for label in host['labels']:
          data['labels'].append(label)
      
    except CensysException as e:
      print(f"This broke: {e}")
      return {value: {'err': e}}  
    
    return {value: data}

  def run(self):
    if self._censys == None:
      return

    if self._value == None:
      self._value = input('Enter an IP address: ').strip()

    print(yaml.dump(self._performLookup(self._value)))