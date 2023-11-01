mod plugins;
mod utils;

use std::collections::BTreeMap;

use plugins::Plugin;
use crate::plugins::url_sanitize::URLSanitize;
use crate::plugins::decoders;

fn main_menu_dict() -> BTreeMap<i32, fn()> {
  let mut map: BTreeMap<i32, fn()> = BTreeMap::new();
  map.insert(0, || std::process::exit(0));
  map.insert(1, || URLSanitize::new().run());
  map.insert(2, || decoders::decoder_menu());
    
  map
}

fn main_menu() {
  println!("\n What would you like to do?");
  println!("\n OPTION 1: Sanitize URL");
  println!(" OPTION 2: Decoders (PP, URL, SafeLinks)");

  println!("\n OPTION 0: Exit");

  let input = utils::get_input("> ");
  match input.parse() {
    Ok(val) => match main_menu_dict().get(&val) {
      Some(func) => func(),
      None => eprintln!("Invalid value specified"),
    },
    Err(_) => println!("Invalid value specified")
  }
}

fn main() {
    loop {
      main_menu();
    }
}
