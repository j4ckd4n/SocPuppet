from . import GreyNoise, ShodanLookup, URLScanIO, VirusTotal

api_dict = {
  0: {
    "name": "Exit to Main Menu",
    "run": 0
  },
  1: {
    "name": "GreyNoise Search (Community API)",
    "run": lambda: GreyNoise.GreyNoise().run()
  },
  2: {
    "name": "Shodan Search",
    "run": lambda: ShodanLookup.ShodanLookup().run()
  },
  3: {
    "name": "URLScan.io URL Search (WIP)",
    "run": lambda: URLScanIO.URLScanIO().run()
  },
  4: {
    "name": "VirusTotal Search (Community API)",
    "run": lambda: VirusTotal.VirusTotal().run()
  }
}

def apiMenu():
  print("\n ------------------------------------ ")
  print("           A P I  T O O L S           ")
  print(" ------------------------------------ ")
  print(" What would you like to do? ")
  for item in api_dict.keys():
    if item == 0:
      continue
    print(f" OPTION {item}: {api_dict[item]['name']}")
  print("\n OPTION 0: Exit to Main Menu")
  try:
    val = int(input(">> "))
    if val not in api_dict:
      print("Invalid option specified")
      apiMenu()
    elif val == 0:
      return
    else:
      api_dict[val]['run']()
  except ValueError:
    print("Invalid option specified")
    apiMenu()