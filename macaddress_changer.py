##GhOST##
# Mac-Address Changer #
import subprocess
import sys
import argparse
import re 
import time
import random

# This gives you your wireless interface #
def get_interface():
    # Use iifconfig to see interfaces #
    result = subprocess.run(["ifconfig"], capture_output=True, text=True).stdout
    # Get all interfaces #
    interface_names = []
    for line in result.split("\n"):
        if ":" in line:
            interface_names.append(line.split()[0])

    for interface_name in interface_names:
        return interface_name
# Function to get current mac address #
def get_current_mac(interface):
    ifconfig_result = subprocess.run(["ifconfig", interface], capture_output=True, text=True).stdout
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address.")
# Function to change mac address #
def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_random_mac():
    mac = [ 0x00, 0x24, 0x81,
            random.randint(0x00, 0x7f),
            random.randint(0x00, 0xff),
            random.randint(0x00, 0xff) ]
    return ':'.join(map(lambda x: "%02x" % x, mac))

# Main function #
if __name__ == "__main__":
    print("GhOST Mac-Address Changer")
    interface = get_interface()
    print("Your interface is: " + interface)
    current_mac = get_current_mac(interface)
    print("Your current MAC is: " + str(current_mac))
    new_mac = get_random_mac()
    change_mac(interface, new_mac)
    current_mac = get_current_mac(interface)
    if current_mac == new_mac:
        print("[+] MAC address was successfully changed to " + current_mac)
    else:
        print("[-] MAC address did not get changed.")
        
    