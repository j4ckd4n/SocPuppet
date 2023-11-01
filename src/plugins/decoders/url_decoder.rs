use super::Plugin;
use serde_json;
use urlencoding::decode;

use crate::utils::get_input;

pub struct URLDecode {}

impl Plugin for URLDecode {
  const NAME: &'static str = "URL Decode";
  fn new() -> Self {
     Self{}
  }

  fn perform_lookup(&self, value: &str) -> Result<serde_json::Value, String> {
    let decoded_val = Self::decode_url(value);
    Ok(serde_json::json!({"result": "decoded", "value": decoded_val}))
  }

  fn run(&self) {
    println!("URL Decoder");

    let usr_in = get_input("Enter URL to decode: ");
    match self.perform_lookup(&usr_in) {
      Ok(result) => println!("\n{}", result),
      Err(error) => eprintln!("Error: {}", error)
    }

  }

  fn get_name(&self) -> &str {
      return Self::NAME;
  }
}

impl URLDecode {
  fn decode_url(val: &str) -> String {
    let decoded_val = decode(val).expect("UTF-8");
    decoded_val.into_owned()
  }
}