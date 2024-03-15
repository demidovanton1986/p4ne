import glob
import os

for file in glob.iglob(os.path.join(os.getcwd(), "config_files", "*.log")):
    with open(file, encoding="utf-8") as f:
        result = set()
        for line in f:
            line = line.split("ip address")[-1].strip().rstrip("sub").rstrip() if "ip address" in line else ""
            if line:
                result.add(line)
        print(f"В файле {file} содержатся следующие адреса:")
        print(*result, sep="\n", end="\n\n")
