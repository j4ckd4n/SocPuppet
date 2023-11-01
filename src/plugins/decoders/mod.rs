use std::collections::BTreeMap;

use crate::plugins::Plugin;
use crate::utils::get_input;

pub(crate) mod base64_decoder;
pub(crate) mod url_decoder;
pub(crate) mod safelinks_decoder;
pub(crate) mod proofpoint_decoder;

fn decoders_menu_dict() -> BTreeMap<i32, (String, Box<dyn Fn()>)> {
  let mut map: BTreeMap<i32, (String, Box<dyn Fn()>)> = BTreeMap::new();
  map.insert(0, ("Exit menu".to_string(), Box::new(|| {})));
  map.insert(1, ("Base64 Decoder".to_string(), Box::new(|| base64_decoder::Base64Decoder::new().run())));
  map.insert(2, ("SafeLinks Decoder".to_string(), Box::new(|| safelinks_decoder::SafeLinksDecode::new().run())));
  map.insert(3, ("ProofPoint Decoder".to_string(), Box::new(|| proofpoint_decoder::ProofPointDecode::new().run())));

  map
}

pub fn decoder_menu() {
  println!("\n------------------------");
  println!("     D E C O D E R S     ");
  println!("-------------------------");
  println!(" What would you like to do? \n");

  for (item, (name, _)) in decoders_menu_dict().iter() {
    if *item == 0 {
      continue;
    }
    println!(" OPTION {}: {}", item, name);
  }
  println!("\n OPTION 0: Exit to Main Menu");

  let input = get_input("> ");

  match input.parse() {
    Ok(val) => match decoders_menu_dict().get(&val) {
      Some(decoder) => (decoder.1)(),
      None if val == 0 => return,
      _ => println!("Invalid option specified")
    },
    Err(_) => println!("Invalid option specified")
  }

}