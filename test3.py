from datetime import datetime
from time import sleep

import httpx

with httpx.Client() as client:
    r = client.get('https://prenotami.esteri.it/Home')
    print(r.text)
    print(r.cookies)
    [(cookie, value) for cookie, value in r.cookies.items()]

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # Requests sorts cookies= alphabetically
        # 'Cookie': '_Culture=1; BIGipServerpool_prenotami.esteri.it=rd21o00000000000000000000ffffc0a806e9o443; _pk_ses.E1e0Ge2p6l.5f67=1; TS00000000076=081e1ab290ab280073b323c21bf5f417925f9c8424aa1336d75bc9eaafb4242ae2dfe65755151d7fc5aefea21df72c4e08c321d8a109d00032d2c40cd80ccb3d109f403484975b0462d3af0403c92b51f6d78246555c2341f9b7b9c46bce9c4aa156de60e099be9f8ce8e1260ec921424bb1500bcbc68e873b093bc2c5fe303a2333bbb844dae879dbc088d1fb3b86343fe9c5349c00293b9509a2426b851b2f9f393fbfad67bd5e0a2b3704e0675223f7bc5053f924cf14374f09cf12d3f2ab2c7ec0860acd9c91166fa11dd756cd18ccfe3bfcd97cb104ff571bb5ff8461e4a6c1482e788f56d4b682297c10a88b32af0fde8461555bf8c5137f6f1e9553c574d432b1f16c24d6; TSPD_101_DID=081e1ab290ab280073b323c21bf5f417925f9c8424aa1336d75bc9eaafb4242ae2dfe65755151d7fc5aefea21df72c4e08c321d8a1063800aa41e13529a6106aa905362bf36c7afe8782ab3529312a975ccf20f5b526db4a3ae40776776bffd6543616bbdd906fa610d0d1d7a64a66a7; OClmoOot=A3d3JJeCAQAAdCkdDIqYqjVgWR5Ts9fwKr1eru49HPpi2JMIJQBEhMldkn1sATarpwSucm46wH8AAOfvAAAAAA|1|1|d6f69c22129f9efc74357687fd32054d313df7f9; TSPD_101=081e1ab290ab280039499218143989c9e9b68be00d8a30d172678866bf69575713aee73fa08eea02510b60ac8c84b4cc08d8b4e52e0518001435d6d2cd9efdfed8f3de04574bf4f5d8097ff00bffc96c; TS01a5ae52=01500ad820575e76ad8fa52c929660367cea810e98d0c9b8e75d1cb36c0c1175a1712f18e879a0fce009192eb039b32761cfecf82bd5e10f3962a7435f4887b3fd7c980c70d2bf41b3f4286cbd1dfdf9d256b4c7223ed9ba82788060f087531445ab6bd87da16eba8b98b83bd9f11ad429203c9da0; _pk_id.E1e0Ge2p6l.5f67=072f85d922783314.1660393127.1.1660393386.1660393127.; TSd04043d8029=081e1ab290ab280011937663bb1f2f8c5672a2d875bed6fbee7230c804e9edd2c5b2b7c1debf1ce12ae880d80a65ea1e; TS203332db027=081e1ab290ab20000d31398766e54bdd8f0a17a938bfae453608136ee25b16622ae55b43df0b419008abe8576011300092751b72052bdd9719fe28944224ccd1e35e5f6a968d6264596d3d5ae78d08ebcb1338a740c9f0d3b61832d453664b7d; TSd04043d8077=081e1ab290ab28002fa6482a54c278b0b89f6741bcfecc5926c3f71ece4d7f470065dbf3e8d14045ee6d9cebf8c363b908b7a061ef1720002805f8dc008c4bf920c08513967a8cc4bd3ca2e9a1bb5c5fe51fc21374cedc90',
        'Origin': 'https://prenotami.esteri.it',
        'Referer': 'https://prenotami.esteri.it/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    data = {
        'Xa4vrhYP3Q-a': 'y0B8hex4LcsnCzjdrYMz0JIihl3ny71t4dxJv7PrT7NcKEHoBe4M8zOc=1XbHsiM8xfEuTibfOobMbckuwuHr-WWM9MNh3b0701GQlscysDsR3nQ2zPk8yi-HyW7Sz6xyEKQE9iKr6kAje243ISVxFUS9XwVEiVboblAeMtFvRfXwz0l74YbvWnvcH0jpXAKtyNrqQY5iqMO5Rn5vTQJ_m2t4NfCDTXohxFRcDVW2pxRMTwURoe2Ds5=jp-LEVJnTt=9yb_KvjWDlcrvQwStF1NYuRdqsGoPUctvfN9Yhk9qzkbf9-UxIRe0lTCcRr2Kk0eyJ1t0r27CmC6kWei=wMtP=EybRj_M3=qWECbr_gq=4GjkwuQS5mCNs-gk6XmaLEc3U27qcdu1-nKOBQ0kRFSVLBDdi37qvdojkYL63FhmvQky_gk3cdyjGOyv54RuuTJ3ckpcw-PEsFmwKwIsrvzNrk3IoW73QloaKeBgdUY-rNrN49gTyvdcdLQwDuowJ-mU=_e7M-yPLtstWPAyTxalBvYjfG9lakyeEH6UVIBO=RzdQu_x3HNRXH=-m2zqVpvHVBfy6b4RRY_W_CEr6EEHUs5XG1AR8dJ3gasjvk4z2BdRtaRs==W_PPPbOIu=mHqPI=VBPjVTRz_LnPG4Fs3Ab8fWMCqjpsntE9fusqM0ShOgnTrqsHjiqmyLhCMYcudO7hQJwwyFSzUbKXWCnbnqpo3pXtCuR__cqbCrqLfHUc3yV6DXpuE8VeSaYnIv4PX91gN1tIPYAXQ7EdDzp0ci44pUY4A2U2ycs0QPg4i1toxQr7_hJHO7TFzJnVXdgA8lyX6riTxLtsld3e4HRXsUaQ3845ilx96_dTGGOtNkEmHvjJmw_EEB_2qt5Fwr3k_HzGqmLgCgkqHh4imXfM7egSihcjgJm2kCYJ=qz4PY2Y-h0zh0bVBmyGLc-H5RPuueBJepwAmdNa4UlWeNbNtMFpe5oNDmt168WWdGCjAp5lN3xu5=suvdNrgJvaTovTH2X-GbORL7=xD_FvOG6dUi6xF_ASxvLnuXgc_y8tAUHFnKB7PfhFWdMy-E649L9vStr56BoG92n5IvKBbB7athQhtYsMWKFzxfyTfhHSGLURoNj8LPvJOqXuhlX5O5YWD4yMdgrc-fNQR2l0QkXciTfywILLnw2QUcQwMOn_kE7a8_-HHV3MBVrGJY0Aan0IcGEuvE_0uCXhbaKpjhmXaoFj6TI5kJp9NN0mAp55H_8bQEm=pwp99LIgTS1hdeX7E1Tq9x2LOIFKLYu5enfR15cyGL-QSL70fQycv3p3TYnBH2TuFp7D7cs7-L3AqfR5P2E0pszhl01sDRsBzyr0evh8_9EmknmaOxc4DIMyNPTQBjJSJkr0OaV4W_f9Fe9L9FJKeJt3hg4Ch2pOBaHgbXMp=lrMBW3hV23_4LbGOQ2HJJywBDKjLxUz6YtsxticmFDaHTv8BXWumn9Pu2zQC_M6KCSoKrXfrJIGDeS_YJUUv7CKi5ECsm=E9j9S_4si76W1V4DQP6HkGIYAyGfPxGcxEzDtNUu2mK_B=kDXkdsURLwMUD7zFCO2bcAmmGkvE3bGuXtawChnV5Ce5n0dUWjTK_fpyvdBU3gxiskyEbXdi8yNbDJa2Ew_cWkzrWyzspCh1nGT3WLgqELwlUmUeApo2Qve0qEh3oPgTKi6Pb1ljAij0n5m9NT7O4paO1SGB6vilRKSklLWkj1iyEuvDDLdOoGqmraK9KMkhRty9gB-kMJkhxkzxivJulp_jvD2ygzxrqvaXeU5sI3xeFYuhCuFmDLWVve_V4h8nsMPMmbM1y2x9PiADHavsjETw6wEEQ_qSYW6HgevhmEfvO9RTnMkCT86Ti=K6jz5Dy54GdHF=N0plimMXbsHtijq062b2QKO2ifrmtDSQGlePFGPR_1_pyxIWgb5LHYFWBsEkEoFSGcAgTxUk4oHYpB8oIkv=RR77UKTq-14BEAMORzL8FJ7PUR6FYRQ_bhW0iy26VlH1tLvVMPsPt1BP0TM2Dh_weWs-yrHB-V4fU_s=QuzGLFYtW3Q2RKSSEd=18StA=-NyCFHNHEtg4rgt8M2qnn2A82wd8hN_Mjq321l-s1MS1ICLnV-PEg_FRTzAEt3TwzCSUVhbJIx2nmoTi-wIIpN16GIG=12gKhetWfvjamRk3wl2L6mlAOl8agFl4EgbnOGEPEBbJ68FXtKk0xn5Eoy1W7f2Kdag-vwIuebrbBAa9YpD2w_cwnHVleSMY0-RiCxxMJnxGL-DSysJ7=JHb3Qc9uFerIYKq7NHf1ivvm1i7oLeVJrkX_4g9VEoSf38BMkdu70N0=bNfx3s0GyLYGcjqoI_62pjYqqScwxKTiEp9G7Bj7e8cOJBAip_eMU_i4eJJxr7w3F8gl0mvLOqdhTNjnp5EN7uExgJHo73pTFfUCmlw0VmN9GBXo_vSnCjRCTYbMknUgoRx4eB6OUrA_wMjElL2dYuMSUh-HkMqVwikinmHcpJQ3ithbSHdLgLjXvEqycHe1LEMXB39axdP6Qg5VVRM74WyjKCKKj-sLoOD6ajT0Wou4KJy6wsa0HMuTzD2mIDh1hkdfYaiSMKSLMRfV6oHYNdL1TwDzX1Yd9O3cu6KJRnhOTaUyTP8QcrjlFYUl5e-DXxfgbtqNGauxyvBCKgI1aWT3qfctVjqtfuaKqlaM4SkbmC9GfA2--uzU8AOQglFr3QLB4Crk8G9mjgKc-UNcQMHf=QYV2YVpHLrB4CLKEh8nEjJjySNu_CH7WXLcf0mn8hkln0kSX4l=7s5svrgfkdqAX6LRuve2Bm8DR=05rnBac8U3lgiIocfJGWsV8yih5tiGGvYot6MGXgTaMMh1P54LewQsa9DPsbnItLnq5Xz-2v-uMuFplAR=xPr7jTBkb1yNXesGGixbbftNMEIUdMlnHY1kFOq2TDDvq_R4hzGpl_9BDpcDqoIeJqCYlPO4tf_sTyA-vSD=87B3Uc6U5nkQCYsS6rkD8SQg9jzLCESYGuMMU4DSG4vlXNgVLP9fqTqg9z6R4Stg3MpN=BYmTxM7aJuOMs7fVRjlMioVROJ0inex1WWkWYpdR2usK-Huxtc4SwPk7kPkiBq=_y9YhwIHcF9aUN0C2wvBDAb=OiajFUyrG42k3tMRt92h7UKT7FPywV-Dtk=8HjfbODk123o4bCAy8W4BF-ke_8de8ghRpMu=zS-SVWk8txjSLNJzJapmIYFh2540B5veebg3uX2JuQXQRRmdbyIsYyJeYbvpimFi30JptR-dKtPnYsoN=ltmmtc6nzKnkbEMKnUymotPaEKMaxb7QsKHjDObmoR_3zOij0L=PzQLSm4eV=2Ybsjz9S3MBrIFTxGxdA-aUuBEkTyCXFDRxr8i7Ou-oXYGhzCmfwc4A-fCh9O6EWcwiKq9vWthHnwxf54dXnja14X602n6gKB-9ufDxnrla5yPns5abPBNdK_MJqfcOMIhP6zUaXUXkItdsnV0hnJo-jzpa-iceVAjnJ=8MhBCRB0eaXtYnMsjJFS47kFVeWh7cBJAFvGCONHpR=yhb_hBgYBSGTNGzWb85NabgXxzIrQpLIXXGob5OlPrziwfSAhzDL1cjItYkzTjL65k7PG0HWToXyyv4oQhoPmuyQPUaBuX=PxJL0G42a0GkLiEDanFVv76R3oq0FzLjIs9rSQsvMShPUlYC6O113NOrwr3q6Mz7c5g62c79yGqz4Be08YP6faMM68YXyb=W-Nsz8=cTx92PMojHUuGgyYc3Ps4v5BQYTnTCxAfQS6ylBJF8A=WMG9IJz42-dA5kJXB8xxz_9O7kTFxF7FUs=CPh35xqCEc03naywEzjo9wgsjiGkUvc9bIlrYssyoWldpCbOvLrTiBXNtsVql7CD3Jqp0KoxWbtOlLeGquR4G1xYCHd0ab3OeOnb4BEJx8G=CJ36dlHOP4Lfp1=QmY_rySyj_7Xptxl9dOp3nfUAt8UybDdw-cJA3cxElG5lJaTc9Y77OFiNd5VTiLEweFU7W7kowM=kedz=LR6RlC2ytXJ97vNf7EWYh-psP7zUkPkqwCG587MP9N7=d6_sxhCxgm-tAk0mu68k5uRdrX8tdsvD48cI_LmazLeu=D87dHJH55j_Od_QTavDYPgP7STDWIK7vsIHjf0eT33uGPR9U_oEhUeLAxgg=IV14VzR2wqxjM82ymQcIS1l7Jt_ok1dukLf7dlU=oYvwmY-SBzU6qmPFnEaucxGf7mM8pnbadH2EqgaCerEOo=fDrgkJBbaHex5n-7jeM0XhYsW65jGw3qilfSRMXlUhnmV30vh7jWkCyl0gFOfDLpBYPJCj0ugNj3P3VPsG2D753BEDHH9OUGGllpnYrKQ2cOSnylLObELncR-lozMsIPIOr1cPbu_Caux36Va6z-dnyyAl2DxCwcJwGrriiN1ctcXbh7JLFnng9pWfWjyATJOKiJ9NmRaQIXdUkiqxE9iKPQ23uhWT3Rc0lFieITjW5XXwOHuzkpPQG8NQDTgqz-r1CIzgBKb04O53O8nvcc6lnnbuuf3VmonMTEah8SKdBBOu_V9cLY2t-eIvnlLooU3f_Hl=CPne9yKancpyU3B6Fx5AMIlqSgq82iO2rWNm_LuvSiJdOvejct1M_Cu71zPygFVK-TN3t3NQe3jc998Jt64kv2wf5xLSbeoMcWpt94qrc-R6mC8Ihhn_aeEKTDBs4TDp9aW7=BUl=dx=vgKEM3EvKjfuTneGI2eAeU=kiXmy9tm09eaQP_pvznspYHA-diTY36dQPWYxlmAwGGJuLlr5xorznjqUG=gPOMW0G63flXmNil-9IFV9I4t8wfrQUfuN9x8f7gtPkrERz9_6-FHyiKuG5==dN49UhNp68hivV_7ytmb2AKzTvsyimR69uscV7_NiN__d_YoGQmptO9_ARGEASdouPE_cY8A-xSCVgHWwTM3qdvumWQWhiAb91gQLmkgrt=0pr0m4-=6Apwm02sO6sSSPDwqM68HSsEl6F3s4TeIWjkURoMoEl8JWbOIvBJCdTAumGrmT3I0jDovywirFC0tcDr',
        'Xa4vrhYP3Q-z': 'q',
        'Xa4vrhYP3Q-d': 'ABaChIjBDKGNgUGAQZIQhISi0eIApJmBCgBDIXFqYI2QAf____-o31dSAtbl0biEa8pawZoUFBCeUMk',
        'Xa4vrhYP3Q-c': 'AICZJZeCAQAAFCXgQIFVNbomiSLrDEnxpPxhTe0FDZe5oG6z80MhcWpgjZAB',
        'Xa4vrhYP3Q-b': 'cek9an',
        'Xa4vrhYP3Q-f': 'A2lzKJeCAQAAoClPlHU6ozAE-05cHFJaxh3q881mmqplJ3iy_2diOo1_IGRQATarpwSucm46wH8AAOfvAAAAAA==',
        'Email': 'sash.kardash@gmail.com',
        'Password': 'Ab123456!',
    }

    r = client.post('https://prenotami.esteri.it/Home/Login', headers=headers, data=data, follow_redirects=True)
    today = datetime.now().strftime("%d/%m/%Y")

    json_data = {
        '_Servizio': '1090',
        'selectedDay': today,
    }

    s = client.post('https://prenotami.esteri.it/BookingCalendar/RetrieveCalendarAvailability', headers=headers, json=json_data)

    print(r.text)

r.status_code

r.headers['content-type']

r.text
