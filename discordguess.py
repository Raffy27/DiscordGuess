import requests
import json
from time import sleep
from colorama import init, Fore

init()

print(Fore.LIGHTGREEN_EX + """
    ____  _                          ________                    
   / __ \\(_)_____________  _________/ / ____/_  _____  __________
  / / / / / ___/ ___/ __ \\/ ___/ __  / / __/ / / / _ \\/ ___/ ___/
 / /_/ / (__  ) /__/ /_/ / /  / /_/ / /_/ / /_/ /  __(__  |__  ) 
/_____/_/____/\\___/\\____/_/   \\__,_/\\____/\\__,_/\\___/____/____/  
                                                                 """ + Fore.RESET);

# Discord has a 10 requests/minute rate limit on the Add Friend function.
# Rate limiting delays are implemented, but use a 10 second delay to avoid suspicion.

token = input('Token: ')      # Discord Authorization Token
delay = int(input('Delay: ')) # Seconds to wait between requests
req = {}
req['username'] = input('Username: ') # Username to guess
token = token.replace('"', '')

headers = { 'Host':             'discordapp.com',
            'User-Agent':       'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Accept':           '*/*',
            'Accept-Language':  'en-GB',
            'Accept-Encoding':  'gzip, deflate, br',
            'Content-Type':     'application/json',
            'Authorization':    token,
            'Connection':       'keep-alive',
            'Referer':          'https://discordapp.com/channels/@me'}

# Grab necessary cookies
s = requests.Session()
s.get('https://discordapp.com/channels/@me')
print('Cookies -->', s.cookies.get_dict())
print()

# Start bruteforce
found = False
i = 0
while i<10000:
    normalSleep = True
    i += 1
    print('[',i,'] ', sep = '', end = '')
    req['discriminator'] = i
    r = s.post('https://discordapp.com/api/v6/users/@me/relationships', data = json.dumps(req), headers = headers)
    if r.status_code == 204:   # Friend Request sent
        print(Fore.LIGHTGREEN_EX + 'Success!' + Fore.RESET)
        found = True
        break
    elif r.status_code == 400: # Incorrect Discriminator
        print('Incorrect')
    elif r.status_code == 429: # Rate Limit
        i -= 1
        p = (json.loads(r.text)['retry_after'])/1000
        print(Fore.MAGENTA + 'Rate limit: retrying after', p, 'seconds.' + Fore.RESET)
        normalSleep = False
        sleep(p)
    elif r.status_code == 401: # Invalid token
        print(Fore.LIGHTRED_EX + 'Invalid Token!')
        break
    else:
        print('Unknown error', r.status_code,'-->',r.text)
    if normalSleep:
        sleep(delay)

print()
if found:
    print('Discord Tag: ', Fore.LIGHTBLUE_EX + req['username'], '#', i, sep = '')
else:
    print(Fore.LIGHTRED_EX + 'This Discord Tag doesn\'t exist.')
print()