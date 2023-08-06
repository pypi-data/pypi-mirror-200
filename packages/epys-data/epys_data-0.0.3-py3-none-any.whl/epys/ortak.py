
# Kütüphaneler

import pandas as pd
import requests


#TGT Oluşturucu

def tgt_olustur(username,password):
    url = "https://cas.epias.com.tr/cas/v1/tickets?format=text"

    data = {"Host":"cas.epias.com.tr",
        "Cache-Control": "no-cache", 
        "Content-Type":"application/x-www-form-urlencoded",
        "username":username,
        "password":password}
    
    response = requests.post(url,data=data)
    tgt =response.text
    return tgt


#ST Oluşturucu

def st_olustur(tgt):
    st_url = "https://cas.epias.com.tr/cas/v1/tickets/" + tgt
    st_headers = {
            "Host":"cas.epias.com.tr",
            "Content-Type":"application/x-www-form-urlencoded",
            "Content-Length":"39",
            "service" : "https://epys.epias.com.tr"
        }
    response = requests.post(st_url,data=st_headers)
    st = response.text
    return st

