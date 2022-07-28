from datetime import datetime
from time import sleep

import requests

server_pool = 'rd21o00000000000000000000ffffc0a806e8o443'

def get_dates():
    cookies = {
        'BIGipServerpool_prenotami.esteri.it': f'{server_pool}',
        '.cookie.': 'pTb4-p3Te4oYkkE6cXK1q-xspUeVdbRYMr5mZQe7gW7P2KSFd_rZ6H4T58NbzXIipSjhfmJVdmhzOlb-kxF72x9mciPB9sPzHUEnBjLipsYGCfhslGdp-3dwImT4zaS3Qbr2ANMreQG-_rv1KNW71WBTkOnD1dAmCUSe3jSLHh5FKV1n6iGAog-EpPSP2D8l_qG7jDhK09jP_Zv0bee5TpUNzhuM4SdRprEggXFnR2vUtiWUE2W4igfllpIXMtPJfVTFrYz7hRlbDnwdpNmAORTcIDaMFs4vVZtzCzzPMUFnd1pAF5YRcOizDzSqBXqnB_51K7KoicHVhEzhmt_1lW5SkUWyu8o4PfiCqk4jCZ-2GqQbq097HzUoGgrFjPMay3pXqIcMzFmrcLPrGjyRUQb9MnjKK0VSioVlU0dGtXr8foIV8PW-WjKct5l-orJU9tQ9W5VDmtrIeiWS5NJdKIZ1FQJOf8yxl5ciP_CZ5Av6DvwE0LrR25yJXmRhUBwvqUETftafnTj4SZW7h8PsNmMShHsBi4tlLU6xBF-wwm6UIUvakbtvRAmaMy8H3q60J15eoRwLKYQeWVBOBF7Mu5de-BbZnlCZk6EaQY5BsLE',
        'ASP.NET_SessionId': 'zexfp2xdpnplwkf3msb2kchw',
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json; charset=UTF-8',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'XXXOClmoOot=A8_eh-eBAQAAujJMS1HuZg6O1wTXx4Uas1waWEUQ384u6LSoKB7dT7GW6H3FAV1Ubbmuci7ywH8AAOfvAAAAAA|1|1|c214c8cbf0e236f4b14ff8814432a13e2f4b8686; OClmoOot=A8_eh-eBAQAAujJMS1HuZg6O1wTXx4Uas1waWEUQ384u6LSoKB7dT7GW6H3FAV1Ubbmuci7ywH8AAOfvAAAAAA|1|1|c214c8cbf0e236f4b14ff8814432a13e2f4b8686; _Culture=1; BIGipServerpool_prenotami.esteri.it=rd21o00000000000000000000ffffc0a806e8o443; TS00000000076=081e1ab290ab28006f16783944cf6b4ef41d7b510660dd845245fd98ba9e8f4ebf9e8d1c7f5efccc9d7f25dce1f474c408a4ebe5ea09d000430d6b006f0418b77212973f99723aa9f4b8524ee1baef838bc12b89d0e1ee8c9083d3d8939e4a3b93262a79aab420118fab7530aefe4499ec48b923fbfb7b3e50e2ad6fc6ef8c3b7b527d69f3b15bcae0c3f5f7a6d27a5ba976a7300d66e4edc70535a874fdf7996e8ab690861b260eafd99514bcdf31f7927d8e30c30f228d83bc03a1e17215f77bf8336bb6ef7cf32f5a84c23aafde437c9a7c642be288553408e3c059a6a3e0020a4fe52a5e7a7b295bada57d85ac9f25573b7d29c53c48f3ce6f4fd1b97a7d9d258ef7915b7008; TSPD_101_DID=081e1ab290ab28006f16783944cf6b4ef41d7b510660dd845245fd98ba9e8f4ebf9e8d1c7f5efccc9d7f25dce1f474c408a4ebe5ea06380052e7fd5e9bb52456d015b01cbbbe60982583372d70f529788a7113046e0cac211bd09ef75a5bc94972042c453df509b9377dba87ce40a153; .cookie.=DXJIxnODCcoVVe6qtFIcFh3GcYb6Z0hMUjhJSISWDJWQMIQmYBKwtRELCX_pcQxYDAKWi5dxOxxjYRUhDK8Ol86zaZn3RHJoHwZOeL1ZOd5FPE-wSHC5rtfvfHIOLy6pp3Q0SySyXZUD625inoEim8KmsWsXB2oUSbhAid0frlgdAnbPtMT9tvJjl-zguR8W0Qxuo8YGpg74B7KSt0TRl1t7cPF_5nAk0Vzj1mZTJEslqPdO40aDpuj4gfKb_xYk6Fjfv-024iCY9Ju7fvoRHX4zM3S2AZqLzeyGWI3dSVsdC1rW69TKfB1TwWZlTHorvJj3nG84GdBB9ioqzAUn39aUEsj6wgK0HJUF_BRd3rbcMdYSm4vjDoK8F5pqSUCTFRPLveU4ApFkfLW0plojBT23uX4oEcaCC1sn22UdohxSSARNozc7Ug53VgOfX7ayDOGfTQnB1a3Hdf_EJRvJIz3kRIv2omE4-_jBKo-UVaxLKmnmMmFZIt6PAqAWS8Dgzblq4dyTJltdq6Gvu5ETCgsIY3cPHE7_LSX0UNLCGaCCiHt4icbTt6LsfjwCPxcJpkXsZ1Vce9OHeOZ_OHU_evr3xFROCt_iH-gLAiFspy0; TSPD_101=081e1ab290ab28002d716c8952f53953b3d22eedc6bdb9ff0659b69bd582038d422b984b0bb83ebca3ca741b4a052265084791b66a051800f3e59ffbdd209d79d8f3de04574bf4f5d8097ff00bffc96c; ASP.NET_SessionId=zexfp2xdpnplwkf3msb2kchw; TS01a5ae52=01500ad820a3f82bff3c56b1e13993bcc2b4846e199e69cce5adcb1293344f568180e8a2603a7c27ba65e209b424753efb1fe56de3846e369fc5ff2b33d9c8fe06c8ac53e4977e962142f3671291c818dc558ef6570e16881e561d7a87db291e534c5bd871acb82898069ec019ad37266bbcc171f6; TSd04043d8077=081e1ab290ab2800a73a21bb64500a0559d8934cc476490ba755ecc657bc3a2b0aff4297a563db7d3df5603a5ed2860c081ac3a0261720005099e16c74a7c9b0e5cdcc53a33afbe67b1afdd11db45048457d7c96d880907c; TSd04043d8029=081e1ab290ab28004722fe494c1922e1008b37cd08eece31754c1b73a578ce62a4bb58128003db3697919a6d5d0b6d6f; TS203332db027=081e1ab290ab2000e9d3743b3d27c7a3e300e02996a273a8b0f7570056d94c3148ce09623ab0eeea08379614021130001d6d98a1be1a7a040b8966d4fe448c218cfaf4770b244772a216314b5366f05ba909af40288700fd160808a81f681001',
        'Origin': 'https://prenotami.esteri.it',
        'Referer': 'https://prenotami.esteri.it/BookingCalendar?selectedService=Visti%20per%20Motivi%20di%20studio',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    json_data = {
        '_Servizio': '163',
        'selectedDay': '27/07/2022',
    }

    return requests.post('https://prenotami.esteri.it/BookingCalendar/RetrieveCalendarAvailability', cookies=cookies, headers=headers, json=json_data)
print(get_dates().text)

while True:
    try:
        print(f'{datetime.now().strftime("%H:%M:%S")}: {get_dates().json()}')
    except Exception as e:
        print(str(e))
    sleep(10)