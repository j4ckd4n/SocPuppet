use super::Plugin;
use serde_json;
use std::io::{self, Write};

pub struct URLSanitize {}

impl Plugin for URLSanitize {
  const NAME: &'static str = "URL Sanitize";
  fn new() -> Self {Self {}}

  fn perform_lookup(&self, value: &str) -> Result<serde_json::Value, String> {
    let sanitized_url = Self::sanitize_url(value);
    Ok(serde_json::json!({"result": "sanitized", "value": sanitized_url}))
  }

  fn run(&self) {
    println!("\n --------------------------------- ");
    println!(" U R L   S A N I T I Z E   T O O L ");
    println!(" --------------------------------- ");

    let mut input_url = String::new();
    print!("Enter URL to sanitize: ");
    io::stdout().flush().expect("Failed to flush stdio");
    
    io::stdin().read_line(&mut input_url).expect("Failed to read input");
    let input_url = input_url.trim();
    match self.perform_lookup(input_url) {
      Ok(result) => println!("\n{}", result),
      Err(error) => eprintln!("Error: {}", error),
    }
  }

  fn get_name(&self) -> &str {
    return Self::NAME;
  }
}

impl URLSanitize {
  fn sanitize_url(url: &str) -> String {
    let sanitized_url = url.replace(".", "[.]").replace("http://", "hxxp://").replace("https://", "hxxps://");
    sanitized_url
  }
}