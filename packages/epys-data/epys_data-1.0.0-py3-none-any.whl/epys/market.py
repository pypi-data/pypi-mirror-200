# Kütüphaneler

import pandas as pd
import requests
from epys.ortak import *


# Genel Değişkenler

first_part_url = "https://epys.epias.com.tr/"
second_part_url = "reconciliation-market/v1/"


# 8.16. GÖP Uzlaştırma Bildirimi

def gop_eslesme_listele(start_date,end_date,tgt):

    """ Piyasa Katılımcılarının ilgili fatura döneminde GÖP sisteminde yaptıkları işlemlere ait 
    Miktar ve Tutar bilgilerinin günlük bazda listelenmesidir."""

    start_date = start_date + "T00:00:00+03:00"
    end_date = end_date + "T00:00:00+03:00"

    particular_url = first_part_url + second_part_url + "market/day-ahead-market/daily/list"
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
        "deliveryDayStart":start_date,
        "deliveryDayEnd":end_date,
        "region":"TR1"}

        response = (requests.post(particular_url,json=data,headers=headers)).json()

        body = response["body"]
        content = body["content"]
        items = content["items"]
        table = pd.DataFrame(items)

        table.rename(columns={"effectiveDate":"Tarih","mcp":"PTF","smp":"SMF"},inplace=True)
        göp_satış_miktarı = []
        göp_satış_tutarı = []

        for i in range (len(items)):
            item = items[i]
            transaction = item["marketParticipationTransaction"]
            göp_satış_miktarı.append(float(transaction["salesVolume"]))
            göp_satış_tutarı.append(float(transaction["salesAmount"]))
        
        table["Göp Satış Miktarı"] = göp_satış_miktarı
        table["Göp Satış Tutarı"] = göp_satış_tutarı
        table = table.drop(["marketParticipationTransaction","efmDefaultTransaction"], axis=1)
        table = table.reset_index(drop=True)

            
    except (KeyError, TypeError):
        print("Hata: Veri çekilemedi.")
        return pd.DataFrame()
    else:
        return table

# 7.8. GİP Eşleşme Sonuçları Servisi(Günlük)

def gip_eslesme_listele(start_date,end_date,tgt):

    """ Organizasyonun güniçi piyasasındaki eşleşme sonuçlarını döner."""

    start_date = start_date + "T00:00:00+03:00"
    end_date = end_date + "T00:00:00+03:00"

    particular_url = first_part_url + second_part_url + "market/intraday-market/daily/list"
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
        "deliveryDayStart":start_date,
        "deliveryDayEnd":end_date,
        "region":"TR1"}

        response = (requests.post(particular_url,json=data,headers=headers)).json()

        body = response["body"]
        content = body["content"]
        items = content["items"]
        table = pd.DataFrame(items)

        table.rename(columns={"effectiveDate":"Tarih","mcp":"PTF","smp":"SMF"},inplace=True)
        gip_satış_miktarı = []
        gip_satış_tutarı = []
        gip_alış_miktarı = []
        gip_alış_tutarı = []

        for i in range (len(items)):
            item = items[i]
            transaction = item["marketParticipationTransaction"]
            gip_satış_miktarı.append(float(transaction["salesVolume"]))
            gip_satış_tutarı.append(float(transaction["salesAmount"]))
            gip_alış_miktarı.append(float(transaction["purchaseVolume"]))
            gip_alış_tutarı.append(float(transaction["purchaseAmount"]))
        
        table["Gip Satış Miktarı"] = gip_satış_miktarı
        table["Gip Alacak Tutarı"] = gip_satış_tutarı
        table["Gip Alış Miktarı"] = gip_alış_miktarı
        table["Gip Borç Tutarı"] = gip_alış_tutarı
        table = table.drop(["marketParticipationTransaction","efmDefaultTransaction"], axis=1)
        table = table.reset_index(drop=True)

            
    except (KeyError, TypeError):
        print("Hata: Veri çekilemedi.")
        return pd.DataFrame()
    else:
        return table

# 8.5. İkili Anlaşma Detay Servisi

def ia_detay_listele(start_date,end_date,period,version,tgt):

    """ Organizasyonların aralarında yapmış oldukları ikili anlaşma detaylarını döner."""

    start_date = start_date + "T00:00:00+03:00"
    end_date = end_date + "T00:00:00+03:00"
    period = period + "T00:00:00+03:00"
    version = version + "T00:00:00+03:00"


    particular_url = first_part_url + second_part_url + "bilateral-contract/detail/list"
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
        "period": period,
        }

        response = (requests.post(particular_url,json=data,headers=headers)).json()

        body = response["body"]
        content = body["content"]
        items = content["items"]
        table = pd.DataFrame(items)

        table.rename(columns={"effectiveDate":"Tarih","version":"Versiyon","region":"Bölge",
                              "buyerOrganizationName":"Alıcı Organizasyon","sellerOrganizationName":"Satıcı Organizasyon",
                              "transactionVolume":"İşlem Hacmi",},inplace=True)
        table = table.drop(["bcContractId","buyerOrganizationId","sellerOrganizationId","firstVersion"], axis=1)
        table = table.reset_index(drop=True)

            
    except (KeyError, TypeError):
        print("Hata: Veri çekilemedi.")
        return pd.DataFrame()
    else:
        return table