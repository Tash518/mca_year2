from scapy.all import IP, UDP, ICMP, Raw, sr1
import random

dest_ip = input("Enter destination IP address: ").strip()
start_port = int(input("Enter start UDP port number: ").strip())
end_port = int(input("Enter end UDP port number: ").strip())

TIMEOUT = 2
payload = b"UDP Port Scan Test"

print(f"\nScanning UDP ports {start_port} to {end_port} on {dest_ip}...")
print("-" * 75)
print(f"{'Port':<10}{'Status / Response Type':<35}{'ICMP Details':<30}")
print("-" * 75)

for port in range(start_port, end_port + 1):
    src_port = random.randint(1024, 65535)
    packet = IP(dst=dest_ip) / UDP(sport=src_port, dport=port) / Raw(load=payload)
    
    response = sr1(packet, timeout=TIMEOUT, verbose=0)
    
    
    if response is None:
        
        print(f"{port:<10}{'No Response (Open | Filtered)':<35}{'-':<30}")
        
    elif response.haslayer(UDP):
        
        print(f"{port:<10}{'UDP Response Received (Open)':<35}{'App-level response':<30}")
        
    elif response.haslayer(ICMP):
        
        icmp_type = response[ICMP].type
        icmp_code = response[ICMP].code
        
        if icmp_type == 3 and icmp_code == 3:
            status = "ICMP Port Unreachable (Closed)"
        else:
            status = f"ICMP Response (Type {icmp_type}, Code {icmp_code})"
            
        details = f"Type: {icmp_type}, Code: {icmp_code}"
        print(f"{port:<10}{status:<35}{details:<30}")
        
    else:
        print(f"{port:<10}{'Other packet received':<35}{'-':<30}")

print("-" * 75)
print("Scan complete.")