import subprocess
import random
import argparse
from colorama import Fore, Style


def PrintBanner():
    banner = """
  *   ___                       ___               .   _____        *
     /__/\  .     ___  *       /  /\      *          /  /::\   
     \  \:\   *  /  /\        /  /:/                /  /:/\:\  *
    * \  \:\    /  /:/     * /  /:/    .        *  /  /:/  \:\        *
  _____\__\:\  /__/::\  .   /  /:/  ___           /__/:/ \__\:|
 /__/::::::::\ \__\/\:\__  /__/:/  /  /\  [####]  \  \:\ /  /:/
 \  \:\~~\~~\/    \  \:\/\ \  \:\ /  /:/           \  \:\  /:/    
  \  \:\  ~~~      \__\::/  \  \:\  /:/     *       \  \:\/:/  .
   \  \:\    *     /__/:/    \  \:\/:/            .  \  \::/      *
    \  \:\       . \__\/  *   \  \::/      .          \__\/    
  *  \__\/                     \__\/  
     Authored by: r_panov on 07/04/2018           *
     'momentary masters of a fraction of a dot' - Carl Sagan' 

     """
    print(Fore.BLUE)        # wrap output in BLUE text
    print(banner)
    print(Style.RESET_ALL)  # reset color to term. pref.


def funcDate():  # ----------------------------------------------
    # print the function welcome right off the bat
    print("\n<--> Results of date function (option -d)  \n")

    d = "The Date is            : "
    rd = "The reverse date is    : "

    the_date = subprocess.getoutput('date')
    rev_date = the_date[::-1]
    print(Fore.BLUE)        # wrap output in BLUE text
    print(f'{d}' + the_date)
    print(f'{rd}' + rev_date)
    print(Style.RESET_ALL)  # reset color to terminal prefences


