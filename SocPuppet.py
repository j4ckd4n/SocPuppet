from Plugins.Plugin import Plugin
from Plugins.URLSanitize import URLSanitize
from Plugins.ReputationCheck import ReputationCheck

import Plugins.Extra as Extras
import Plugins.Email as Email
import Plugins.Decoders as Decoders
import Plugins.API as API
import Plugins.Lookups as Lookups

import Plugins.Config as Config

import importlib.util
import os
import inspect
import sys
import json

VERSION = "unknown"

# This may be possible to simplify
mainMenu_dict = {
  0: lambda: sys.exit(0),
  1: lambda: URLSanitize().run(),
  2: lambda: ReputationCheck().run(),
  3: lambda: Decoders.decoderMenu(),
  4: lambda: Email.emailMenu(),
  5: lambda: API.apiMenu(),
  6: lambda: Lookups.lookupsMenu(),
  7: lambda: Extras.extraMenu()
}

def mainMenu():
  print("\n What would you like to do? ")
  print("\n OPTION 1: Sanitize URL")
  print(" OPTION 2: Reputation Check")
  print(" OPTION 3: Decoders (PP, URL, SafeLinks) ")
  print(" OPTION 4: Email Tools ")
  print(" OPTION 5: API Tools (require API keys)")
  print(" OPTION 6: Lookup Tools")
  print(" OPTION 7: Extra (Free online lookups and tools)")
  print("\n OPTION 0: Exit Tool")
  try:
    val = int(input(">> "))
    if val not in mainMenu_dict:
      print("Invalid value specified.")
      mainMenu()
    else:
      mainMenu_dict[val]()
  except ValueError:
    print("Invalid Value specified")
    mainMenu()
  

if __name__ == "__main__":
  # TODO: need a check for this to see if the config.json file exists
  Config.loadConfig("config.json")
  
  print("\n ------------------------------------ ")
  print("           S O C P U P P E T          ")
  print(" ------------------------------------ ")
  print(f"            Version: {Config.config['version']}       ")

  try:
    while True:
      mainMenu()
  except KeyboardInterrupt as e:
    print("Bye!")
    sys.exit(1)