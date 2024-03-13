from pysnmp.hlapi import *

engine = SnmpEngine()
comm_data = CommunityData("public", mpModel=0)
transport = UdpTransportTarget(("10.31.70.209", 161))
context_data = ContextData()
snmp_version = ObjectIdentity("SNMPv2-MIB", "sysDescr", 0)
snmp_interfaces = ObjectIdentity("1.3.6.1.2.1.2.2.1.2")

result = getCmd(
    engine,
    comm_data,
    transport,
    context_data,
    ObjectType(snmp_version)
)

result2 = nextCmd(
    SnmpEngine(),
    CommunityData('public', mpModel=0),
    UdpTransportTarget(('10.31.70.209', 161)),
    ContextData(),
    ObjectType(snmp_interfaces),
    lexicographicMode=False
)

for elem in result:
    [print(x) for x in elem[3]]
else:
    print()

for elem in result2:
    # [print(x) for x in elem[3]]
    errorIndication, errorStatus, errorIndex, varBinds = elem
    [print(x) for x in varBinds]
else:
    print()