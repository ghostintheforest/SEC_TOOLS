##GhOST##
# Subdomain Buster #
import requests
from concurrent.futures import ThreadPoolExecutor

# Define the target
target_url = "soccer.htb"

header = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'}

# Open the wordlist file
with open('/home/ghost/Downloads/dnscan/subdomains-10000.txt', 'r') as wordlist_file:
    # Read it
    raw_response = wordlist_file.read()
    # Split it into a list
    wordlist = raw_response.splitlines()

# Define a function to send requests
def send_request(word):
    # Construct the test URL
    test_url = 'http://' + word + "." + target_url  # Make the request
    try:
        response = requests.get(test_url,headers=header, timeout=5)
        if response.status_code == 200:
            print("[+] Discovered subdomain --> " + test_url)
            print("    Response Content: ")
            print(response.content)
    except requests.ConnectionError:
        pass

# Create a ThreadPoolExecutor #
with ThreadPoolExecutor(max_workers=40) as executor:
    # Submit tasks to the pool
    for word in wordlist:
        executor.submit(send_request, word)
