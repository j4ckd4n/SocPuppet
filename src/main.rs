mod plugins;
mod utils;

use plugins::Plugin;
use crate::plugins::decoders::url_decoder::URLDecode;

fn main() {
    let url_sani = URLDecode::new();
    url_sani.run();
}
