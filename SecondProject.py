import requests
from bs4 import BeautifulSoup
import urllib.parse

# Test payloads
SQLI_PAYLOADS = ["'", "' OR '1'='1", "'--"]
XSS_PAYLOADS = ['<script>alert(1)</script>', '" onmouseover="alert(1)"']

HEADERS = {'User-Agent': 'Mozilla/5.0'}

def get_forms(url):
    """Extract all forms from a webpage."""
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.content, 'html.parser')
    return soup.find_all('form')

def form_details(form):
    """Extract form details like action, method, and inputs."""
    details = {}
    action = form.attrs.get('action')
    method = form.attrs.get('method', 'get').lower()
    inputs = []

    for input_tag in form.find_all('input'):
        input_type = input_tag.attrs.get('type', 'text')
        name = input_tag.attrs.get('name')
        if name:
            inputs.append({'type': input_type, 'name': name})

    details['action'] = action
    details['method'] = method
    details['inputs'] = inputs
    return details

def submit_form(form_details, url, value):
    """Submit form with a payload."""
    target_url = urllib.parse.urljoin(url, form_details['action'])
    data = {}

    for input_field in form_details['inputs']:
        if input_field['type'] == 'text':
            data[input_field['name']] = value
        else:
            data[input_field['name']] = 'test'

    if form_details['method'] == 'post':
        return requests.post(target_url, data=data, headers=HEADERS)
    else:
        return requests.get(target_url, params=data, headers=HEADERS)

def scan_sql_injection(url):
    print("\n[+] Scanning for SQL Injection...")
    forms = get_forms(url)
    vulnerable = False

    for form in forms:
        form_info = form_details(form)
        for payload in SQLI_PAYLOADS:
            res = submit_form(form_info, url, payload)
            if any(error in res.text.lower() for error in ["sql syntax", "mysql", "warning", "error in your sql"]):
                print(f"[!] SQL Injection vulnerability detected with payload: {payload}")
                vulnerable = True
                break

    if not vulnerable:
        print("[-] No SQL Injection vulnerabilities found.")

def scan_xss(url):
    print("\n[+] Scanning for XSS...")
    forms = get_forms(url)
    vulnerable = False

    for form in forms:
        form_info = form_details(form)
        for payload in XSS_PAYLOADS:
            res = submit_form(form_info, url, payload)
            if payload in res.text:
                print(f"[!] XSS vulnerability detected with payload: {payload}")
                vulnerable = True
                break

    if not vulnerable:
        print("[-] No XSS vulnerabilities found.")

def main():
    url = input("Enter target URL: ").strip()
    if not url.startswith("http"):
        url = "http://" + url
    scan_sql_injection(url)
    scan_xss(url)

if __name__ == "__main__":
    main()