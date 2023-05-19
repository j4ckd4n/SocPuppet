from Plugins.Plugin import Plugin
from Plugins.URLSanitize import URLSanitize
from Plugins.ReputationCheck import ReputationCheck

import importlib.util
import os
import inspect

VERSION = "1.1.5"

# This may be possible to simplify
mainMenu_dict = {
  0: lambda: exit(0),
  1: lambda: URLSanitize().run(),
  2: lambda: ReputationCheck().run(),
  3: lambda: decoderMenu(),
  4: lambda: emailMenu(),
  5: lambda: apiMenu(),
  6: lambda: lookupsMenu(),
  7: lambda: extraMenu()
}

decoders_dict = {
  0: {
    "name": "Exit to Main Menu",
    "run": lambda: mainMenu()
  },
}

dns_dict = {
  0: {
    "name": "Exit to Main Menu",
    "run": lambda: mainMenu()
  }
}

lookups_dict = {
  0: {
    "name": "Exit to Main Menu",
    "run": lambda: mainMenu()
  }
}

api_dict = {
  0: {
    "name": "Exit to Main Menu",
    "run": lambda: mainMenu()
  }
}

extra_dict = {
  0: {
    "name": "Exit to Main Menu",
    "run": lambda: mainMenu()
  }
}

email_dict = {
  0: {
    "name": "Exit to Main Menu",
    "run": lambda: mainMenu()
  }
}

def mainMenu():
  print("\n ------------------------------------ ")
  print("           S O C P U P P E T          ")
  print(" ------------------------------------ ")
  print(" What would you like to do? ")
  print("\n OPTION 1: Sanitize URL")
  print(" OPTION 2: Reputation Check")
  print(" OPTION 3: Decoders (PP, URL, SafeLinks) ")
  print(" OPTION 4: Email Tools ")
  print(" OPTION 5: API Tools (require API keys)")
  print(" OPTION 6: Lookup Tools")
  print(" OPTION 7: Extra (Free online lookups and tools)")
  print("\n OPTION 0: Exit Tool")
  val = int(input(">> "))
  if val not in mainMenu_dict:
    print("Invalid value specified.")
    mainMenu()
  else:
    mainMenu_dict[val]()
      
def decoderMenu():
  print("\n --------------------------------- ")
  print("           D E C O D E R S        ")
  print(" --------------------------------- ")
  print(" What would you like to do? \n")
  for item in decoders_dict.keys():
    if item == 0:
      continue
    print(f" OPTION {item}: {decoders_dict[item]['name']}")
  print("\n OPTION 0: Exit to Main Menu")
  val = int(input(">> "))
  if val not in decoders_dict:
    print("Invalid value specified")
    decoderMenu()
  else:
    decoders_dict[val]['run']()

def emailMenu():
  print("\n ------------------------------------- ")
  print("         E M A I L    T O O L S        ")
  print(" ------------------------------------- ")
  print(" What would you like to do? \n")
  for item in email_dict.keys():
    if item == 0:
      continue
    print(f" OPTION {item}: {email_dict[item]['name']}")
  print("\n OPTION 0: Exit to Main Menu")
  val = int(input(">> "))
  if val not in email_dict:
    print("Invalid value specified")
    emailMenu()
  else:
    email_dict[val]['run']()

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
  val = int(input(">> "))
  if val not in api_dict:
    print("Invalid value specified")
    apiMenu()
  else:
    api_dict[val]['run']()

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
  val = int(input(">> "))
  if val not in lookups_dict:
    print("Invalid value specified")
    lookupsMenu()
  else:
    lookups_dict[val]['run']()

def extraMenu():
  print("\n ------------------------------ ")
  print("           E X T R A        ")
  print(" ------------------------------ ")
  print(" What would you like to do? \n")
  for item in extra_dict.keys():
    if item == 0:
      continue
    print(f" OPTION {item}: {extra_dict[item]['name']}")
  print("\n OPTION 0: Exit to Main Menu")
  val = int(input(">> "))
  if val not in extra_dict:
    print("Invalid value specified")
    extraMenu()
  else:
    extra_dict[val]['run']()


# TODO: Recommend refactoring this to something more simplified. Lots of repeating values.
def importModules():
  print("Importing Modules")
  directory_path = os.path.dirname(os.path.abspath(__file__))
  directories = [os.path.join(directory_path, 'Plugins', 'Decoders'),
                 os.path.join(directory_path, 'Plugins', 'Email'),
                 os.path.join(directory_path, 'Plugins', 'API'),
                 os.path.join(directory_path, 'Plugins', 'Extra'),
                 os.path.join(directory_path, 'Plugins', 'Lookups')]
  
  for dir in directories:
    files = os.listdir(dir)
    if "__pycache__" in files:
      files.remove("__pycache__")
    
    if "__init__.py" in files:
      files.remove("__init__.py")

    for idx, file_name in enumerate(files):
      module_name = file_name.replace('.py', '')
      module_path = os.path.join(dir, file_name)

      if file_name.endswith('.py') and os.path.isfile(module_path) and module_name != "__init__":
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        module.__package__ = module_name

        for _, obj in inspect.getmembers(module):
          if inspect.isclass(obj) and issubclass(obj, Plugin) and obj != Plugin:
            item = {
              'name': module_name,
              'run': lambda obj=obj: obj().run()
            }
            if dir.endswith("Decoders"):
              decoders_dict[idx+1] = item
            elif dir.endswith("Email"):
              email_dict[idx+1] = item
            elif dir.endswith("API"):
              api_dict[idx+1] = item
            elif dir.endswith("Extra"):
              extra_dict[idx+1] = item
            elif dir.endswith("Lookups"):
              lookups_dict[idx+1] = item

if __name__ == "__main__":
  importModules()
  mainMenu()