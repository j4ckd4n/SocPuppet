mod plugins;

use plugins::Plugin;
use plugins::url_sanitize::URLSanitize;

fn main() {
    let url_sani = URLSanitize::new();
    url_sani.run();
}
