use std::io::{self, Write};

pub fn get_input(prompt: &str) -> String {
  let mut usr_input = String::new();
  print!("{}", prompt);
  io::stdout().flush().expect("Failed to flush stdout");

  io::stdin().read_line(&mut usr_input).expect("Failed to read input");
  let output = usr_input.trim().to_string();
  output
}