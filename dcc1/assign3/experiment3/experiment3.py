
from scapy.all import IP, ICMP, Raw, sr1


DESTINATION = "8.8.8.8"

MAX_TTL = 20

TIMEOUT = 2
print("\nICMP TTL Investigation")
print("Destination:", DESTINATION)

print("-" * 65)
print(
    f"{'TTL':<10}"
    f"{'Responding IP':<22}"
    f"{'ICMP Type':<15}"
    f"{'ICMP Code':<10}"
)
print("-" * 65)
for ttl in range(1, MAX_TTL + 1):

    packet = (
        IP(dst=DESTINATION, ttl=ttl)
        /
        ICMP(type=8, code=0, id=1234, seq=ttl)
        /
        Raw(load=b"TTL TEST")
    )
    
    response = sr1(
        packet,
        timeout=TIMEOUT,
        verbose=0
    )
    
    if response is None:

        print(
            f"{ttl:<10}"
            f"{'*':<22}"
            f"{'-':<15}"
            f"{'-':<10}"
        )

        continue

    
    if IP in response and ICMP in response:

        responding_ip = response[IP].src
        icmp_type = response[ICMP].type
        icmp_code = response[ICMP].code
        print(
            f"{ttl:<10}"
            f"{responding_ip:<22}"
            f"{icmp_type:<15}"
            f"{icmp_code:<10}"
        )

        if (
            icmp_type == 0
            and responding_ip == DESTINATION
        ):

            print("\nDestination reached!")

            break

    else:

        print(f"{ttl:<10}Unexpected response")

else:

    print("\nMaximum TTL reached.")
