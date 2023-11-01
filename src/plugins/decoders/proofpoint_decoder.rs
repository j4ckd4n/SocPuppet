use super::Plugin;
use serde_json;
use regex::Regex;
use urlencoding::decode;

use crate::utils::get_input;

pub struct ProofPointDecode {
  url_re: Regex,
  url_re_v3: Regex
}

impl Plugin for ProofPointDecode {
  const NAME: &'static str = "ProofPoint Decoder";

  fn new() -> Self {
    Self {
      url_re: Regex::new(r"https://urldefense.proofpoint.com/(v[0-9])/").unwrap(),
      url_re_v3: Regex::new(r"urldefense.com/(v3)/").unwrap()
    }
  }

  fn perform_lookup(&self, value: &str) -> Result<serde_json::Value, String> {
    let match_result = self.url_re.find(value);
    let matchv3_result = self.url_re_v3.find(value);

    let mut decoded_links: Vec<String> = Vec::new();

    if let Some(m) = match_result {
      println!("{}", m.as_str());
      if String::from(m.as_str()).contains("v1") {
        let mut links = Self::decodev1(value);
        for item in &links {
          println!("\nDecoded Link: {}", item);
        }
        decoded_links.append(&mut links);
      } else if String::from(m.as_str()).contains("v2") {
        let mut links = Self::decodev2(value);
        for item in &links {
          println!("\nDecoded Link: {}", item);
        }
        decoded_links.append(&mut links);
      }
    }

    if let Some(m) = matchv3_result {
      if m.as_str() == "v3" {
        let mut links = Self::decodev3(value);
        for item in &links {
          println!("\nDecoded Link: {}", item);
        }
        decoded_links.append(&mut links);
      }
    }

    Ok(serde_json::json!({"status": "complete", "decoded_links": decoded_links}))
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

impl ProofPointDecode {
  fn decodev1(rewrittenurl: &str) -> Vec<String> {
    let re: Regex = Regex::new(r"u=(.+?)&k=").unwrap();
    let mut links_found_list: Vec<String> = Vec::new();

    if let Some(caputres) = re.captures(rewrittenurl) {
      if let Some(encoded_url) = caputres.get(1) {
        let url_encoded_url = encoded_url.as_str();
        if let Ok(html_encoded_url) = decode(url_encoded_url) {
          let url = html_encoded_url.replace("http://", "");
          println!("{}", url);
          if !links_found_list.contains(&url) {
            links_found_list.push(url);
          }
        }
      }
    } else {
      println!("No captures for v1 found.")
    }

    links_found_list
  }

  fn decodev2(rewrittenurl: &str) -> Vec<String> {
    let re: Regex = Regex::new(r"u=(.+?)&[dc]=").unwrap();
    let mut links_found_list: Vec<String> = Vec::new();
  
    if let Some(captures) = re.captures(rewrittenurl) {
      if let Some(special_encoded_url) = captures.get(1) {
        let trans = special_encoded_url.as_str().replace("-", "%").replace("_", "/");
        if let Ok(url_encoded_url) = decode(&trans) {
          let html_encoded_url = url_encoded_url.replace("http://", "");
          if let Ok(url) = decode(&html_encoded_url) {
            println!("{}", url);
            if !links_found_list.contains(&url.to_string()) {
              links_found_list.push(url.to_string());
            }
          }
        }
      }
    } else { 
      println!("No captures for v2 found.")
    }
  
    links_found_list
  }

  fn decodev3(rewrittenurl: &str) -> Vec<String> {
    let re: Regex = Regex::new("v3/__(?P<url>.+?)__;").unwrap();
    let mut links_found_list: Vec<String> = Vec::new();

    if let Some(captures) = re.captures(rewrittenurl) {
      if let Some(url) = captures.name("url") {
        let mut url = url.as_str().to_string();
        if Regex::new(r"\*(\*.)?").unwrap().is_match(&url) {
          url = url.replace("*", "+");
          println!("{}", url);
          if !links_found_list.contains(&url) {
            links_found_list.push(url);
          }
        }
      }
    } else {
      println!("No captures for v3 found.")
    }
    
    links_found_list
  }
}