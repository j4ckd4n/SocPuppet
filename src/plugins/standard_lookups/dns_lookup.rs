use super::Plugin;
use std::net::{IpAddr, ToSocketAddrs};
use std::collections::HashMap;

use crate::utils::get_input;

pub struct DNSLookup {}

impl Plugin for DNSLookup {
  const NAME: &'static str = "DNS Lookup";

  fn new() -> Self {
    Self {}
  }

  fn perform_lookup(&self, value: &str) -> Result<serde_json::Value, String> {
    let dns = value.trim_start_matches("http://").trim_start_matches("https://").trim();
    let default_port = 80;

    let dns_with_port = format!("{}:{}", dns, default_port);

    match dns_with_port.to_socket_addrs() {
      Ok(socket_addrs) => {
        let mut dns_resolution: Vec<String> = Vec::new();
        for socket_addr in socket_addrs {
          if let IpAddr::V4(ipv4) = socket_addr.ip() {
            dns_resolution.push(ipv4.to_string());
          } else if let IpAddr::V6(ipv6) = socket_addr.ip() {
            dns_resolution.push(ipv6.to_string());
          }
        }

        Ok(serde_json::json!({
          "status": "complete",
          "dns_resolution": dns_resolution
        }))
      }
      Err(error) => {
        println!("{}", error);
        Err(String::from("DNS resolution failed"))
      }
    }
  }

  fn run(&self) {
    println!("{}", Self::NAME);

    let usr_in = get_input("Enter domain to resolve: ");
    match self.perform_lookup(&usr_in.trim()) {
      Ok(result) => println!("\n{}", result),
      Err(error) => eprintln!("Error: {}", error)
    }
  }
}