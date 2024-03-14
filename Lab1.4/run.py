from IPv4RandomNetwork import IPv4RandomNetwork

result = []

for _ in range(1, 51):
    while True:
        ip = IPv4RandomNetwork()
        if not ip.network_address.is_private:
            result.append(ip)
            break

result = sorted(result, key=lambda x: (x.netmask, x.network_address))
print(*result, sep="\n")
