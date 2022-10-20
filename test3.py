import requests

headers = {
    'authority': 'konzinfoidopont.mfa.gov.hu',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
    'content-type': 'application/json; charset=utf-8',
    'origin': 'https://konzinfoidopont.mfa.gov.hu',
    'referer': 'https://konzinfoidopont.mfa.gov.hu/',
    'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
}

json_data = {
    'callId': '1b1f9719-7541-464f-bd9d-2f6a216ae4a0',
    'data': '4wE5UyviATlTHk0+R4bRohf6vTQjTT5H2DYTjF8wqHWZMW+JENOGRz5SHlM5dVFsnsEiTT5H6jIWeE5x6Q8n2NNbP53bnPFYI6J2BOIBPFMeTUpHhtHkhmkonZGbCml7Bz2YRz5NL1M5AUV2rMeNuqO52TYUjWMgmWx4wfoXoj/ntKNWHlM5Y0tzrbtirrKsi9GiF18qlYygyfoXokHrubG8jKGubkRmq14eTT637kAQfEgyoYWZLwIXotHyqKy0k7SgZu4BOVOBvKyt70MPeG4mo5FBvfoXFTbyrKHBg7d8YlVmrFweTT6s/kUUeD4eqIQ9vfoXFjrzrJG1g7itA+IBObyCUD5HhjUHgwC9NCOZKG99CzWPRz5NkbSvZidzq8KQUj5HhjoVhGkhOCM0vWZ4EDiORz5NgZaobk9mp8c1TT5HyUYVi2kqmZWHImyNCzTrip/Ag6eycUcLOVMeTz5HhjoGHPq9NJmVKW98rdGGR6KykbaralJ1osKMUj5HhjgUhm8tQiM0vV+PC0T6rLawisisalFvQ1MeTauo/kEHiW0sopY/vfoXCUP1vK6ygraadEcLOVMesKas6TwHhFsmoC40vfp8DzLvs6zCi7Wec+oBOVORwqCK9UYQiwO9NCN5NW6JAxr0ra1UHlM5GOIBObZ/wKOb/0EHZFsrmISoLGyQ5jL6qIeRKFM5AUVirLhyxq6szxWmF/q9ooShIv8XotH8qKrCg1g5AeJmq8WNv0ZHhtELikgyoYWZLwAXotHzqLajf786xau5DSC8hX/SwFjpk6juCy40vfpgGDL0trRtZ8mab+MBOZsnWEH9juaiF/ofmY+jMyiDFzX8sKWNi7SibRBkqMAfTT5Ht96iF/roZ1pp7y9O0gi5em99H5+L/kBW4bFr810dTczP6ae9NSM0ve6oIo2uyCqOoj5ytrB7znR3TT5H3JRPkW8qn+bdL1+DBz6zZ6a8kcazxJx1/PSUEPhnvwHChVsto5FUMb3RDjqmu5+/khbse01wnRa/wKdn8ZRLiV8pmZBU5W54FEW0rKy0g7f8qk56WYA+kWdHhtGiGPu+PCM0vfoXotGHRz5NL7JAecuzS5zSAe2DSVYVWO5OtN9cPuZYJry//AzHs3RJAeIB/O2SuaO9SXoON20398ShHgMXotHHqXCDVoNyNBUBOVMeTT5HhtGiF/q9NCM0vfoXogUAAAA=',
}

response = requests.post('https://konzinfoidopont.mfa.gov.hu/api/data/GetAvailableBookingTimes', headers=headers, json=json_data)
print()