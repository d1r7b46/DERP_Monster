# DERP_Monster
Find, collect, and create business email accounts.

## Instructions
- git clone https://github.com/d1r7b46/DERP_Monster
- cd DERP_Monster
- python3 DERP_Monster.py

## About
This tool is designed to intake a domain name and provide the following functions:
- Perform Google, Yahoo, Bing, and Yandex searches
- Deduplicate
- Intake usernames and append the same domain
- Append 50 of the most common service account emails (https://github.com/d1r7b46/Default-Email-Repository-Project/blob/main/2-50-Most-Common)

After the list is created, it can be used with a tool like CredMaster (https://github.com/knavesec/CredMaster/tree/master) to enumerate actual accounts.

## Future Plans
- Run Dehashed-Parser (https://github.com/hmaverickadams/DeHashed-API-Tool/tree/main) alongside but combine emails the main enumeration list.
- Research other free email finders and include
