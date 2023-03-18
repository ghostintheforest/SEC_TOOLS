##GhOST##
# CLI subdomain buster #
import requests
import argparse
from concurrent.futures import ThreadPoolExecutor

parser = argparse.ArgumentParser(description='Subdomain crawling: -w for wordlist, -u for url')

header = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'}

parser.add_argument('-u', '--url', help='Enter the target URL', required=True)
parser.add_argument('-w', '--wordlist', help='Enter the wordlist', required=True)

args = parser.parse_args()

with open(args.wordlist, 'r') as wordlist_file:
    raw_response = wordlist_file.read()
    wordlist = raw_response.splitlines()

# Define a function to send requests #
def send_request(word):
    test_url = args.url + "/" + word
    try:
        response = requests.get(test_url,headers=header, timeout=5)
        if response.status_code == 200:
            print("[+] Discovered subdomain --> " + test_url)
            print("    Response Content: ")
            print(response.content)
    except requests.ConnectionError:
        pass

# Create a ThreadPoolExecutor #
with ThreadPoolExecutor(max_workers=10) as executor:
    for word in wordlist:
        executor.submit(send_request, word)
