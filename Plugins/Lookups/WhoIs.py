from Plugins import Plugin

from ipwhois import IPWhois

import datetime, os, re, socket

class WhoIs(Plugin.Plugin):
  def __init__(self, value: str = None, name: str = 'WhoIs'):
    super().__init__(name)
    self._value = value
    self._ip_pat = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

  def _performLookup(self, value) -> dict:
    try:
      w = IPWhois(value)
      w = w.lookup_whois()
      addr = str(w['nets'][0]['address'])
      addr = addr.replace('\n', ', ')
      return {
        value: {
          "cidr": str(w['nets'][0]['cidr']),
          "name": str(w['nets'][0]['name']),
          "ip_range": str(w['nets'][0]['range']),
          "description": str(w['nets'][0]['description']),
          "country": str(w['nets'][0]['country']),
          "state": str(w['nets'][0]['state']),
          "city": str(w['nets'][0]['city']),
          "address": addr,
          "postal_code": str(w['nets'][0]['postal_code']),
          "created_date": str(w['nets'][0]['created']),
          "updated_date": str(w['nets'][0]['updated'])
        }
      }
    except Exception as e:
      return {
        value: {
          'err': "Lookup did not return anything."
        }
      }

  def run(self):
    print("\n ----------------------- ")
    print("        W H O I S        ")
    print(" ----------------------- ")

    if self._value == None:
      self._value = input('Enter IP / Domain: ').strip()
    
    self._value = re.sub('(https|http)://', '', self._value)
    
    if not self._ip_pat.match(self._value):
      try:
        s = socket.gethostbyname(self._value)
        print('\nResolved Address: %s' % s)
        self._value = s
      except: 
        print("Domain not found")

    lookup = self._performLookup(self._value)[self._value]
    if "err" in lookup:
      print(f"Lookup Error: {lookup['err']}")
      return
    
    print("\nWHOIS REPORT:")
    print("CIDR:      " + lookup['cidr'])
    print("Name:      " + lookup['name'])
    # print("  Handle:    " + str(w['nets'][0]['handle']))
    print("Range:     " + lookup['ip_range'])
    print("Descr:     " + lookup['description'])
    print("Country:   " + lookup['country'])
    print("State:     " + lookup['state'])
    print("City:      " + lookup['city'])
    print("Address:   " + lookup['address'])
    print("Post Code: " + lookup['postal_code'])
    # print("  Emails:    " + str(w['nets'][0]['emails']))
    print("Created:   " + lookup['created_date'])
    print("Updated:   " + lookup['updated_date'])

    #self._writeToFile(w)
  
  def _writeToFile(self, w: dict):
    now = datetime.datetime.now() # current date and time

    today = now.strftime("%m-%d-%Y")
    if not os.path.exists('output/'+today):
        os.makedirs('output/'+today)

    addr = str(w['nets'][0]['address'])
    addr = addr.replace('\n', ', ')

    f = open('output/'+today+'/'+str(self._value.split()) + ".txt","a+")
    f.write("\n ---------------------------------")
    f.write("\n WHO IS REPORT:")
    f.write("\n ---------------------------------\n")
    f.write("\n CIDR:      " + str(w['nets'][0]['cidr']))
    f.write("\n Name:      " + str(w['nets'][0]['name']))
    # print("  Handle:    " + str(w['nets'][0]['handle']))
    f.write("\n Range:     " + str(w['nets'][0]['range']))
    f.write("\n Descr:     " + str(w['nets'][0]['description']))
    f.write("\n Country:   " + str(w['nets'][0]['country']))
    f.write("\n State:     " + str(w['nets'][0]['state']))
    f.write("\n City:      " + str(w['nets'][0]['city']))
    f.write("\n Address:   " + addr)
    f.write("\n Post Code: " + str(w['nets'][0]['postal_code']))
    # print("  Emails:    " + str(w['nets'][0]['emails']))
    f.write("\n Created:   " + str(w['nets'][0]['created']))
    f.write("\n Updated:   " + str(w['nets'][0]['updated']))

    f.close()