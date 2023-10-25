from . import BitcoinAddress, BitcoinTransactionTracer, DNSLookup, ReverseDNSLookup, WhoIs, TorExitNodeLookup, BlockListDELookup, SSLAbuseIPLookup, PhishingDatabase

lookups_dict = {
  0: {
    "name": "Exit to Main Menu",
    "run": 0
  },
  1: {
    "name": "DNS Lookup",
    "run": lambda: DNSLookup.DNSLookup().run()
  },
  2: {
    "name": "Reverse DNS Lookup",
    "run": lambda: ReverseDNSLookup.ReverseDNSLookup().run()
  },
  3: {
    "name": "WhoIs Lookup",
    "run": lambda: WhoIs.WhoIs().run()
  },
  4: {
    "name": "Bitcoin Address Lookup",
    "run": lambda: BitcoinAddress.BitcoinAddress().run()
  },
  5: {
    "name": "Bitcoin Transaction Tracer (WIP, will ban you if ran)",
    "run": lambda: BitcoinTransactionTracer.BitcoinTransactionTracer().run()
  },
  6: {
    "name": "Tor Exit Node Lookup",
    "run": lambda: TorExitNodeLookup.TorExitNodeLookup().run()
  }, 
  7: {
    "name": "BlockListDE blocklist Lookup",
    "run": lambda: BlockListDELookup.BlockListDELookup().run()
  },
  8: {
    "name": "SSLAbuse IP lookup",
    "run": lambda: SSLAbuseIPLookup.SSLAbuseIPLookup().run()
  },
  9: {
    "name": "Phishing Database Lookup",
    "run": lambda: PhishingDatabase.PhishingDatabase().run()
  }
}

def lookupsMenu():
  print("\n ------------------------------------ ")
  print("         L O O K U P  T O O L S        ")
  print(" ------------------------------------- ")
  print(" What would you like to do? \n")
  for item in lookups_dict.keys():
    if item == 0:
      continue
    print(f" OPTION {item}: {lookups_dict[item]['name']}")
  print("\n OPTION 0: Exit to Main Menu")

  try:
    val = int(input(">> "))
    if val not in lookups_dict:
      print("Invalid option specified")
      lookupsMenu()
    elif val == 0:
      return
    else:
      lookups_dict[val]['run']()
  except ValueError:
    print("Invalid option specified")
    lookupsMenu()