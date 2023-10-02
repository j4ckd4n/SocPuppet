![Welcome](https://img.shields.io/badge/SocPuppet-Welcome!-red?style=for-the-badge&logo=appveyor)

![GitHub Last Commit](https://img.shields.io/github/last-commit/j4ckd4n/SocPuppet)
![GitHub issues](https://img.shields.io/github/issues-raw/j4ckd4n/SocPuppet)
![GitHub repo size](https://img.shields.io/github/repo-size/j4ckd4n/SocPuppet)


# Overview

SocPuppet is a tool developed with the task of aiding SOC analysts with automating part of their workflow. One of the goals of SocPuppet is to perform as many of the routine checks as possible, allowing the analyst more time to spend on deeper analysis within the same time-frame. Details for many of SocPuppet's features can be found below.

This tool is a fork of the [Sooty](https://github.com/TheresAFewConors/Sooty) tool developed by [TheresAFewConors](https://github.com/TheresAFewConors).

## Contents
 - [Current Features](#socpuppet-can-currently)
 - [Requirements & Installation](#requirements-and-installation)
 - [SocPuppetAI](#socpuppetai---experimental)
 - [Development](#development)
 - [Changelog](#changelog)
 - [Roadmap](#roadmap)

## SocPuppet can currently:
  - Sanitize URL's to be safe for sending emails.
  - Perform reverse DNS and DNS lookups.
  - Perform reputation checks:
    - Hashes:
      - [VirusTotal](https://www.virustotal.com/) - API Key Required
      - [Malware Bazzar](https://bazaar.abuse.ch/)
    - Domain and IP:
      - Reverse DNS
      - DNS Lookup
      - [ThreatFox](https://threatfox.abuse.ch/browse/)
      - [URLScan.io](https://urlscan.io/) - API Key Required
      - [InternetDB](https://internetdb.shodan.io/)
      - WhoIs
      - [GreyNoise](https://viz.greynoise.io/) - API Key Required
      - [Shodan](https://www.shodan.io/) - API Key Required
      - [IP-API](https://ip-api.com/)
      - [inQuest - Labs](https://labs.inquest.net/)
  - Decode:
    - ProofPoint URLs.
    - UTF-8 Encoded URLs.
    - Office SafeLink URLs.
    - Base64 Strings.
    - Cisco7 Passwords.
  - Email:
    - Analyze Email Information (Perform Reputation Checks)
  - Unshorten URL's that have been shortened by external services. (Limited to 10 requests per hour).
  - [Unfurl](https://github.com/obsidianforensics/unfurl) URLs via the CLI version of Unfurl.
  
```
└── Main Menu
   ├── Sanitize URL's for use in emails
   |  └── URL Sanitizing Tool
   ├── Reputation Check
   |  └── Perform a check against IPs, Domains, or Hashes
   ├── Decoders
   |   ├── ProofPoint Decoder
   |   ├── URL Decoder
   |   ├── Office Safelinks Decoder
   |   ├── URL Unshortener
   |   ├── Base 64 Decoder
   |   ├── Cisco Password 7 Decoder
   |   └── Unfurl URL
   ├── Email
   |   └── Analyze Email
   ├── API (Requires API keys)
   |   ├── URLScan.io lookup
   |   ├── VirusTotal lookup
   |   ├── GreyNoise lookup
   |   └── Shodan lookup
   ├── Lookup Tools
   |   ├── Bitcoin Address
   |   ├── Bitcoin Transaction Tracer
   |   ├── Reverse DNS Lookup
   |   ├── DNS Lookup
   |   └── WhoIs Lookup
   ├── Extra's
   |   ├── InternetDB (Free Shodan)
   |   ├── IP-API (IP Geo Location, rate limited without a key)
   |   ├── Malware Bazaar (Abuse.ch)
   |   ├── SocPuppetAI - Experimental, uses [GPT4All](https://github.com/nomic-ai/gpt4all)
   |   ├── inQuest (limited queries without API)
   |   └── ThreatFox
   └── Exit
```

---

## Requirements and Installation
  - [Python 3.x](https://www.python.org/)
  - Install all dependencies from the requirements.txt file. `pip install -r requirements.txt`
  - Launch the tool by navigating to the main directory, and executing with `python SocPuppet.py`, or simply `SocPuppet.py` 
  - Several API Keys are required to have full functionality with SocPuppet. However, it will still function without these keys, just without the added functionality they provide. Links are found below:
    - [VirusTotal API Key](https://developers.virustotal.com/reference)
    - [GreyNoise API Key](https://docs.greynoise.io/reference/get_v3-community-ip)
    - [URLScan.io API Key](https://urlscan.io/about-api/)
  - API keys are set via environment variables listed below:
    - GreyNoise - `GREYNOISE_API_KEY`
    - Shodan.io - `SHODAN_API_KEY`
    - URL Scan - `URLSCAN_IO_API_KEY`
    - VirusTotal - `VT_API_TOKEN`

## Launch with Docker
- docker build -t sooty . && docker run --rm -it sooty 
 
 <!-- - To use the Hash comparison with VirusTotal requires an [API key](https://developers.virustotal.com/reference), replace the key `VT_API_KEY` in the code with your own key. The tool will still function without this key, however this feature will not work.
 - To use the Reputation Checker with AbuseIPDB requires an [API Key](https://www.abuseipdb.com/api), replace the key `AB_API_KEY` in the code with your own key. The tool will still function without this key, however this feature will not work.
 - To use the URLScan.io checker function with URLScan requires an [API Key](https://urlscan.io/about-api/), replace the key `URLSCAN_IO_KEY` in the code with your own key. The tool will still function without this key, however this feature will not work. 
 - Use of the HaveIBeenPwned functionality requires an [API Key](https://haveibeenpwned.com/API/Key), replace the key `HIBP_API_KEY` in the code with your own key. The tool will still function without this key, however this feature will not work. -->

## SocPuppetAI - Experimental
This is an experimental implementation of [GPT4All](https://github.com/nomic-ai/gpt4all) by Nomic AI.

With the current implementation, the tool automatically attempts to download the `ggml-wizardLB-7B.q4_2` model. This particular model is based on Llama 7b and trained by Microsoft and Peking University. The `ggml-wizardLB-7B.q4_2` is 4GB in size and will take up 4GB of RAM during execution. During testing, I've observed that this model appears to been better a summarizing findings that other models supplied by the organziation. That said, you can check out available models on their [official](https://gpt4all.io/index.html) GPT4All website and use them here. You will have to modify the `self._gpt = gpt4all.GPT4all("ggml-wizardLM-7B.q4_2")` line of code to match the model you wish to use.

The AI runs completely on your CPU which may take some time to give you a response in comparison to ChatGPT.

> Due to this being a completely experimental model, you may or may not receive an expected output. In many cases, you may not even receive a response. That said

### Commands

> All commands must end with `eof` at this time, this does include the data you are pushing for the SocPuppet to analyse.

#### `clear_context`
This command will clear the context memory that is fed back into the AI model

#### `exit_gpt`
This command will exit the SocPuppetAI.

#### `show_context`
This command will give you the raw context array of what is being fed into the AI

## Development

### Want to contribute? Great!

#### Code Contributions
  - If you wish to work on a feature, leave a comment on the issue page and I will assign you to it.
  - Under the projects tab is a list of features that are waiting to be started / completed. 
  - All code modifications, enhancements or additions must be done through a pull request. 
  - Once reviewed and merged, contributors will be added to the ReadMe.

### Found a Bug? Show Me!

#### Bugs and Issues
  - If an issue / bug is found, please open a ticket in the issue tracker and use the bug report template. Fill in this template and include any additional relevant information.
  - If you wish to work on a known bug, leave a comment on the issue page and open a Pull Request to track progress. I will assign you to it.
  - If there is an issue with installation or usage, use the supplied template and I will respond ASAP.

## Changelog

Check the `CHANGELOG.md` file.

## Roadmap
This is an outline of what features *may* be coming in future versions. You can see the current SocPuppet project items on the [Projects](https://github.com/users/j4ckd4n/projects/2) site.

#### Version 1.2 - The Phishing Update
  - Scan email attachments for malicious content, macros, files, scan hashes, etc.
  - Ability to analyze an email, retrieve emails, urls and extract info from headers.
  - Extract IPs from body of an email.
  - Perform reputation checks on the sender of email and provide enriched information.

#### Version 1.3 - The Templating Update
  - Add dynamic email templates that generate based on SocPuppet's analysis.
  - Verify MX Records
  - Perform DKIM Verification

#### Version 1.4 - The PCAP Analysis Update
  - Add ability to analyze .pcap files and provide concise, enriched information.

#### Version 1.x - The Case Update
  - Add a 'New Case' Feature, allowing output of the tool to be output to a txt file.

