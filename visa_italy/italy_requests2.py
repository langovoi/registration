import re
from time import sleep

import mechanize

import ssl

from mechanize import CheckboxControl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

browser = mechanize.Browser()
browser.set_handle_robots(False)
cookies = mechanize.CookieJar()
browser.set_cookiejar(cookies)

browser.addheaders = [('User-agent',
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36')]
browser.set_handle_refresh(False)

url = 'https://prenotami.esteri.it/Home'
html = browser.open(url).read()
print(html.decode('utf-8'))
browser.select_form(nr=0)  # This is login-password form -> nr = number = 0
browser.form['Email'] = 'kojio6ok@tut.by'
browser.form['Password'] = 'Khimik1971'
html = browser.submit().read()
print(html.decode('utf-8'))

browser.follow_link(url='/Services')

url = 'https://prenotami.esteri.it/Services/Booking/163'
html = browser.open(url).read()
print(html.decode('utf-8'))
browser.select_form(nr=1)
add_control = browser.form.find_control(name='PrivacyCheck', id='PrivacyCheck')
add_control.value = True
response = browser.submit()

with open('page_source.html', 'w') as f:
    f.write(response.read().decode('utf-8'))

# # Print the site
# content = resp.get_data().decode("utf-8")
# for link in browser.links():
#     print(link)
# print(content)


# with open('page_source.html', 'w') as f:
#     f.write(content)
#
# # print(response.read())
