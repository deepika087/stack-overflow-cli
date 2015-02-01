"""
    Add the keywords to be searched in the command line.
    Result Set of 10 or less results baed on the query parameters added will be returned.
    Choose the option which you want to see on chrome or any browser of you choice.
    Edit chromePath accordingly.
    If the reuslt set is not as per your requirement then type 'm'.
    This will load another set of results of size = min(10, avaliableResults)
    To quit the scrpt type 'q'.
    
    Search Stack Overflow.
    Display a list of results on command line.
    Open user's chosen result in web browser.
    Ugly 30 minute script is ugly. No apologies.
    tonyblundell@gmail.com
"""

from bs4 import BeautifulSoup
import getpass
import os
import requests
import subprocess
import sys
from subprocess import Popen

"""
Add the path of your chrome.exe here.
Windows : Go to start, type chrome. Right click on appropriate suggestion
go To properties -> Shortcut-> copy Target field.
"""
chromePath="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe";
def main(q, page):
    """
        Main loop. Grab links from Stack Overflow, display to user as a menu.
    """
    links = get_links(q, page)
    show_menu(links)
    choice = get_choice(links)
    process_choice(choice, q, page, links)

def get_links(q, page):
    """
        Pull links from Stack Overflow - parse text and href to a dict.
    """
    links = []
    payload = {'pagesize': 10, 'q': q, 'page': page}
    response = requests.get('http://stackoverflow.com/search', params=payload)
    soup = BeautifulSoup(response.text)
    divs = soup.findAll('div', {'class': 'question-summary search-result'})
    for div in divs:
        a = div.find('a')
        text = BeautifulSoup(a.text, "html")
        links.append({'url': a['href'], 'text': text})
    return links

def show_menu(links):
    """
        Output menu to screen, wait for user input. 
    """
    for i, link in enumerate(links):
        print('{0}    {1}'.format(i, link['text']))
    print('m    More')
    print('q    Quit')

def get_choice(links):
    """
        Get user's menu choice.
    """
    choice = input('> ')
    valid_choices = [str(i) for i in range(len(links))]
    valid_choices.extend(['m', 'q'])
    if not choice in valid_choices:
        return get_choice(links)
    return choice

def process_choice(choice, q, page, links):
    """
        Process the user's menu choice (open in browser, show more links, etc).
    """
    # Open link in browser
    if choice in [str(i) for i in range(len(links))]:
        url = 'http://stackoverflow.com{0}'.format(links[int(choice)]['url'])
        subprocess.call([chromePath, url])
        #get_choice(links)
    # Get & show more links
    elif choice == 'm':
        main(q, page + 1)
    # Quit
    elif choice == 'q':
        sys.exit()

if __name__ == '__main__':
    """
        Run main loop with command line args as Stack Overflow search params.
    """
    main(' '.join(sys.argv[1:]), 1)
