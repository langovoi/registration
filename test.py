import requests

s = requests.Session()
headers = { 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8', 'Connection': 'keep-alive',
            'Referer': f'https://service2.diplo.de/rktermin/extern/choose_category.do?locationCode=mins&realmId=231&categoryId=373','Sec-Fetch-Dest': 'document','Sec-Fetch-Mode': 'navigate','Sec-Fetch-Site': 'same-origin','Sec-Fetch-User': '?1','Upgrade-Insecure-Requests': '1','User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36','sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"macOS"',
            }
s.get('https://service2.diplo.de/rktermin/extern/choose_category.do?locationCode=mins&realmId=231&categoryId=373', headers=headers)
print(s.cookies)
print(s.cookies.get_dict()['JSESSIONID'])
