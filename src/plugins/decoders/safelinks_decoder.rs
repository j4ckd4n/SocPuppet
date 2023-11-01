use super::Plugin;
use serde_json;
use urlencoding::decode;

use crate::utils::get_input;

pub struct SafeLinksDecode {}

impl Plugin for SafeLinksDecode {
    const NAME: &'static str = "SafeLinks Decoder";

    fn new() -> Self {
        Self {}
    }

    fn perform_lookup(&self, value: &str) -> Result<serde_json::Value, String> {
        let decoded_value = Self::decode_url(value);
        Ok(serde_json::json!({ "result": "decoded", "value": decoded_value}))
    }

    fn run(&self) {
        println!("SafeLinks Decoder");

        let usr_in = get_input("Enter URL: ");
        match self.perform_lookup(&usr_in) {
          Ok(result) => println!("\n{}", result),
          Err(error) => eprintln!("Error: {}", error)
        }
    }
}

impl SafeLinksDecode {
  fn decode_url(url: &str) -> String {
    let mut dc_url = decode(url).expect("UTF-8").to_string();
    dc_url = dc_url.replace("https://nam02.safelinks.protection.outlook.com/?url=", "");
    dc_url
  }
}