def getnics():  # ----------------------------------------------
    # print the function welcome right off the bat
    print("\n<--> Results of network interface function (option -n)  \n")
    # to-do ---> somehow incorporate a progress bar for the length nic subprocess call
    # in the section we will find system nics, display them, and ask if user wants to diagnose
    print('Checking for networks interfaces (nics) ---> ')
    print('This will take ~10 seconds...')
    # subprocess to call cmd, save and split the out to a variable, and print the variable with tab seps
    a = subprocess.run(['netstat -i | cut -d " " -f 1'], shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
    b = a.split()
    # have to loop through list and append new/unique values since 'sort()' doesn't work
    c = []
    for x in b:
        if x in c or x == 'Name':
            pass
        else:
            c.append(x)

    # count the interfaces
    d = len(c)
    # print message and interface list
    print(f"Interface's found: {d}\n")
    print(Fore.BLUE)        # wrap output in BLUE text
    print(*c, sep='\t')
    print(Style.RESET_ALL)  # reset output to terminal preference

    # print user options after nics have been displayed to see how they want proceed

    e = str(input('\nWould you like to run diagnostics in a nic? (y/n) :    ')).lower()
    if e == 'y':
        print('\nOK, please choose a nic to run diasnostics on :    ')
        f = str(input('nic --> : '))
    elif e == 'n':
        print('\nNo problem, back to main menu')
        exit()
    else:
        print("""\nMust enter 'y' or 'n'... you failed... goodbye""")

    diagnose(f)


def diagnose(f):  # ----------------------------------------------
    # in this section id like to run some network diagnostic tests on a specific nic
    # run a subprocess call 'ifconfig <nic>' on a specific nic
    a = subprocess.run([f'ifconfig {f}'], shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
    b = a.split()
    # print(b)

    # prints interface
    print(Fore.BLUE)        # wrap output in BLUE text
    print(f'Interface:               -->    {f}')
    # prints interfaces status
    for i in b:
        if i == 'active' or i == 'inactive':
            print(f'Network status:          -->    {i}')
    # print ipv4, ipv6, and default gateway address's
    for index, y in enumerate(b):
        if y == 'inet':
            ipv4 = index + 1
            print(f'IPv4 address:            -->    {b[ipv4]}')
        if y == 'inet6':
            ipv6 = index + 1
            print(f'IPv6 address:            -->    {b[ipv6]}')
        if y == 'broadcast':
            broad = index + 1
            print(f'Default Gateway:         -->    {b[broad]}')

    # public internet facing address
    # To-Do ---- try, except error capture
    c = subprocess.run(["""dig +short myip.opendns.com @resolver1.opendns.com"""], shell=True,
                       stdout=subprocess.PIPE).stdout.decode('utf-8')
    print(f'Public facing IP:        -->    {c}')

    # check for listening ports
    e = subprocess.run(["""lsof -i -P | grep -i "listen" | grep -v 'localhost'"""], shell=True,
                       stdout=subprocess.PIPE).stdout.decode('utf-8')
    e1 = list(e)
    e2 = []
    # list comprehension to scape ports numbers from command ouput
    z = [e2.append(i) for i in e1 if i != '*' and i != ":"]
    print('Open ports (excluding localhost):    ')
    print(*e2, sep='')
    print(Style.RESET_ALL)  # reset color to terminal preferences

    # connection speed
    print('Would you like to run a speed test? (y/n)')
    speedchoice = str(input('It will take ~15 seconds:  '))
    if speedchoice == 'y':
        print(Fore.BLUE)  # wrap output in BLUE text -- must be done before subprocess to catch stdout
        d = subprocess.run(["""curl -o /dev/null http://speedtest.wdc01.softlayer.com/downloads/test10.zip"""],
                           shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
        print(d)
        print(Style.RESET_ALL)  # reset color to terminal preferences
    else:
        pass

    # foreign connections?
    print('Would you like to investigate active foreign TCP connections? (y/n)')
    foreign = str(input('It will take < 3 seconds:  '))
    if foreign == 'y':
        f = subprocess.run(["""netstat -t -p TCP"""], shell=True,
                           stdout=subprocess.PIPE).stdout.decode('utf-8')
        print(Fore.BLUE)         # wrap output in BLUE text
        print(f)
        print(Style.RESET_ALL)  # reset color to terminal preference

        # ask user if they'd like to investigate any of the IP generated above
        forD = str(input('\nWould you like to investigate a foreign address listed above? (y/n) :   ')).lower()

        forDiagnose(forD)
    else:
        print('Exiting ... x__x ')


def forDiagnose(forD):

    while forD == 'y':
        a = str(input("Enter the foreign address you'd like to investigate  \nAddress:  "))
        print(f'\nInvestigating IP        --->    [{a}] \nThis may take ~3-10 seconds...')

        b = subprocess.run([f'nslookup {a}'], shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
        print(Fore.BLUE)        # wrap output in BLUE text
        print(b)
        print(Style.RESET_ALL)  # reset color to term. pref.

        c = subprocess.run([f'whois {a}'], shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
        print(Fore.BLUE)        # wrap output in BLUE text
        print(c)
        print(Style.RESET_ALL)  # reset color to term. pref.

        forD = str(input('Would you like to diagnose another IP address? (y/n) :    '))

    else:
        print('Exiting ... x__x ')


##### running the function
def main():
    import argparse
    # print the banner right off the bat
    PrintBanner()

    # take the user input, to decide what to function to run next
    parser = argparse.ArgumentParser(description='Messin around tool options:')
    parser.add_argument('-d', '--date', help='Enter (y/n) to run the date function')
    parser.add_argument('-n', '--nics', help='Enter (y/n) to run the network interface function')
    args = parser.parse_args()

    dateChoice = str(args.date).lower()
    nicsChoice = str(args.nics).lower()

    if dateChoice == 'y':
        funcDate()

    if nicsChoice == 'y':
        getnics()


main()























