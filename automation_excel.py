import os
import shutil

import pandas as pd
import requests

#automate from Desktop on desired day after scan : refer - https://towardsdatascience.com/how-to-easily-automate-your-python-scripts-on-mac-and-windows-459388c9cc94

####Fetch new csv file from Tenable 
print("\n\nFetching new file from Tenable.io\n\n")
key = "<Tenable_accessKEY>"

#Get Scan status (4129 = 'XXX-PUB-External All' scan-id)
url = "https://cloud.tenable.com/scans/4129/latest-status"
headers = {
    "Accept": "application/json",
    "X-ApiKeys": key
}
response = requests.get(url, headers=headers)


#Get export file
url = "https://cloud.tenable.com/scans/4129/export"
payload = {"format": "csv"}
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-ApiKeys": key
}
response = requests.post(url, json=payload, headers=headers)
temp_file = response.text
export_file = temp_file.strip("{file:\"}")


#Download export file
print("\n\nExporting .csv file from Tenable.io in progress\n\n")
url = "https://cloud.tenable.com/scans/4129/export/%s/download"%export_file
print(url)
headers = {
    "Accept": "application/octet-stream",
    "X-ApiKeys": key
}    
response = requests.get(url, headers=headers).text
with open('<file_Location>/XXX-PUB-External_All.csv', 'w') as f:
    f.write(response)


##Move file to workdir
original = r'<FROM DOWNLOADS>'
target = r'<TO WORKDIR>'
shutil.move(original, target)


##Delete unrequired columns of XXX-PUB-External_All.csv file
df = pd.read_csv('~Workdir/XXX-PUB-External_All.csv', low_memory=False)
df.drop(df.columns[[0,1,2,3,4,5,6,7,8,9,10,11,13,14,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]], axis=1, inplace=True)
columns_titles = ["IP Address","Plugin Output"]
df=df.reindex(columns=columns_titles)
remove_dup_ip = df.drop_duplicates(subset=['IP Address'])
remove_dup_ip.to_csv('~Workdir/XXX-PUB-External_All.csv', index = False)


##Append new + old and save in .csv file (old) then Delete repeated ip's from old file
print("\n\nSyncing in process ~ Removing duplicates\n\n")
rf = pd.read_csv('~/Workdir/XXX-PUB-External_All.csv')
tf = pd.read_csv('~/Workdir/original.csv')
frames = [tf, rf]
result = pd.concat(frames)

#To print all repeated ip's
'''
remov = result.drop(result.columns[1], axis=1, inplace=False)
df = remov[remov.duplicated(['IP Address'], keep='first')]
print(df)
print("\n")
'''

#gives values removed from new scan
dup = result.drop_duplicates(subset=['IP Address'])
newframes = [dup, rf]
newresult = pd.concat(newframes)
mid = newresult.drop(newresult.columns[1], axis=1, inplace=False)
mids = mid.drop_duplicates(subset=['IP Address'], keep= False)
print("\n\nIPs removed from previous scan\n")
print(mids)
mids.to_csv('~/Workdir/removed_ips.csv', index = False)
print("\n")

#Gives new ip's added
newframes1 = [dup, tf]
newresult1 = pd.concat(newframes1)
mid1 = newresult1.drop(newresult1.columns[1], axis=1, inplace=False)
mids1 = mid1.drop_duplicates(subset=['IP Address'], keep= False)
print("\n\nNew IPs added this week\n")
print(mids1)
print("\n")
mids1.to_csv('~/Workdir/new_ips.csv', index = False)
dup.to_csv('<file_location>.csv', index = False) #append to last weeks scan


##delete new file as already synced from workdir and downloads folder
os.remove('~/Workdir/XXX-PUB-External_All.csv') 
print("\n\nFile is synced successfully\n\n")

##Done
print("\n\n\nProcess Completed Successfully\n")