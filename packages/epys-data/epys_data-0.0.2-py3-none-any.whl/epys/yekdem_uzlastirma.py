# Kütüphaneler

import pandas as pd
import requests
from ortak import *


# Genel Değişkenler

first_part_url = "https://epys.epias.com.tr/"
second_part_url = "reconciliation-res/v1/"


# 12.42. UEVÇB Verileri Listeleme Servisi

def yekdem_listele(start_date,version,tgt):
    """ YEK uzlaştırma detaylarının dönüldüğü servistir. """

    start_date = start_date + "T00:00:00+03:00"
    version = version + "T00:00:00+03:00"

    particular_url = first_part_url + second_part_url + "payment-obligation/details/list"
    try:
        
        st = st_olustur(tgt)

        headers = {
          "Host":"epys.epias.com.tr",
          "TGT": tgt,
          "ST": st,
          "Accept":"application/json; charset=utf-8",
          "Content-Type":"application/json; charset=utf-8" }

        data = {
        "page":{
            "number":"1",
            "size": "9999"
        },
        "effectiveDate":start_date,
        "version":version}

        response = (requests.post(particular_url,json=data,headers=headers)).json()

        body = response["body"]
        content = body["content"]
        items = content["items"]
        table = pd.DataFrame(items)
        
        table.rename(columns={"effectiveDate":"Tarih","version":"Versiyon",
                              "organizationId":"Organizasyon Id","organizationName":"Organizasyon Adı","powerPlantId":"Santral Id",
                              "powerPlantName":"Santral Adı","dollarExchangeRate":"Dolar Kuru","resPrice":"YEKF",
                              "toleranceCoefficient":"J/P Katsayısı","resGeneration":"YEK UEVM","totalCost":"YEK UEVM * YEKF",
                              "income":"YEK UEVM * PTF * J/P","total":"YEKBED","mcp":"PTF"},inplace=True)
        table = table.drop(["settlementPointId","settlementPointName"], axis=1)
        table = table.set_index("Tarih")

            
    except (KeyError, TypeError):
        print("Hata: Veri çekilemedi.")
        return pd.DataFrame()
    else:
        return table