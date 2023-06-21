from . import AnalyzeEmail

email_dict = {
  0: {
    "name": "Exit to Main Menu",
    "run": 0
  },
  1: {
    "name": "Analyze Email File",
    "run": lambda: AnalyzeEmail.AnalyzeEmail().run()
  }
}

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
  elif val == 0:
    return
  else:
    email_dict[val]['run']()