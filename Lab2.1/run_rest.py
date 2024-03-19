import requests
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


headers = {"accept": "application/yang-data+json", "Content-Type": "application/yang-data+json"}
login = "restapi"
password = "j0sg1280-7@"
host_url = "https://10.31.70.209"
response = requests.get(
    host_url + "/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces",
    auth=(login, password),
    headers=headers,
    verify=False
)

for interface in response.json()["Cisco-IOS-XE-interfaces-oper:interfaces"]["interface"]:
    print(f'Interface: {interface["name"]}')
    print(f'Packets/bytes input: {interface["statistics"]["in-unicast-pkts"]} / {interface["statistics"]["in-octets"]}')
    print(f'Packets/bytes output: {interface["statistics"]["out-unicast-pkts"]} / {interface["statistics"]["out-octets"]}')
    print()
