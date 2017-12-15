import pandas as pd
import numpy as np
import math

col_list = range(10,110)
l = [0.1] * 100
xls = pd.ExcelFile('UUCF Assignment Spreadsheet V2.xls')
user_movieRating = xls.parse('Sheet3')
Rel_Users = xls.parse('Sheet2')
User_Info = xls.parse('user-row')
User_Info.index = User_Info.iloc[:,0]
User_Info = User_Info.iloc[:,1:101]
UUcoerrMatrix = User_Info.T.corr()
#IIcoerrMatrix = User_Info.corr()

count = 0
sumOfRelUsersWeightFor3712 = 0.0

Df3712 = pd.DataFrame(data=[l],columns = col_list)
prod3712 = 0.0
Prodsum3712 = 0.0

for m in range(10,110):
    prod3712 = 0.0
    Prodsum3712 = 0.0
    sumOfRelUsersWeightFor3712 = 1.0
    count = 0
    
    if(list(user_movieRating.loc[user_movieRating['User_Id'] == 3712][m])[0]!=0):
        Df3712[m][0] = list(user_movieRating.loc[user_movieRating['User_Id'] == 3712][m])[0]
        
    elif(math.isnan(list(user_movieRating.loc[user_movieRating['User_Id'] == 3712][m])[0])):
        
        for i,j in user_movieRating.iterrows():
            for k,l in Rel_Users.iterrows():                    
                if(user_movieRating[m][i]!=0):
                    count = count + 1;
                    if(count==1):
                            sumOfRelUsersWeightFor3712 = sumOfRelUsersWeightFor3712 - 1.0
                    if(Rel_Users['RelTo3712'][k] == user_movieRating['User_Id'][i]):  
                        prod3712 = user_movieRating[m][i] * Rel_Users[3712][k]
                        Prodsum3712 = Prodsum3712 + prod3712
                        sumOfRelUsersWeightFor3712 = sumOfRelUsersWeightFor3712 + Rel_Users[3712][k]
        Df3712[m][0] = Prodsum3712/sumOfRelUsersWeightFor3712