# Kütüphaneler

import pandas as pd
import requests
from epys.ortak import *


# Genel Değişkenler

first_part_url = "https://epys.epias.com.tr/"
second_part_url = "reconciliation-bpm/v1/"


# 11.40. KÜPST Detay Listelerinin Görüntülenmesi.

def kupst_detay_listele(start_date,end_date,period,tgt):

    """ Yetkili kullanıcıların KÜPST Detaylarının Listelendiği Ekranı Görüntüleme işlemidir. """

    start_date = start_date + "T00:00:00+03:00"
    end_date = end_date + "T00:00:00+03:00"
    period = period + "T00:00:00+03:00"

    particular_url = first_part_url + second_part_url + "reconciliation/sbfgp"
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
        "period":start_date,}

        response = (requests.post(particular_url,json=data,headers=headers)).json()

        body = response["body"]
        content = body["content"]
        items = content["items"]

        table = pd.DataFrame(items)

        table.rename(columns={"effectiveDate":"Tarih","version":"Versiyon","region":"Bölge","powerPlantName":"Santral Adı",
                              "powerPlantName":"Santral Adı","settlementAggregationEntityId":"Santral Id","mcp":"PTF","smp":"SMF",
                              "settlementBasedFinalGenerationPlan":"KUDUP","upRegulation":"YALM","downRegulation":"YATM",
                              "expectedGenerationPlanForSettlementPeriod":"BUDÜP","generation":"UEVM","settlementPeriodGenerationPlanDeviation":"UDÜPS",
                              "secondaryReserveImbalance":"SRDM","deviationVolumeFromDailyGenerationSchedule":"KÜPSM",
                              "amountResultingFromDeviationFromDailyGenerationSchedule":"KÜPST"                
                              },inplace=True)
        table = table.drop(["settlementAggregationEntityName","rowId"],axis=1)
        table = table.reset_index(drop=True)
    except (KeyError, TypeError):
        print("Hata: Veri çekilemedi.")
        return pd.DataFrame()
    else:
        return table