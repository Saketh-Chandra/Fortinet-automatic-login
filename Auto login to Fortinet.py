from os import path, popen, remove
from time import sleep
from requests import post, head, Session, ConnectionError
from getpass import getpass


def _GetchWindows():
    # This reads only one character.
    from msvcrt import getch
    return getch()


def login(uname, passw):
    url_1 = 'http://www.google.co.in'

    headers = \
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}

    session = Session()

    res = session.get(url_1, headers=headers)

    magic = res.url.split('?')[1]

    my_referer = res.url

    payload = {
        '4Tredir': 'http://google.com/',
        'magic': str(magic),
        'username': uname,
        'password': passw,
        }

    url_2 = 'http://detectportal.firefox.com'

    res = post(url_2, headers=headers, data=payload)

    if 'Failed' in res.text:
        return False
    else:
        print('Successfully authenticated, now closing this window. Bye.. :)')
        sleep(.777)
        return True


def main():
    print("Checking connectivity..")
    try:
        res = head('http://www.google.co.in')
        print('Already connected. :)')
    except ConnectionError:
        fn = path.expanduser('~/.fgauthcred')  # filename

        if not path.isfile(fn):
            print('Enter credentials to login, for the first time. (password will be hidden.)')

            username = input('Enter your username : ').strip()
            password = getpass()

            if login(username, password):
                with open(fn, 'w') as f:
                    f.write(username + '\n' + password + '\n')
                    popen('attrib +h ' + fn)
            else:
                print('Wrong credentials. Try again.\n')
                username = input('Enter your username : ').strip()
                password = getpass()
                login(username, password)
        else:
            with open(fn, 'r') as f:
                (username, password) = [x.strip() for x in f]
            if not login(username, password):
                remove(fn)
                print('Something went wrong with your credentials. Reseting...\nRestart the program again.')
                print("\nPress any key to exit.")
                _GetchWindows()


if __name__ == '__main__':
    main()
    sleep(1)
