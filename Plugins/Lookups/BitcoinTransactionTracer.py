from Plugins import Plugin

import requests
import time

from math import pow

class BitcoinTransactionTracer(Plugin.Plugin):
  def __init__(self, transaction: str = None, name: str = 'BitcoinTransactionTracer'):
    super().__init__(name)
    self._transaction = transaction
    self._endpoint = "https://blockchain.info/rawaddr/"
    self._hardstop = 10
    self._sleep = 5 # seconds

  def run(self):
    print("\n ---------------------------------- ")
    print("    B I T C O I N  T R A C K E R    ")
    print(" ---------------------------------- ")
    print("[INFO]: Still trying to figure out the kinks, you will get banned by the site if you use this tool.")
    if self._transaction == None:
      self._transaction = input('Enter transaction hash here: ').strip()
    
    self._recursiveCall(self._transaction, 0)

  def _recursiveCall(self, val: str, idx: int):
    if idx >= self._hardstop:
      return
    
    res = requests.get(f"{self._endpoint}/{val}")

    if res.status_code != 200:
      print(f"Query failed: {res.content}")
      return
    
    print()
    print("=" * 20)
    rj = res.json()

    txs = rj['txs']

    print(f"Address (base58): {rj['address']}")
    print(f"Address (hash160): {rj['hash160']}")
    
    follow_hash = ""
    amount_transferred = 0

    print(f"Transactions:")
    for tx in txs:
      print(f"  - Transaction Hash: {tx['hash']}")
      print(f"  - Relayed by: {tx['relayed_by']}")
      for output in tx['out']:
        print(f"   - Hash: {output['addr']}")
        print("   - Amount Transferred: %.8f" % (output['value'] / pow(10, 8)))
        if output['value'] > amount_transferred:
          follow_hash = output['addr']
          amount_transferred = output['value']

    print(f"\nFollowing hash: {follow_hash} due to large transaction value of {amount_transferred}/{amount_transferred / pow(10, 8)}")
    print("Sleeping for '%d' seconds.." % self._sleep)
    idx = idx + 1
    time.sleep(self._sleep)
    self._recursiveCall(follow_hash, idx)
