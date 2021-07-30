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
    
    #check to see if it's past the 15th
    if int(date[2:4]) > 15:
        #if yes, add a fourth month
        newMonth = newMonth + 1
    
    #make sure the month isn't over 12
    if (newMonth > 12): 
        newMonth = newMonth % 12
        newYear = date[2:4]
        newYear = newYear + 1
    else:
        newYear = date[2:4]
    
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
    
test_file = pd.read_csv('repltest.csv')

params = urllib.parse.quote_plus("DRIVER={SQL Server};SERVER=pssapps21.psscorp.local;DATABASE=TEST11NXT;Trusted_Connection=Yes;APP=PDSPS")
conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
engine = create_engine(conn_str)

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
    replcost = str(test_file['replcost'][i])
    listprice = str(test_file['listprice'][i])
    stndcost = str(test_file['stndcost'][i])
    arpvendno = str(test_file['arpvendno'][i])
    prodline = str(test_file['prodline'][i])
    whse = str(test_file['whse'][i])
    
    sql_df = pd.read_sql_query("""
    select whse, prod, replcost, replcostdt, listprice, stndcost, stndcostdt, baseprice
    from NXT.dbo.icsw
    where cono=1
    and prod= """ + prod + """
    and prodline <> 'clsd'

        """, engine)
    
    valid_whse_list = []
    for k in range(len(sql_df)):
        if listprice == 'nan':
            gap_to_maintain = float(sql_df['listprice'][k])/float(sql_df['replcost'][k])
            listprice = str(float(replcost)*gap_to_maintain)
        if stndcost == 'nan':
            gap_to_maintain = float(sql_df['stndcost'][k])/float(sql_df['replcost'][k])
            stndcost = str(float(replcost)*gap_to_maintain)
            baseprice = str(float(new_stnd)/.65)
        elif stndcost != 'nan':
            baseprice = str(float(stndcost)/.65)
        
        sql_whse = str(sql_df['whse'][k])
        valid_whse_list.append(sql_whse)
        
    arpvendno_col = list(set(list(sql_df['arpvendno'])))
    if len(arpvendno_col) > 1:
        print("To exceptions; arpvendno has too many variations")
        break
    prodline_col = list(set(list(sql_df['prodline'])))
    if len(prodline_col) > 1:
        print("To exceptions, prodline has too many variations")
        break
            
    date = (datetime.datetime.now().strftime("%m") + datetime.datetime.now().strftime("%d") + datetime.datetime.now().strftime("%y"))
    replcostdt = str(date)
    stndcostdt = str(date)
  
    companyNumber = 1

    api_call_headers = {'Authorization': 'Bearer ' + token, 'Accept': 'application/json', 'Content-type': 'application/json'}
    for k in range(len(valid_whse_list)):
    # key1 = prod, key2 = whse, fieldName = icsw field
        request = {'companyNumber': 1, 'operatorInit': 'ehr', 'operatorPassword': 'ehr700', 'tMntTt': { "t-mnt-tt": [ {'setNo': 1, 'seqNo': 1, 'key1': prod, 'key2': valid_whse_list[k], 'updateMode': 'chg', 'fieldName': 'replcost', 'fieldValue': replcost}, \
                                                                                                                      {'setNo': 1, 'seqNo': 2, 'key1': prod, 'key2': valid_whse_list[k], 'updateMode': 'chg', 'fieldName': 'stndcost', 'fieldValue': stndcost}, \
                                                                                                                      {'setNo': 1, 'seqNo': 3, 'key1': prod, 'key2': valid_whse_list[k], 'updateMode': 'chg', 'fieldName': 'listprice', 'fieldValue': listprice}, \
                                                                                                                      {'setNo': 1, 'seqNo': 4, 'key1': prod, 'key2': valid_whse_list[k], 'updateMode': 'chg', 'fieldName': 'replcostdt', 'fieldValue': replcostdt}, \
                                                                                                                      {'setNo': 1, 'seqNo': 5, 'key1': prod, 'key2': valid_whse_list[k], 'updateMode': 'chg', 'fieldName': 'replcostdt', 'fieldValue': replcostdt}, \
                                                                                                                      {'setNo': 1, 'seqNo': 6, 'key1': prod, 'key2': valid_whse_list[k], 'updateMode': 'chg', 'fieldName': 'baseprice', 'fieldValue': baseprice}]}}
     
        payload = {'request': request}

        api_call_response = requests.post(api_url, json=payload, headers=api_call_headers, verify=False)
        
        print(api_call_response)
        print(api_call_response.text)