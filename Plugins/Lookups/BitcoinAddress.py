from Plugins import Plugin

from datetime import datetime

import requests, json

from math import pow

class BitcoinAddress(Plugin.Plugin):
  def __init__(self, value: str = None, name: str = 'BitcoinAddress'):
    super().__init__(name)
    self._value = value
    self._endpoint = "https://blockchain.info/rawaddr"

  def run(self):
    print("\n ---------------------------------------- ")
    print("         B I T C O I N  L O O K U P        ")
    print(" ----------------------------------------- ")
    if self._value == None:
      self._value = input('Enter a base58 or hash160 address: ').strip()

    res = requests.get(f'{self._endpoint}/{self._value}')
    
    if res.status_code != 200:
      print(f"Query failed: {res}")
      return
    
    res_json = res.json()

    print(f"""
Address (base58): {res_json['address']}
Address (hash160): {res_json['hash160']}

Total Transactions Recorded: {res_json['n_tx']}
Total Bitcoin Sent: {res_json['total_sent'] / pow(10, 8)} BTC
Total Bitcoin Received: {res_json['total_received'] / pow(10, 8)} BTC
Final Bitcoin Balance: {res_json['final_balance'] / pow(10, 8)} BTC

Transactions:""")

    for trans in res_json['txs']:
      print(f" Transaction ID: {trans['hash']}")
      print(f" Transaction Result: {trans['result'] / pow(10, 8)} BTC")
      print(f" Transaction Time: {datetime.fromtimestamp(trans['time']).__str__()}")
      print(f" From:")
      for inp in trans['inputs']:
        print(f"  Address: {inp['prev_out']['addr']}")
        print(f"  Amount: {inp['prev_out']['value'] / pow(10, 8)} BTC")
      
      print(f" To:")
      for output in trans['out']:
        print(f"  Address: {output['addr']}")
        print(f"  Amount: {output['value'] / pow(10, 8)} BTC")

      print()