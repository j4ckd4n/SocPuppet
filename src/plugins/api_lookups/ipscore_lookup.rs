use super::Plugin;
use serde_json;
use serde::{Deserialize, Serialize};

use crate::utils::get_input;

#[derive(Debug, Deserialize, Serialize)]
struct IPInfo {
    ip: String,
    status: bool,
    useragent: String,
    geoip1: GeoIP,
    geoip2: GeoIP,
    blacklists: Blacklists,
    isp: String,
    org: String,
    asn: String
}

#[derive(Debug, Deserialize, Serialize)]
struct GeoIP {
    country: String,
    countrycode: String,
    region: String,
    city: String,
    zip: String,
    lat: f32,
    lon: f32,
    timezone: String
}

#[derive(Debug, Deserialize, Serialize)]
struct Blacklists {
    spamhaus: String,
    sorbs: String,
    spamcop: String,
    southkoreannbl: String,
    barracuda: String
}

pub struct IPScoreLookup {}

impl Plugin for IPScoreLookup {
    const NAME: &'static str = "IP-Score Lookup";

    fn new() -> Self {
      Self {}
    }

    fn perform_lookup(&self, value: &str) -> Result<serde_json::Value, String> {
      let url = String::from("https://ip-score.com/fulljson");
      let client = reqwest::blocking::Client::new();
      let response = client.get(url).body(format!("ip={}", value))
        .header(reqwest::header::USER_AGENT, "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36")
        .send().unwrap();

      if response.status() == reqwest::StatusCode::OK {
        let body = response.text().unwrap();
        let parsed_response: IPInfo = serde_json::from_str(&body).map_err(|e| e.to_string())?;
        Ok(serde_json::json!({"status": "complete", "ipinfo": parsed_response}))
      } else {
        Err(String::from("query to ip-score.com failed"))
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