import requests
import json
import pandas as pd
import random
import string
from tqdm import tqdm



UrlCreateLicenses = "http://iot.adani.by:4101/license/create"
UrlGetAllProducts = "http://iot.adani.by:4101/Product"
UrlGetAllCompanies = "http://iot.adani.by:4101/Company"
UrlGetAllDevices = "http://iot.adani.by:4000/Devices/GetAllMongo"
AuthGetDevices = {'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYyMGY0NjRlYzk2MjExNTIxMTg1NzNkYyIsIm5iZiI6MTY0ODU0NzUzMiwiZXhwIjoxNjQ4NTY1NTMxLCJpYXQiOjE2NDg1NDc1MzJ9.tcpaAisMD3HTVKONEW4AP-Al_Kxz2jDcw2bo2hyfNok'}
Auth = {'Content-type':'application/json', 'Accept':'application/json','Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYyMzFlNWQ0OTM2NGM0NGUzMGZlMzE4NyIsIm5iZiI6MTY0ODU0NzQyMSwiZXhwIjoxNjQ5MTUyMjIxLCJpYXQiOjE2NDg1NDc0MjF9.r2jL3mX6YLAh27k2BdUJrLOE1O67efB5l9x-5eRFb2k'}
AuthGet = {'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYyMzFlNWQ0OTM2NGM0NGUzMGZlMzE4NyIsIm5iZiI6MTY0ODU0NzQyMSwiZXhwIjoxNjQ5MTUyMjIxLCJpYXQiOjE2NDg1NDc0MjF9.r2jL3mX6YLAh27k2BdUJrLOE1O67efB5l9x-5eRFb2k'}


def TableLoad (url,Auth):
    print ("Loading table...")
    resp = requests.get(url, headers = Auth)
    #print (resp)
    devices_list = resp.json()
    if devices_list == {"message": "Unauthorized"}:
        print ('The token "AuthGetDevices" has expired. Enter a new token authorization token "AuthGetDevices": ')
    else:
        column_names = devices_list[0].keys()
        
        #table = pd.DataFrame(columns = column_names)
        table = pd.DataFrame(columns = column_names)
        for r in tqdm(devices_list):
            df_dictionary = pd.DataFrame([r])
            table = pd.concat([df_dictionary,table], ignore_index=True)
        print (" \nCreating Licenses...")
        return table

def GenerateRandomKey(length):
    letters_and_digits = string.ascii_letters + string.digits
    rand_string = ''.join(random.sample(letters_and_digits, length))
    #print("KEY: ", rand_string)
    return rand_string


def GetMethodProducts (url,Auth):
    resp = requests.get(url, headers = Auth)
    #print (resp)
    products_list = resp.json()
    if products_list == {"message": "Unauthorized"}:
        print ('The token "AuthGet" has expired. Enter a new token authorization token "AuthGet": ')
    else:
        randProduct = random.choice(products_list)
        return randProduct

def GetMethodCompanyName (url,Auth):
    resp = requests.get(url, headers = Auth)
    companies_list = resp.json()
    randCompany = random.choice(companies_list)
    return randCompany["name"]

def GetDevices (url,Auth):
    scannerModel = random.choice(["BV 5030CA", "BV 5030", "BV 6045", "BV 6045DV", "BV 7080DV", "BV 6080", "BV 100100TB", "BV 100100DV", "BV 100100DVM", "BV STREAM", "BV MAX", "BV 160180", "BV 160165", "BV 100100M", "BV 6080M", "PROTEUS 6045" ])
    serialNumberRand = random.choice(table[table['model'] == scannerModel]['serialNumber'].values)
    return scannerModel, serialNumberRand 


i = 0 
quantity_licenses = int (input ("Enter the number of licenses: "))
table = TableLoad (UrlGetAllDevices, AuthGetDevices)

while i!= quantity_licenses:
    for k in tqdm (range (quantity_licenses)):
        randProduct = GetMethodProducts(UrlGetAllProducts, AuthGet)
        randCompany =  GetMethodCompanyName (UrlGetAllCompanies,AuthGet)  
        scannerKey = GenerateRandomKey(32)
        serialNumberRand =  GetDevices (UrlGetAllDevices, AuthGetDevices) 
    
        param_dict = {
            "companyName": randCompany,
            "scannerKey": scannerKey,
            "scannerModel": serialNumberRand [0],
            "scannerSerialNumber": serialNumberRand [1],
            "products": [randProduct],
            "validTill": "2023-03-15T07:57:35.712Z"
            } 
        js = json.dumps(param_dict)
        response = requests.post(UrlCreateLicenses, headers = Auth, data = js)
        #print (param_dict)
        #print (response)
        i+=1

