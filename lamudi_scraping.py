import requests
import csv
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from re import sub
from time import sleep

ua = UserAgent()
header = {'User-Agent':str(ua.chrome)}

lamudi_csv = open('lamudi_makassar.csv', 'w', newline='')
csv_writer = csv.writer(lamudi_csv)
csv_writer.writerow(('Judul', 'Kota', 'Wilayah', 'Luas_Bangunan', 'Luas_Lahan', 'Harga'))

for page in range(15):
    source = requests.get(f'https://www.lamudi.co.id/south-sulawesi/makassar/house/buy/?page={page+1}', headers=header).text
    soup = BeautifulSoup(source, 'lxml')

    print(f'Halaman {page+1}')
    for per_item_rumah in soup.select("div[class*='row ListingCell-row ListingCell-agent-redesign']"):

        #judul di lamudi
        __judul = per_item_rumah.select_one("h2[class*='ListingCell-KeyInfo-title']").text.strip()
        judul = sub('[^A-z0-9 ]', '', __judul)

        #kota dan kecamatan
        __lokasi = per_item_rumah.select_one("span[class*='ListingCell-KeyInfo-address-text']").text.strip()
        if len(__lokasi.split(', ')) == 2:
            lokasi_wilayah = __lokasi.split(', ')[0]
            lokasi_kota = __lokasi.split(', ')[1]
        elif len(__lokasi.split(', ')) == 1:
            lokasi_wilayah = ''
            lokasi_kota = __lokasi

        #harga    
        try:
            __harga = per_item_rumah.select_one("span[class*='PriceSection-FirstPrice']").text.strip()
            harga = sub('[^0-9]', '', __harga)
        except:
            harga = ''

        #keterangan luas lahan dan bangunan
        __keterangan = per_item_rumah.select("span[class*='KeyInformation-label_v2']")
        luas_bangunan = ''
        luas_lahan = ''
        for i, tag in enumerate(__keterangan):
            if __keterangan[i].text.strip() == 'Bangunan':
                __luas_bangunan = per_item_rumah.select("span[class*='KeyInformation-value_v2 KeyInformation-amenities-icon_v2']")[i].text.strip()
                luas_bangunan = sub('[^0-9]', '', __luas_bangunan)
            if __keterangan[i].text.strip() == 'Lahan':
                __luas_lahan = per_item_rumah.select("span[class*='KeyInformation-value_v2 KeyInformation-amenities-icon_v2']")[i].text.strip()
                luas_lahan = sub('[^0-9]', '', __luas_lahan)

        print(judul, lokasi_kota, lokasi_wilayah, luas_bangunan, luas_lahan, harga, sep='|')
        csv_writer.writerow((judul, lokasi_kota, lokasi_wilayah, luas_bangunan, luas_lahan, harga))

    #biar g sengaja overload server
    sleep(7)
