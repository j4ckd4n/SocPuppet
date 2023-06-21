from Plugins import Plugin

import os, requests, time

class URLScanIO(Plugin.Plugin):
  def __init__(self, url: str = None, name: str = 'URLScanIO'):
    super().__init__(name)
    self._url = url
    self._api_key = os.getenv("URLSCAN_IO_API_KEY")

  def run(self):
    if self._api_key == None:
      print("No API Key found. Define it as an environment variable 'URLSCAN_IO_API_KEY'.")
      return

    print("\n --------------------------------- ")
    print("        U R L S C A N . I O        ")
    print(" --------------------------------- ")
    if self._url == None:
      self._url = input('\nEnter url:').strip()
    
    try:
      type_prompt = str(input('\nSet scan visibility to Public? \nType "1" for Public, "2" for Unlisted, or "0" to skip: '))
      if type_prompt == '1':
        scan_type = 'public'
      elif type_prompt == "2":
        scan_type = 'unlisted'
      else:
        print("Exiting...")
        return
    except:
      print('Please make a selection again.. ')

    headers = {
      'Content-Type': 'application/json',
      'API-Key': self._api_key,
    }

    response = requests.post('https://urlscan.io/api/v1/scan/', headers=headers, data='{"url": "%s", "visibility": "%s"}' % (self._url, scan_type)).json()

    try:
      if 'successful' in response['message']:
        print('\nNow scanning %s. Check back in around 1 minute.' % self._url)
        uuid_variable = str(response['uuid']) # uuid, this is the factor that identifies the scan
        time.sleep(45) # sleep for 45 seconds. The scan takes awhile, if we try to retrieve the scan too soon, it will return an error.
        scan_results = requests.get('https://urlscan.io/api/v1/result/%s/' % uuid_variable).json() # retrieving the scan using the uuid for this scan

        task_url = scan_results['task']['url']
        verdicts_overall_score = scan_results['verdicts']['overall']['score']
        verdicts_overall_malicious = scan_results['verdicts']['overall']['malicious']
        task_report_URL = scan_results['task']['reportURL']

        print("\nurlscan.io Report:")
        print("\nURL: " + task_url)
        print("\nOverall Verdict: " + str(verdicts_overall_score))
        print("Malicious: " + str(verdicts_overall_malicious))
        print("urlscan.io: " + str(scan_results['verdicts']['urlscan']['score']))
        print("Report URL: %s" % scan_results['task']['reportURL'])
        print("ScreenShot URL: %s" % scan_results['task']['screenshotURL'])
        if scan_results['verdicts']['urlscan']['malicious']:
          print("Malicious: " + str(scan_results['verdicts']['urlscan']['malicious'])) # True
        if scan_results['verdicts']['urlscan']['categories']:
          print("Categories: ")
        for line in scan_results['verdicts']['urlscan']['categories']:
          print("\t"+ str(line)) # phishing
        for line in scan_results['verdicts']['engines']['verdicts']:
          print(str(line['engine']) + " score: " + str(line['score'])) # googlesafebrowsing
          print("Categories: ")
          for item in line['categories']:
            print("\t" + item) # social_engineering
          print("\nSee full report for more details: " + str(task_report_URL))
          print('')
      else:
        print("Scan did not succeed, reason: %s\n\tDescription: %s" % (response['message'], response['description']))
    except Exception as e:
      print(e)
      print('Error reaching URLScan.io')
