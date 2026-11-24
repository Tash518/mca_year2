from scapy.all import IP, TCP, sr1, send, RandShort
import random

destination_ip = input("Enter destination IP address: ").strip()
destination_port = int(input("Enter TCP port number: ").strip())

source_port = int(RandShort())
client_isn = random.randint(0, 2**32 - 1)

TIMEOUT = 5

ip_layer = IP(dst=destination_ip)

tcp_layer = TCP(
    sport=source_port,
    dport=destination_port,
    seq=client_isn,
    flags="S"
)

syn_packet = ip_layer / tcp_layer

print("\n[STEP 1] Sending SYN")
print("Client ISN:", client_isn)
syn_packet.show2()

response = sr1(
    syn_packet,
    timeout=TIMEOUT,
    verbose=False
)

if response is None:
    print("\nNo response received. Check destination IP, port and firewall.")
    raise SystemExit

if not response.haslayer(TCP):
    print("\nReceived a non-TCP response.")
    response.show()
    raise SystemExit

server_flags = response[TCP].flags

if not (server_flags & 0x02 and server_flags & 0x10):
    print("\nResponse is not SYN+ACK.")
    print("Received flags:", server_flags)
    response.show()
    raise SystemExit

server_isn = response[TCP].seq
received_ack = response[TCP].ack

print("\n[STEP 2] Received SYN+ACK")
print("Server ISN:", server_isn)
print("SYN+ACK acknowledgment:", received_ack)

expected_client_seq = (client_isn + 1) % (2**32)
expected_client_ack = (server_isn + 1) % (2**32)

print("\n[CALCULATION]")
print("Expected client sequence:", expected_client_seq)
print("Expected client acknowledgment:", expected_client_ack)

if received_ack != expected_client_seq:
    print("Unexpected acknowledgment number.")
    raise SystemExit

ack_packet = (
    IP(dst=destination_ip) /
    TCP(
        sport=source_port,
        dport=destination_port,
        seq=expected_client_seq,
        ack=expected_client_ack,
        flags="A"
    )
)

print("\n[STEP 3] Constructing final ACK")
ack_packet.show2()

print("\nSending final ACK...")
send(ack_packet, verbose=True)

print("\n========== TCP HANDSHAKE SUMMARY ==========")
print("Client ISN =", client_isn)
print("Server ISN =", server_isn)
print("SYN+ACK acknowledgment =", received_ack)
print("Expected client acknowledgment =", expected_client_ack)
print("Expected client sequence =", expected_client_seq)
print("===========================================")