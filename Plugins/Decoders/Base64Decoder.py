from Plugins import Plugin

import base64
import re

class Base64Decoder(Plugin.Plugin):
  def __init__(self, string: str = None, name = "Base64 Decoder"):
    super().__init__(name)
    self._string = string if string is not None else None

  def run(self):
    print("\n -------------------------------------- ")
    print("        B A S E 6 4  D E C O D E        ")
    print(" -------------------------------------- ")
    if self._string == None:
      self._string = str(input(" Enter Base64 String: ")).strip()

    try:
        b64 = str(base64.b64decode(self._string))
        a = re.split("'", b64)[1]
        print(" B64 String:     " + self._string)
        print(" Decoded String: " + a)
    except:
        print(' No Base64 Encoded String Found')