from scapy.all import sniff, IP, TCP, UDP, ICMP, wrpcap
from collections import defaultdict
from datetime import datetime
import time

flows = {}

ip_stats = defaultdict(lambda: {
    "packets": 0,
    "bytes": 0
})

def packet_analysis(pkt):

    if not pkt.haslayer(IP):
        return

    ip = pkt[IP]

    src_ip = ip.src
    dst_ip = ip.dst

    if pkt.haslayer(TCP):

        protocol = "TCP"
        src_port = pkt[TCP].sport
        dst_port = pkt[TCP].dport

    elif pkt.haslayer(UDP):

        protocol = "UDP"
        src_port = pkt[UDP].sport
        dst_port = pkt[UDP].dport

    elif pkt.haslayer(ICMP):

        protocol = "ICMP"
        src_port = 0
        dst_port = 0

    else:
        return

    flow_key = (
        src_ip,
        src_port,
        dst_ip,
        dst_port,
        protocol
    )
    
    packet_size = int(ip.len)
    packet_time = float(pkt.time)

    if flow_key not in flows:

        flows[flow_key] = {
            "packets": 0,
            "bytes": 0,
            "first_time": packet_time,
            "last_time": packet_time
        }

    flows[flow_key]["packets"] += 1
    flows[flow_key]["bytes"] += packet_size
    flows[flow_key]["last_time"] = packet_time

    ip_stats[src_ip]["packets"] += 1

    ip_stats[src_ip]["bytes"] += packet_size
print("Starting network traffic capture...")

print("Capture duration: 15 minutes")

print("Start time:", datetime.now())

start = time.time()

pkts = sniff(
    filter="ip and (tcp or udp or icmp)",
    prn=packet_analysis,
    timeout=900,
    store=True
)

end = time.time()

print("\nCapture completed!")

print("End time:", datetime.now())

print("Actual capture duration:", round(end - start, 2), "seconds")

print("Total captured packets:", len(pkts))


wrpcap("network_capture.pcap", pkts)

print("\nPackets saved to network_capture.pcap")



print("\n========== ALL NETWORK FLOWS ==========")

for flow, stats in flows.items():

    duration = stats["last_time"] - stats["first_time"]

    print("\nFlow:", flow)

    print("Packets:", stats["packets"])

    print("Bytes:", stats["bytes"])

    print("Duration:", round(duration, 6), "seconds")



print("\n========== TOP 10 FLOWS BY BYTES ==========")

top_bytes = sorted(
    flows.items(),
    key=lambda x: x[1]["bytes"],
    reverse=True
)[:10]

for rank, (flow, stats) in enumerate(top_bytes, 1):

    print(
        rank,
        flow,
        "Bytes:", stats["bytes"],
        "Packets:", stats["packets"]
    )

print("\n========== TOP 10 FLOWS BY PACKETS ==========")

top_packets = sorted(
    flows.items(),
    key=lambda x: x[1]["packets"],
    reverse=True
)[:10]

for rank, (flow, stats) in enumerate(top_packets, 1):

    print(
        rank,
        flow,
        "Packets:", stats["packets"],
        "Bytes:", stats["bytes"]
    )

print("\n========== TOP TALKERS BY BYTES ==========")

top_ip_bytes = sorted(
    ip_stats.items(),
    key=lambda x: x[1]["bytes"],
    reverse=True
)[:10]

for rank, (ip, stats) in enumerate(top_ip_bytes, 1):

    print(
        rank,
        ip,
        "Bytes sent:", stats["bytes"],
        "Packets sent:", stats["packets"]
    )

print("\n========== TOP TALKERS BY PACKETS ==========")

top_ip_packets = sorted(
    ip_stats.items(),
    key=lambda x: x[1]["packets"],
    reverse=True
)[:10]

for rank, (ip, stats) in enumerate(top_ip_packets, 1):

    print(
        rank,
        ip,
        "Packets sent:", stats["packets"],
        "Bytes sent:", stats["bytes"]
    )


print("\n========== ANALYSIS COMPLETED ==========")
