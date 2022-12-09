import pandas as pd

rf = pd.read_csv('~/Documents/CSV1.csv')
print(rf)
print("\n")
tf = pd.read_csv('~/Documents/CSV2.csv')
print(tf)
print("\n")


#gives duplicates
frames = [tf, rf]
result = pd.concat(frames)
'''
remov = result.drop(result.columns[1], axis=1, inplace=False)
df = remov[remov.duplicated(['IP'], keep='first')]
print(df)
print("\n")
'''


#gives new values added
dup = result.drop_duplicates(subset=['IP'])
print(dup)
print('\n')
newframes = [dup, rf]
newresult = pd.concat(newframes)
mid = newresult.drop(newresult.columns[1], axis=1, inplace=False)
mids = mid.drop_duplicates(subset=['IP'], keep= False)
print(mids)
print("\n")

'''
#gives values not in new csv
dup1 = result.drop_duplicates(subset=['IP'])
newframes = [dup, tf]
newresult = pd.concat(newframes)
mid = newresult.drop(newresult.columns[1], axis=1, inplace=False)
mids = mid.drop_duplicates(subset=['IP'], keep= False)
print(mids)'''