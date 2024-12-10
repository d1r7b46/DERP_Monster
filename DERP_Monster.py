import os
from colorama import Fore, Style, init
from time import sleep
from search_engines import search_emails  # Import the search function

def banner():
    init(autoreset=True)
    print(Fore.BLUE + Style.BRIGHT + """
                ⣀⣤⣴⣶⣤⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀      ⣠⡤⣤⣄⣾⣿⣿⣿⣿⣿⣿⣷⣠⣀⣄⡀⠀⠀⠀⠀ 
⠀⠀       ⠙⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣬⡿⠀⠀⠀⠀ 
⠀      ⠀    ⣼⠟⢿⣿⣿⣿⣿⣿⣿⡿⠘⣷⣄⠀⠀⠀⠀⠀ 
     ⣰⠛⠛⣿⢠⣿⠋⠀⠀⢹⠻⣿⣿⡿⢻⠁⠀⠈⢿⣦⠀⠀⠀⠀ 
     ⢈⣵⡾⠋⣿⣯⠀⠀⢀⣼⣷⣿⣿⣶⣷⡀⠀⠀⢸⣿⣀⣀⠀⠀ 
     ⢾⣿⣀⠀⠘⠻⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⠿⣿⡁⠀⠀⠀ 
      ⠈⠙⠛⠿⠿⠿⢿⣿⡿⣿⣿⡿⢿⣿⣿⣿⣿⣷⣄⠀⠘⢷⣆⠀⠀ 
         ⠀⠀⢠⣿⠏⠀⣿⡏⠀⣼⣿⠛⢿⣿⣿⣆⠀⠀⣿⡇⡀ 
       ⠀⠀  ⣾⡟⠀⠀⣿⣇⠀⢿⣿⡀⠈⣿⡌⠻⠷⠾⠿⣻⠁ 
⠀      ⣠⣶⠟⠫⣤⠀⠀⢸⣿⠀⣸⣿⢇⡤⢼⣧⠀⠀⠀⢀⣿⠀  
     ⣾⡏⠀⡀⣠⡟⠀⠀⢀⣿⣾⠟⠁⣿⡄⠀⠻⣷⣤⣤⡾⠋⠀  
    ⠀⠙⠷⠾⠁⠻⣧⣀⣤⣾⣿⠋⠀⠀⢸⣧⠀⠀⠀⠉⠁⠀⠀⠀  
⠀⠀⠀        ⠈⠉⠉⠹⣿⣄⠀⠀⣸⡿⠀⠀⠀⠀⠀⠀⠀   
⠀⠀⠀⠀     ⠀⠀ ⠀ ⠀⠙⠛⠿⠟⠛⠁⠀               
""")
    print(Fore.MAGENTA + Style.BRIGHT + "                         DERP_Monster                                   ")
    print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT + "                           By d1r7b46                                    \n" + Style.RESET_ALL)
    print("-" * 45)

def generate_emails(domain):
    # Check if domain contains a dot
    if '.' not in domain:
        raise ValueError("Invalid domain name. Please provide a valid domain name.")

    # Read common usernames from file
    with open('common_usernames.txt', 'r') as file:
        common_usernames = file.read().splitlines()

    # Read additional usernames if the file exists
    additional_usernames = []
    if os.path.exists('additional_usernames.txt'):
        with open('additional_usernames.txt', 'r') as file:
            additional_usernames = file.read().splitlines()

    # Generate email addresses from common usernames
    emails = [username + '@' + domain for username in common_usernames]

    # Ask if users have been added to additional_usernames.txt
    add_additional = input("Have users been added to additional_usernames.txt? (y/n): ").lower()
    if add_additional == 'y' and additional_usernames:
        # Only add if the file exists and has usernames
        emails.extend(username.strip() + '@' + domain for username in additional_usernames)
    elif add_additional != 'n':
        print("Invalid input. Assuming 'n'.")

    return emails

def save_emails(emails, domain):
    # Create a filename based on the domain
    filename = domain + "_DERPed.txt"
    
    # Check if file already exists
    if os.path.exists(filename):
        print(f"File {filename} already exists. Appending emails to it.")
        with open(filename, 'a') as output_file:
            for email in emails:
                output_file.write(email + '\n')
    else:
        with open(filename, 'w') as output_file:
            for email in emails:
                output_file.write(email + '\n')
    print(f"\nGenerated emails are saved in {filename}")

if __name__ == "__main__":
    banner()
    domain = input("Enter the domain name: ")
    
    try:
        # Step 1: Search for emails
        print(f"\nSearching for email addresses related to {domain}...\n")
        search_emails(domain)  # Call search function (from search_engines.py)
        sleep(1)  # Just for a slight delay between tasks

        # Step 2: Generate emails
        emails = generate_emails(domain)

        # Step 3: Save the generated emails
        save_emails(emails, domain)

    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")
