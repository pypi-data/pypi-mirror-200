# Kütüphaneler

import pandas as pd
import requests
from epys.ortak import *


# Genel Değişkenler

first_part_url = "https://epys.epias.com.tr/"
second_part_url = "reconciliation-imbalance/v1/"


# 7.5. DSG Enerji Dengesizlik Detay Servisi

def dengesizlik_detay_listele(start_date,end_date,period,version,tgt):
    """ Dengeden sorumlu grup üyelerinin enerji dengesizlik bilgilerini döner. """

    start_date = start_date + "T00:00:00+03:00"
    end_date = end_date + "T00:00:00+03:00"
    period = period + "T00:00:00+03:00"
    version = version + "T00:00:00+03:00"

    particular_url = first_part_url + second_part_url + "imbalance/balance-group-organization/detail/list"
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
        "effectiveDateStart":start_date,
        "effectiveDateEnd":end_date,
        "region":"TR1",
        "version" : version,
        "period":start_date,}

        response = (requests.post(particular_url,json=data,headers=headers)).json()

        body = response["body"]
        content = body["content"]
        items = content["items"]
        table = pd.DataFrame(items)
        
        table.rename(columns={"effectiveDate":"Tarih","version":"Versiyon","region":"Bölge",
                              "organizationId":"Organizasyon Id","organizationName":"Organizasyon Adı",
                              "withdrawal":"UEÇM","positiveImbalanceVolume":"Pozitif Dengesizlik Miktarı",
                              "negativeImbalanceVolume":"Negatif Dengesizlik Miktarı","imbalanceVolume":"Net Dengesizlik Miktarı",
                              "positiveImbalanceAmount":"Pozitif Dengesizlik Tutarı","negativeImbalanceAmount":"Negatif Dengesizlik Tutarı",
                              "imbalanceAmount":"Net Dengesizlik Tutarı"
                              },inplace=True)
        table = table.drop(["balanceGroupImbalanceVolume","balanceGroupImbalanceAmount"], axis=1)
        table = table.reset_index(drop=True)

            
    except (KeyError, TypeError):
        print("Hata: Veri çekilemedi.")
        return pd.DataFrame()
    else:
        return table