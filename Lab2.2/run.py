from flask import Flask
from flask import request
from flask import jsonify
import glob
import re
import os


ip_and_hostnames = {}
app = Flask(__name__)


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
