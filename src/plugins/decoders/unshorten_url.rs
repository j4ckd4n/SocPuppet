use super::Plugin;
use serde_json;
use reqwest;

use crate::utils::get_input;

pub struct UnshortenUrl {}

impl Plugin for UnshortenUrl {
  const NAME: &'static str = "Unshorten URL";

  fn new() -> Self {
    Self {}
  }

  fn perform_lookup(&self, value: &str) -> Result<serde_json::Value, String> {
    let url = format!("https://unshorten.me/s/{}", value);
    let response = reqwest::blocking::get(&url).unwrap();

    if response.status() == reqwest::StatusCode::OK {
      let body = response.text().unwrap();
      Ok(serde_json::json!({"status": "complete", "data": body}))
    } else {
      Err(String::from("query to urlshorten.me failed"))
    }
  }

  fn run(&self) {
    println!("{}", Self::NAME);
  
    let usr_in = get_input("Enter URL to decode: ");
    match self.perform_lookup(&usr_in.trim()) {
      Ok(result) => println!("\n{}", result),
      Err(error) => eprintln!("Error: {}", error)
    }
  }
}