use super::Plugin;
use serde_json;
// TODO Replace deprecated code.
#[allow(deprecated)]
use base64::decode;

use crate::utils::get_input;

pub struct Base64Decoder {}

impl Plugin for Base64Decoder {
  const NAME: &'static str = "Base64 Decoder";
  fn new() -> Self { Self {} }

  fn perform_lookup(&self, value: &str) -> Result<serde_json::Value, String> {
    let decoded_str = Self::b64_decode(value);
    Ok(serde_json::json!({"result": "decoded", "value": decoded_str}))
  }

  fn run(&self) {
    println!("Base64 Decoder");

    let input = get_input("Enter Base64 String: ");
    match self.perform_lookup(&input) {
      Ok(result) => println!("\n{}", result),
      Err(error) => eprintln!("Error: {}", error)
    }
  }

  fn get_name(&self) -> &str {
    return Self::NAME;
  }
}

#[allow(deprecated)]
impl Base64Decoder {
  fn b64_decode(val: &str) -> String {
    let decoded_bytes = decode(val).unwrap();
    let decoded_str = String::from_utf8(decoded_bytes).unwrap();
    decoded_str
  }
}