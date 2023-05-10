from Plugins.Plugin import Plugin

import importlib.util
import os
import inspect

mainMenu_dict = {
  0: lambda: exit(0),
  1: lambda: decoderMenu(),
  2: lambda: dnsMenu(),
  3: lambda: apiMenu(),
  4: lambda: extraMenu()
}

decoders_dict = {
  0: {
    "name": "Exit to Main Menu",
    "run": lambda: mainMenu()
  }
}

dns_dict = {
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

def mainMenu():
  print("\n ------------------------------------- ")
  print("\n           S  O  O  T  Y  V 2          ")
  print("\n ------------------------------------- ")
  print(" What would you like to do? ")
  print("\n OPTION 1: Decoders (PP, URL, SafeLinks) ")
  print(" OPTION 2: DNS Tools ")
  print(" OPTION 3: API Tools (require API keys)")
  print(" OPTION 4: Extra (Free online lookups and tools)")
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

def dnsMenu():
  print("\n --------------------------------- ")
  print("         D N S    T O O L S        ")
  print(" --------------------------------- ")
  print(" What would you like to do? \n")
  for item in dns_dict.keys():
    if item == 0:
      continue
    print(f" OPTION {item}: {dns_dict[item]['name']}")
  print("\n OPTION 0: Exit to Main Menu")
  val = int(input(">> "))
  if val not in dns_dict:
    print("Invalid value specified")
    dnsMenu()
  else:
    dns_dict[val]['run']()

def apiMenu():
  print("\n ------------------------------------ ")
  print("\n           A P I  T O O L S          ")
  print("\n ------------------------------------ ")
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

def importModules():
  print("Importing Modules")
  directory_path = os.path.dirname(os.path.abspath(__file__))
  directories = [os.path.join(directory_path, 'Plugins', 'Decoders'),
                 os.path.join(directory_path, 'Plugins', 'DNS'),
                 os.path.join(directory_path, 'Plugins', 'API'),
                 os.path.join(directory_path, 'Plugins', 'Extra')]
  
  for dir in directories:
    files = os.listdir(dir)

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
            elif dir.endswith("DNS"):
              dns_dict[idx+1] = item
            elif dir.endswith("API"):
              api_dict[idx+1] = item
            elif dir.endswith("Extra"):
              extra_dict[idx+1] = item

if __name__ == "__main__":
  importModules()
  mainMenu()