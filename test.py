import sys
from multiprocessing import Pool

from germany import Germany
from utils import telegram

if __name__ == "__main__":
    with Pool(10) as p:
        p.map(register, families)

params = {
    'locationCode': 'mins',
    'realmId': '231',
    'categoryId': '375',
    'dateStr': '18.08.2022',
    'openingPeriodId': '29296',
}

response = requests.get('https://service2.diplo.de/rktermin/extern/appointment_showForm.do', params=params, cookies=cookies, headers=headers)
print(response.text)