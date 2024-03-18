import glob
import os
import re
import ipaddress


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
    with open(file, encoding="utf-8") as f:
        result = set()
        for line in f:
            if ip_tuple := is_having_ip(line):
                result.add(ipaddress.IPv4Interface(ip_tuple))

        print(f"В файле {file} содержатся следующие адреса:")
        # print(*sorted(result), sep="\n", end="\n==================\n")
        [print(i.ip, i.netmask) for i in sorted(result)]
        print("==================")
        print(f"Всего {len(result)} шт.", end="\n\n")

