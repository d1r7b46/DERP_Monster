import requests
import logging
import random
import time
from random import randint
from time import sleep
import concurrent.futures
from emailfinder.utils.exception import GoogleCaptcha, GoogleCookiePolicies
from emailfinder.utils.file.email_parser import get_emails  # Assuming you have this function
from emailfinder.utils.color_print import print_info, print_ok
from bs4 import BeautifulSoup

# Set up logging
logging.basicConfig(level=logging.INFO)

# Retry function with exponential backoff
def retry_request(url, retries=5, backoff_factor=2, proxies=None):
    """Retry a request with exponential backoff."""
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=get_random_user_agent(), timeout=5, proxies=proxies)
            response.raise_for_status()  # Raise an error for bad status codes (4xx, 5xx)
            return response
        except requests.exceptions.RequestException as e:
            logging.info(f"Request failed: {e}. Retrying...")
            sleep_time = random.randint(2 ** attempt, 2 ** (attempt + 1))
            time.sleep(sleep_time)
    logging.error("Maximum retries reached. Request failed.")
    return None

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

def extract_email_from_html(domain, html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    emails = get_emails(domain, html_content)
    return emails

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
            # Removed progress print
            url = base_url.format(domain, num_results) + f"&start={start * num_results}"
            response = retry_request(url, retries=5, proxies=proxies)

            if not response:
                break

            text = response.text
            if response.status_code == 302 and ("https://www.google.com/webhp" in text or "https://consent.google.com" in text):
                raise GoogleCookiePolicies()
            elif "detected unusual traffic" in text:
                raise GoogleCaptcha()

            emails = emails.union(extract_email_from_html(domain, text))

            soup = BeautifulSoup(text, "html.parser")
            if len(soup.find_all("h3")) < num_results:
                break

        except GoogleCaptcha:
            logging.info("Google CAPTCHA detected. Retrying...")
            sleep(5)
            continue
        except GoogleCookiePolicies:
            logging.info("Google Cookie Policies page detected. Retrying...")
            sleep(5)
            continue
        except Exception as ex:
            logging.info(f"Error: {ex}")
            break

        start += 1
        sleep(2)

    print_ok(f"Found {len(emails)} emails from Google.")
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
            # Removed progress print
            url = base_url.format(domain, start * num_results)
            response = retry_request(url, retries=5, proxies=proxies)

            if not response:
                break

            emails = emails.union(extract_email_from_html(domain, response.text))
            soup = BeautifulSoup(response.text, "html.parser")
            if len(soup.find_all("h2")) < num_results:
                break
        except Exception as ex:
            logging.info(f"Error: {ex}")
            break

        start += 1
        sleep(2)

    print_ok(f"Found {len(emails)} emails from Bing.")
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
            # Removed progress print
            url = base_url.format(domain, start * num_results)
            response = retry_request(url, retries=5, proxies=proxies)

            if not response:
                break

            emails = emails.union(extract_email_from_html(domain, response.text))
            soup = BeautifulSoup(response.text, "html.parser")
            if len(soup.find_all("h3")) < num_results:
                break
        except Exception as ex:
            logging.info(f"Error: {ex}")
            break

        start += 1
        sleep(2)

    print_ok(f"Found {len(emails)} emails from Yahoo.")
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
            # Removed progress print
            url = base_url.format(domain, start * num_results)
            response = retry_request(url, retries=5, proxies=proxies)

            if not response:
                break

            emails = emails.union(extract_email_from_html(domain, response.text))
            soup = BeautifulSoup(response.text, "html.parser")
            if len(soup.find_all("h2")) < num_results:
                break
        except Exception as ex:
            logging.info(f"Error: {ex}")
            break

        start += 1
        sleep(2)

    print_ok(f"Found {len(emails)} emails from Yandex.")
    return emails

def parallel_search(domain, total=100, proxies=None):
    search_functions = [
        search_google,
        search_bing,
        search_yahoo,
        search_yandex
    ]

    all_emails = set()
    email_counts = {engine.__name__: 0 for engine in search_functions}

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_engine = {executor.submit(engine, domain, total, proxies): engine for engine in search_functions}
        for future in concurrent.futures.as_completed(future_to_engine):
            engine = future_to_engine[future]
            try:
                result = future.result()
                email_counts[engine.__name__] = len(result)
                all_emails.update(result)
            except Exception as ex:
                logging.info(f"Error searching with {engine.__name__}: {ex}")

    return list(all_emails), email_counts

def search_emails(domain, total=100, proxies=None):
    logging.info(f"Starting concurrent searches for emails belonging to {domain}")
    
    # Run parallel searches for emails across multiple search engines
    all_emails, email_counts = parallel_search(domain, total, proxies)

    # Print the number of emails found per engine
    print_info(f"Found {email_counts['search_google']} emails from Google.")
    print_info(f"Found {email_counts['search_bing']} emails from Bing.")
    print_info(f"Found {email_counts['search_yahoo']} emails from Yahoo.")
    print_info(f"Found {email_counts['search_yandex']} emails from Yandex.")

    # Deduplication
    total_found = len(all_emails)
    print_ok(f"\nDeduplication complete. {total_found} unique emails were found across all search engines.")

    # Save the emails to a file
    save_emails_to_file(all_emails, domain)

    return list(all_emails)
