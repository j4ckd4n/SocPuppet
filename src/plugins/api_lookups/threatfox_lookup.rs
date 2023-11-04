use super::Plugin;
use reqwest::{blocking::Request, Method};
use serde::{Deserialize, Serialize};
use serde_json::{self, json};

use crate::utils::get_input;

#[derive(Deserialize, Serialize, Debug)]
struct ThreatFox {
  query_status: String,
  data: Vec<IndicatorData>
}

#[derive(Deserialize, Serialize, Debug)]
struct IndicatorData {
  id: String,
  ioc: String,
  threat_type: String,
  threat_type_desc: String,
  ioc_type: String,
  ioc_type_desc: String,
  malware: String,
  malware_printable: String,
  malware_alias: String,
  malware_malpedia: String,
  confidence_level: u32,
  first_seen: String,
  last_seen: String,
  reference: String,
  reporter: String,
  tags: Vec<String>,
  malware_samples: Vec<MalwareSample>
}

#[derive(Deserialize, Serialize, Debug)]
struct MalwareSample {
  time_stamp: String,
  md5_hash: String,
  sha256_hash: String,
  malware_bazaar: String
}

#[derive(Serialize, Deserialize)]
struct ThreatFoxRequest {
  query: String,
  search_term: String,
}

pub struct ThreatFoxLookup {}

impl Plugin for ThreatFoxLookup {
  const NAME: &'static str = "ThreatFox Lookup";

  fn new() -> Self {
    Self {}
  }

  fn perform_lookup(&self, value: &str) -> Result<serde_json::Value, String> {
    let url = String::from("https://threatfox-api.abuse.ch/api/v1");

    let request_body = ThreatFoxRequest {
      query: "search_ioc".to_string(),
      search_term: value.to_string()
    };

    let json_body = json!(request_body).to_string();

    let client = reqwest::blocking::Client::new();
    
    let res = client.post(&url)
      .header(reqwest::header::USER_AGENT, "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36")
      .header(reqwest::header::CONTENT_TYPE, "application/json")
      .body(json_body).build().unwrap();

    let response = client.execute(res)
      .map_err(|e| e.to_string())?;

    if response.status() == reqwest::StatusCode::OK {
      let body = response.text().unwrap();
      let parsed: ThreatFox = serde_json::from_str(&body).map_err(|e| e.to_string())?;
      Ok(json!(parsed))
    } else {
      Err(String::from(response.text().unwrap()))
    }
  }

  fn run(&self) {
    println!("{}", Self::NAME);

    let usr_in = get_input("Enter an IoC to lookup: ");
    match self.perform_lookup(&usr_in.trim()) {
      Ok(result) => println!("\n{}", result),
      Err(error) => eprintln!("Error: {}", error)
    }
  }
}