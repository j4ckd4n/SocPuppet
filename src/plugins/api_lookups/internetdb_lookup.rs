use super::Plugin;
use serde_json;
use serde::{Deserialize, Serialize};

use crate::utils::get_input;

#[derive(Deserialize, Serialize, Debug)]
struct Host {
  cpes: Vec<String>,
  hostnames: Vec<String>,
  ip: String,
  ports: Vec<i32>,
  tags: Vec<String>,
  vulns: Vec<String>
}

pub struct InternetDBLookup {}

impl Plugin for InternetDBLookup {
  const NAME: &'static str = "InternetDB Lookup";

  fn new() -> Self {
    Self {  }
  }

  fn perform_lookup(&self, value: &str) -> Result<serde_json::Value, String> {
    let url = format!("https://internetdb.shodan.io/{}", value);
    let response = reqwest::blocking::get(&url).unwrap();

    if response.status() == reqwest::StatusCode::OK {
      let body = response.text().unwrap();
      let parsed_response: Host = serde_json::from_str(&body).map_err(|e| e.to_string())?;
      Ok(serde_json::json!({"status": "complete", "host": parsed_response}))
    } else {
      Err(String::from("query to internetdb.shodan.io failed"))
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