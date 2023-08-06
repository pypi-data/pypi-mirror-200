# Kütüphaneler

import pandas as pd
import requests
from epys.ortak import *


# Genel Değişkenler

first_part_url = "https://epys.epias.com.tr/"
second_part_url = "pre-reconciliation/v1/"


# 12.42. UEVÇB Verileri Listeleme Servisi

def uevcb_verileri_listele(start_date,end_date,period,version,tgt):
    """ UEVÇB verilerini listeler. """

    start_date = start_date + "T00:00:00+03:00"
    end_date = end_date + "T00:00:00+03:00"
    period = period + "T00:00:00+03:00"
    version = version + "T00:00:00+03:00"

    particular_url = first_part_url + second_part_url + "settlement-point/data"
    try:
        
        st = st_olustur(tgt)

        headers = {
          "Host":"epys.epias.com.tr",
          "TGT": tgt,
          "ST": st,
          "Accept":"application/json; charset=utf-8",
          "Content-Type":"application/json; charset=utf-8" }

        data = {
        "page":
        {
            "number":"1",
            "size": "9999"
        },
        "effectiveDateStart":start_date,
        "effectiveDateEnd":end_date,
        "period": period,
        "region":"TR1",
        "version":version
        }

        response = (requests.post(particular_url,json=data,headers=headers)).json()

        body = response["body"]
        content = body["content"]
        items = content["items"]
        table = pd.DataFrame(items)

        for i in range (len(items)):
            item = items[i]
            table["settlementPoint"] = item["settlementPoint"]["label"]
        
        table.rename(columns={"effectiveDate":"Tarih","version":"Versiyon","region":"Bölge","settlementPoint":"Santral Adı","supply":"UEVM","withdrawal":"UEÇM"},inplace=True)
        table = table.set_index("Tarih")

            
    except (KeyError, TypeError):
        print("Hata: Veri çekilemedi.")
        return pd.DataFrame()
    else:
        return table