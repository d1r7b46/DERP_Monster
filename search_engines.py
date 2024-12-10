import requests
import warnings
import urllib3
from random import randint
from time import sleep
from emailfinder.utils.exception import GoogleCaptcha, GoogleCookiePolicies
from emailfinder.utils.agent import user_agent
from emailfinder.utils.file.email_parser import get_emails  # Assuming you have this function
from emailfinder.utils.color_print import print_info, print_ok
from bs4 import BeautifulSoup

# Suppress the InsecureRequestWarning
warnings.simplefilter('ignore', urllib3.exceptions.InsecureRequestWarning)


def get_random_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    ]
    return {'User-Agent': user_agents[randint(0, len(user_agents) - 1)]}

def save_emails_to_file(emails, domain):
    """ Save the found emails to a file named after the domain. """
    filename = f"{domain}_DERPed.txt"
    with open(filename, "a") as file:
        for email in emails:
            file.write(f"{email}\n")

def generate_emails_from_usernames(domain, common_file, additional_file):
    """ Generate emails from common and additional usernames. """
    emails = set()
    with open(common_file, "r") as common, open(additional_file, "r") as additional:
        common_usernames = common.read().splitlines()
        additional_usernames = additional.read().splitlines()

        for username in common_usernames:
            emails.add(f"{username}@{domain}")
        
        for username in additional_usernames:
            emails.add(f"{username}@{domain}")

    return list(emails)

def search_google(domain, total=100, proxies=None):
    base_url = "https://www.google.com/search?q=intext:@{}&num={}"
    emails = set()
    start = 0
    num_results = 50
    total_loop = int(total / num_results)
    if total % num_results != 0:
        total_loop += 1

    cookies = {"CONSENT": "YES+srp.gws"}

    while start < total_loop:
        try:
            url = base_url.format(domain, num_results) + f"&start={start * num_results}"
            response = requests.get(url,
                                    headers=get_random_user_agent(),
                                    allow_redirects=False,
                                    cookies=cookies,
                                    verify=False,
                                    proxies=proxies)
            text = response.text
            if response.status_code == 302 and ("https://www.google.com/webhp" in text or "https://consent.google.com" in text):
                raise GoogleCookiePolicies()
            elif "detected unusual traffic" in text:
                raise GoogleCaptcha()
            emails = emails.union(get_emails(domain, text))

            soup = BeautifulSoup(text, "html.parser")
            if len(soup.find_all("h3")) < num_results:
                break

        except GoogleCaptcha:
            print_info("Google CAPTCHA detected. Retrying...")
            sleep(5)
            continue
        except GoogleCookiePolicies:
            print_info("Google Cookie Policies page detected. Retrying...")
            sleep(5)
            continue
        except Exception as ex:
            print_info(f"Error: {ex}")
            break

        start += 1
        sleep(2)

    return emails

def search_bing(domain, total=100, proxies=None):
    base_url = "https://www.bing.com/search?q=inbody:@{}&first={}"
    emails = set()
    start = 0
    num_results = 10
    total_loop = int(total / num_results)
    if total % num_results != 0:
        total_loop += 1

    while start < total_loop:
        try:
            url = base_url.format(domain, start * num_results)
            response = requests.get(url,
                                    headers=get_random_user_agent(),
                                    timeout=5,
                                    proxies=proxies)
            emails = emails.union(get_emails(domain, response.text))
            soup = BeautifulSoup(response.text, "html.parser")
            if len(soup.find_all("h2")) < num_results:
                break
        except Exception as ex:
            print_info(f"Error: {ex}")
            break

        start += 1
        sleep(2)

    return emails

def search_yahoo(domain, total=100, proxies=None):
    base_url = "https://search.yahoo.com/search?p=inbody:@{}&b={}"
    emails = set()
    start = 0
    num_results = 10
    total_loop = int(total / num_results)
    if total % num_results != 0:
        total_loop += 1

    while start < total_loop:
        try:
            url = base_url.format(domain, start * num_results)
            response = requests.get(url,
                                    headers=get_random_user_agent(),
                                    timeout=5,
                                    proxies=proxies)
            emails = emails.union(get_emails(domain, response.text))
            soup = BeautifulSoup(response.text, "html.parser")
            if len(soup.find_all("h3")) < num_results:
                break
        except Exception as ex:
            print_info(f"Error: {ex}")
            break

        start += 1
        sleep(2)

    return emails

def search_yandex(domain, total=100, proxies=None):
    base_url = "https://yandex.com/search/?text=inbody:@{}&p={}"
    emails = set()
    start = 0
    num_results = 10
    total_loop = int(total / num_results)
    if total % num_results != 0:
        total_loop += 1

    while start < total_loop:
        try:
            url = base_url.format(domain, start * num_results)
            response = requests.get(url,
                                    headers=get_random_user_agent(),
                                    timeout=5,
                                    proxies=proxies)
            emails = emails.union(get_emails(domain, response.text))
            soup = BeautifulSoup(response.text, "html.parser")
            if len(soup.find_all("h2")) < num_results:
                break
        except Exception as ex:
            print_info(f"Error: {ex}")
            break

        start += 1
        sleep(2)

    return emails

def search_emails(domain):
    # Initialize the set for all emails
    all_emails = set()

    # Create a dictionary to keep track of emails found per engine
    email_counts = {
        'Google': 0,
        'Bing': 0,
        'Yahoo': 0,
        'Yandex': 0
    }

    # Search for emails from each engine and update the set
    google_emails = search_google(domain)
    email_counts['Google'] = len(google_emails)
    all_emails.update(google_emails)

    bing_emails = search_bing(domain)
    email_counts['Bing'] = len(bing_emails)
    all_emails.update(bing_emails)

    yahoo_emails = search_yahoo(domain)
    email_counts['Yahoo'] = len(yahoo_emails)
    all_emails.update(yahoo_emails)

    yandex_emails = search_yandex(domain)
    email_counts['Yandex'] = len(yandex_emails)
    all_emails.update(yandex_emails)

    # Print the number of emails found per engine
    print(f"Found {email_counts['Google']} emails from Google.")
    print(f"Found {email_counts['Bing']} emails from Bing.")
    print(f"Found {email_counts['Yahoo']} emails from Yahoo.")
    print(f"Found {email_counts['Yandex']} emails from Yandex.")

    # Deduplication
    total_found = len(all_emails)
    print(f"\nDeduplication complete. {total_found} unique emails were found across all search engines.")

    # Save the emails to a file
    save_emails_to_file(all_emails, domain)

    # Return the list of unique emails
    return list(all_emails)



