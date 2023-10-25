from . import Base64Decoder, Cisco7Decoder, ProofPointDecoder, SafeLinksDecoder, UnShortenURL, URLDecoder

decoders_dict = {
  0: {
    "name": "Exit to Main Menu",
    "run": 0
  },
  1: {
    "name": "ProofPoint Link Decoder",
    "run": lambda: ProofPointDecoder.ProofPointDecoder().run()
  },
  2: {
    "name": "Microsoft Safe Links Decoder",
    "run": lambda: SafeLinksDecoder.SafeLinksDecoder().run()
  },
  3: {
    "name": "Base64 Decoder",
    "run": lambda: Base64Decoder.Base64Decoder().run()
  },
  5: {
    "name": "Unshorten URL",
    "run": lambda: UnShortenURL.UnShortenURL().run()
  },
  6: {
    "name": "URL Decoder",
    "run": lambda: URLDecoder.URLDecoder().run()
  },
  7: {
    "name": "Cisco7 Decoder",
    "run": lambda: Cisco7Decoder.Cisco7Decoder().run()
  },
}

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
  try:
    val = int(input(">> "))
    if val not in decoders_dict:
      print("Invalid option specified")
      decoderMenu()
    elif val == 0:
      return
    else:
      decoders_dict[val]['run']()
  except ValueError:
    print("Invalid option specified")
    decoderMenu()