from scapy.all import IP, TCP, ICMP, sr1
import random

DEST_IP = input("Enter destination IP address: ").strip()
DEST_PORT = int(input("Enter TCP port number: ").strip())

TIMEOUT = 3

flag_combinations = [
    ("SYN", "S"),
    ("ACK", "A"),
    ("FIN+ACK", "FA"),
    ("RST", "R"),
    ("SYN+FIN", "SF")
]

print("\nTCP FLAG BEHAVIOUR ANALYSIS")
print("=" * 60)

for name, flags in flag_combinations:

    source_port = random.randint(1024, 65535)

    ip_layer = IP(dst=DEST_IP)

    tcp_layer = TCP(
        sport=source_port,
        dport=DEST_PORT,
        flags=flags,
        seq=1000,
        ack=1 if "A" in flags else 0
    )

    packet = ip_layer / tcp_layer

    print(f"\nSending {name} packet...")
    print("Source Port:", source_port)
    print("Destination:", DEST_IP, DEST_PORT)
    print("Sent Flags:", flags)

    response = sr1(packet, timeout=TIMEOUT, verbose=0)

    if response is None:
        print("No response received")

    elif response.haslayer(TCP):
        print("Response Protocol: TCP")
        print("Responding IP:", response[IP].src)
        print("Response Flags:", response[TCP].flags)

    elif response.haslayer(ICMP):
        print("Response Protocol: ICMP")
        print("Responding IP:", response[IP].src)
        print("ICMP Type:", response[ICMP].type)
        print("ICMP Code:", response[ICMP].code)

    else:
        print("Other response received")