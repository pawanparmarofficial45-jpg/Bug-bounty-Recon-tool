import requests
import socket
import argparse
from concurrent.futures import ThreadPoolExecutor

def banner():
    print("""
    =====================================
        QuickRecon - VAPT Recon Tool
        Automated Reconnaissance
    =====================================
    """)

def dns_lookup(domain):
    try:
        ip = socket.gethostbyname(domain)
        print(f"[+] {domain} -> {ip}")
    except:
        pass

def subdomain_enum(domain, wordlist):
    print("\n[+] Starting Subdomain Enumeration\n")

    with open(wordlist) as f:
        subdomains = f.read().splitlines()

    def check_sub(sub):
        url = f"http://{sub}.{domain}"
        try:
            requests.get(url, timeout=3)
            print(f"[FOUND] {url}")
        except:
            pass

    with ThreadPoolExecutor(max_workers=50) as executor:
        for sub in subdomains:
            executor.submit(check_sub, sub)

def port_scan(host):
    print("\n[+] Starting Port Scan\n")

    ports = [21,22,25,53,80,110,139,143,443,445,8080]

    for port in ports:
        try:
            s = socket.socket()
            s.settimeout(1)
            s.connect((host, port))
            print(f"[OPEN] Port {port}")
            s.close()
        except:
            pass

def http_headers(url):
    print("\n[+] Fetching HTTP Headers\n")

    try:
        r = requests.get(url)
        for k,v in r.headers.items():
            print(f"{k} : {v}")
    except:
        print("Unable to fetch headers")

def tech_detect(url):
    print("\n[+] Basic Technology Detection\n")

    try:
        r = requests.get(url)

        headers = r.headers

        if "Server" in headers:
            print(f"Server: {headers['Server']}")

        if "X-Powered-By" in headers:
            print(f"Technology: {headers['X-Powered-By']}")

        if "cloudflare" in r.text.lower():
            print("Possible WAF: Cloudflare")

    except:
        pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d","--domain", help="Target Domain")
    parser.add_argument("-w","--wordlist", help="Subdomain Wordlist")

    args = parser.parse_args()

    banner()

    dns_lookup(args.domain)
    subdomain_enum(args.domain,args.wordlist)
    port_scan(args.domain)
    http_headers(f"http://{args.domain}")
    tech_detect(f"http://{args.domain}")

if __name__ == "__main__":
    main()
