from flask import Flask
from flask import request
from flask import jsonify
import glob
import re
import os
import requests

ip_and_hostnames = {}
app = Flask(__name__)
host_ip = "10.31.70.209"
login = "restapi"
password = "j0sg1280-7@"
api_url = "/restconf/data/Cisco-IOS-XE-process-memory-oper:memory-usage-processes"
headers = {
    "accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/page1')
def page1():
    return "Если вы это читаете, вы что-то знаете :)"


@app.route('/test', methods=["GET"])
def test():
    return jsonify({'ip': request.remote_addr, "path": request.path}), 200


@app.route('/config')
def config():
    return jsonify(ip_and_hostnames)


# http://127.0.0.1:5000/memory
# http://127.0.0.1:5000/memory/3
# http://127.0.0.1:5000/memory/15
@app.route('/memory', defaults={'quantity': 10})
@app.route('/memory/<quantity>')
def memory(quantity):
    response = requests.get("https://" + host_ip + api_url, headers=headers, auth=(login, password), verify=False).json()
    out = response['Cisco-IOS-XE-process-memory-oper:memory-usage-processes']['memory-usage-process']
    out = sorted(out, key=lambda d: int(d["allocated-memory"]), reverse=True)[:int(quantity)]

    # Print to console
    for idx, item in enumerate(out, 1):
        print(f"{str(idx).rjust(3)}) {item['name'].ljust(35, '.')} {item['allocated-memory']}")

    return jsonify(out)


@app.route('/config/<hostname>')
def ip_info(hostname):
    for filename in ip_and_hostnames.keys():
        print(ip_and_hostnames[filename]['hostname'])
        if ip_and_hostnames[filename]['hostname'] == hostname:
            return jsonify(ip_and_hostnames[filename]['addresses'])
    return jsonify("Nothing found")


if __name__ == '__main__':

    def is_having_host(string):
        pattern_ip_with_mask = r"^hostname (.*)"
        if check_result := re.match(pattern_ip_with_mask, string.strip()):
            return check_result.groups()
        else:
            return None


    def is_having_ip(string):
        pattern_ip_with_mask = r"^ip address ([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}) ([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})"
        pattern_ip_wo_mask = r"^ip address ([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})"
        if check_result := re.match(pattern_ip_with_mask, string.strip()):
            return check_result.groups()
        elif check_result := re.match(pattern_ip_wo_mask, string.strip()):
            return check_result.groups()
        else:
            return None


    for file in glob.iglob(os.path.join(os.getcwd(), "config_files", "*.log")):
        current_file_name = os.path.basename(file)
        ip_and_hostnames[current_file_name] = {}
        ip_and_hostnames[current_file_name]['addresses'] = []
        ip_and_hostnames[current_file_name]['hostname'] = []
        with open(file, encoding="utf-8") as f:
            for line in f:
                if host := is_having_host(line):
                    ip_and_hostnames[current_file_name]['hostname'] = host[0]
                if ip := is_having_ip(line):
                    if len(ip) == 2:
                        ip_and_hostnames[current_file_name]['addresses'].append({'ip': ip[0], 'mask': ip[1]})
                    else:
                        ip_and_hostnames[current_file_name]['addresses'].append({'ip': ip[0]})

    app.run(debug=True)
