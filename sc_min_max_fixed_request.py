import sys
import requests
import json
import pandas as pd
import urllib
from sqlalchemy import create_engine
import datetime

def setMinthreshexpdt(date = (datetime.datetime.now().strftime("%m") + datetime.datetime.now().strftime("%d") + datetime.datetime.now().strftime("%y"))):
    #set newMonth to 3 months from now
    date = str(date)
    newMonth = date[0:2]
    newMonth = int(newMonth) + 3
    newYear = date[4:6]
    newYear = int(newYear)
    
    #check to see if it's past the 15th
    if int(date[2:4]) > 15:
        #if yes, add a fourth month
        newMonth = newMonth + 1
    
    #make sure the month isn't over 12
    if (newMonth > 12): 
        newMonth = newMonth % 12
        newYear = newYear + 1
        #if we're still using this script in 2099, here's an overflow catch
        if (newYear < 10):
            newYear = str(newYear)
            newYear = "0" + newYear

    #gotta make sure newYear gets cast to string
    newYear = str(newYear)
    
    #add the new month to the date string
    if newMonth < 10:
        #make sure there's a leading 0
        newMonth = str(newMonth)
        newMonth = "0" + newMonth
    else:
        #no leading 0
        newMonth = str(newMonth)
    
    newDate = newMonth + "01" + newYear
    return newDate
    
'''
test_doc = pd.read_csv('min_max.csv')

prod = str(test_doc['prod'][0])
whse = str(test_doc['whse'][0])
orderpt = str(test_doc['orderpt'][0])
linept = str(test_doc['linept'][0])

params = urllib.parse.quote_plus("DRIVER={SQL Server};SERVER=pssapps21.psscorp.local;DATABASE=TEST11NXT;Trusted_Connection=Yes;APP=PDSPS")
conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
engine = create_engine(conn_str)

df = pd.read_sql_query("""
UPDATE TEST11NXT.dbo.icsw
SET orderpt = """ + orderpt + """, linept = """ + linept + """
WHERE prod = '""" + prod + """'


    """, engine)
'''

test_file = pd.read_csv('MM072921.csv')

api_url = "https://xiplatform.us-ad.pssigroup.com:7443/infor/SX/rest/sxapirestservice/sxapiicproductmnt"

def get_token():
    token_url = "https://xiplatform.us-ad.pssigroup.com/InforIntSTS/connect/token"
    client_id = 'infor~13pvMbvD5T9qS_YI8x57t2lCQc6-IgNFmXUDoR6isyM'
    client_secret = 'wmZQCUcT89ONt-2Pyo6n_Ycn_SZAMgOoAfGgjFXTXv3cP0-TTgJRrfcYSsyzuxvqDo9KErSqRgTpWzsAbspBcg'
    client_user = "infor#deyVx327C82gWLmviqlUfITddHAnq0BV-MBEzTIl3DUlyb057qV62oeA18P_Xx6bJVLydSWapeDcgSv3pGtsrQ"
    client_password = "dnggAuY1Ey-uZfD3b2Z4nd_ktVyZsEtVbM3tO-84GQ6-EWiH-JF88YY_C_JrT6mE9XUJasNFi8gIoLiJZ_x6xw"
    
    token_payload = {'username': client_user, 'password': client_password, 'grant_type': 'password'}
    
    token_response = requests.post(token_url, data=token_payload, verify=False, allow_redirects=False, auth=(client_id, client_secret))
   
    print("Successfuly obtained a new token")
    tokens = json.loads(token_response.text)
    print(tokens)
    
    return tokens['access_token']


token = get_token()
for i in range(len(test_file)):
    prod = str(test_file['prod'][i])
    linept = str(test_file['linept'][i])
    orderpt = str(test_file['orderpt'][i])
    whse = str(test_file['whse'][i])
    statustype = str(test_file['statustype'][i])
    ordcacty = str(test_file['ordcacty'][i])
    orderqtyin = str(test_file['ordqtyin'][i])
    threshrefer = str(test_file['threshrefer'][i])
    minthreshold = str(test_file['minthreshold'][i])
    if str(test_file['minthreshexpdt'][i]) == 'nan' and statustype != 'O' and statustype != 'o':
        minthreshexpdt = setMinthreshexpdt()
    elif statustype == 'O' or statustype == 'o':
        minthreshexpdt = '?'
    else:
        minthreshexpdt = str(test_file['minthreshexpdt'][i])[:-2]
    frozenmmyy = str(test_file['frozenmmyy'][i])
    frozentype = str(test_file['frozentype'][i])
    frozenmos = str(test_file['frozenmos'][i])
  
    companyNumber = 1

    api_call_headers = {'Authorization': 'Bearer ' + token, 'Accept': 'application/json', 'Content-type': 'application/json'}

    # key1 = prod, key2 = whse, fieldName = icsw field
    request = {'companyNumber': 1, 'operatorInit': 'ehr', 'operatorPassword': 'ehr700', 'tMntTt': { "t-mnt-tt": [ {'setNo': 1, 'seqNo': 1, 'key1': prod, 'key2': whse, 'updateMode': 'chg', 'fieldName': 'linept', 'fieldValue': linept}, \
                                                                                                                  {'setNo': 1, 'seqNo': 2, 'key1': prod, 'key2': whse, 'updateMode': 'chg', 'fieldName': 'orderpt', 'fieldValue': orderpt}, \
                                                                                                                  {'setNo': 1, 'seqNo': 3, 'key1': prod, 'key2': whse, 'updateMode': 'chg', 'fieldName': 'icswstatustype', 'fieldValue': statustype}, \
                                                                                                                  {'setNo': 1, 'seqNo': 4, 'key1': prod, 'key2': whse, 'updateMode': 'chg', 'fieldName': 'ordcalcty', 'fieldValue': ordcacty}, \
                                                                                                                  {'setNo': 1, 'seqNo': 5, 'key1': prod, 'key2': whse, 'updateMode': 'chg', 'fieldName': 'threshrefer', 'fieldValue': threshrefer}, \
                                                                                                                  {'setNo': 1, 'seqNo': 6, 'key1': prod, 'key2': whse, 'updateMode': 'chg', 'fieldName': 'minthreshold', 'fieldValue': minthreshold}, \
                                                                                                                  {'setNo': 1, 'seqNo': 7, 'key1': prod, 'key2': whse, 'updateMode': 'chg', 'fieldName': 'minthreshexpdt', 'fieldValue': minthreshexpdt}, \
                                                                                                                  {'setNo': 1, 'seqNo': 8, 'key1': prod, 'key2': whse, 'updateMode': 'chg', 'fieldName': 'frozenmmyy', 'fieldValue': frozenmmyy}, \
                                                                                                                  {'setNo': 1, 'seqNo': 9, 'key1': prod, 'key2': whse, 'updateMode': 'chg', 'fieldName': 'frozentype', 'fieldValue': frozentype}, \
                                                                                                                  {'setNo': 1, 'seqNo': 10, 'key1': prod, 'key2': whse, 'updateMode': 'chg', 'fieldName': 'frozenmos', 'fieldValue': frozenmos}, \
                                                                                                                  {'setNo': 1, 'seqNo': 11, 'key1': prod, 'key2': whse, 'updateMode': 'chg', 'fieldName': 'ordqtyin', 'fieldValue': orderqtyin}]}}
 
    payload = {'request': request}

    api_call_response = requests.post(api_url, json=payload, headers=api_call_headers, verify=False)
    
    print(api_call_response)
    print(api_call_response.text)