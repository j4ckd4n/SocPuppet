use super::Plugin;
use serde::{Deserialize, Serialize};
use serde_json;

use crate::utils::get_input;

#[derive(Deserialize, Serialize, Debug)]
struct Response {
  success: bool,
  data: Vec<Reputation>
}

#[derive(Deserialize, Serialize, Debug)]
struct Reputation {
  description: Option<String>,
  created_date: String,
  data: String,
  data_type: String,
  derived: Option<String>,
  derived_type: String,
  source: String,
  source_url: Option<String>
}

pub struct InQuestLookup {}

impl Plugin for InQuestLookup {
  const NAME: &'static str = "InQuest Lookup";

  fn new() -> Self {
    Self {}
  }

  fn perform_lookup(&self, value: &str) -> Result<serde_json::Value, String> {
    let url = format!("https://labs.inquest.net/api/repdb/search?keyword={}", value);
    let client = reqwest::blocking::Client::new();
    let mut request_builder = client.get(url);
    request_builder = request_builder.header(reqwest::header::USER_AGENT, "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36");

    let res = request_builder.send().unwrap();

    if res.status() == reqwest::StatusCode::OK {
      let body = res.text().unwrap();
      let parsed: Response = serde_json::from_str(&body).map_err(|e| e.to_string())?;
      Ok(serde_json::json!(parsed))
    } else {
      Err(String::from("query to labs.inquest.net failed"))
    }
  }

  fn run(&self) {
    println!("{}", Self::NAME);

    let usr_in = get_input("Enter IP to lookup: ");
    match self.perform_lookup(&usr_in.trim()) {
      Ok(result) => println!("\n{}", result),
      Err(error) => eprintln!("Error: {}", error)
    }   
  }
}