from Plugins import Plugin

class Cisco7Decoder(Plugin.Plugin):
  def __init__(self, password: str = None, name: str = "Cisco 7 Decoder"):
    super().__init__(name)

    self._password = password.strip() if password is not None else None
    self._key = [0x64, 0x73, 0x66, 0x64, 0x3b, 0x6b, 0x66, 0x6f, 0x41,
           0x2c, 0x2e, 0x69, 0x79, 0x65, 0x77, 0x72, 0x6b, 0x6c,
           0x64, 0x4a, 0x4b, 0x44, 0x48, 0x53, 0x55, 0x42]
    
  def run(self):
    print("\n ------------------------------------------ ")
    print("           C I S C O 7 D E C O D E R        ")
    print(" ------------------------------------------ ")
    print("\tWARNING: May not be accurate.")

    if self._password == None:
      self._password = input('Enter Cisco Password 7: ').strip()
    
    try:
      index = int(self._password[:2], 16)

      pw_text = self._password[2:]
      pw_hex_values = [pw_text[start:start+2] for start in range(0, len(pw_text), 2)]

      # XOR those values against the key values, starting at the index, and convert to ASCII
      pw_chars = [chr(self._key[index+i] ^ int(pw_hex_values[i],16)) for i in range(0,len(pw_hex_values))]

      pw_plaintext = ''.join(pw_chars)
      print("Password: " + pw_plaintext)

    except Exception as e:
      print(e)