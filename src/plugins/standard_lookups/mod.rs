use std::collections::BTreeMap;

use crate::plugins::Plugin;
use crate::utils::get_input;

pub(crate) mod dns_lookup;

fn standard_lookups_menu_dict() -> BTreeMap<i32, (String, Box<dyn Fn()>)> {
  let mut map: BTreeMap<i32, (String, Box<dyn Fn()>)> = BTreeMap::new();
  
  map.insert(0, ("Exit menu".to_string(), Box::new(|| {})));
  map.insert(1, ("DNS Lookup".to_string(), Box::new(|| dns_lookup::DNSLookup::new().run())));

  map
}

pub fn standard_lookups_menu() {
  println!("\n-----------------------------");
  println!("       Standard Lookups       ");
  println!("------------------------------");
  println!(" What would you like to do? \n");

  for (item, (name, _)) in standard_lookups_menu_dict().iter() {
    if *item == 0 {
      continue;
    }
    println!(" OPTION {}: {}", item, name);
  }
  println!("\n OPTION 0: Exit to Main Menu");

  let input = get_input("> ");

  match input.parse() {
    Ok(val) => match standard_lookups_menu_dict().get(&val) {
      Some(lookup) => (lookup.1)(),
      None if val == 0 => return,
      _ => println!("Invalid option specified")
    },
    Err(_) => println!("Invalid option specified")
  }
}