# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 08:48:57 2017

@author: abhishekk & Devya &Deeksha
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
color = sns.color_palette()
from sklearn.cluster import KMeans
import pylab as pl
from sklearn import preprocessing


def Clustering_Analysis(data):
    train = data
    train.head()    
    #cols= ['Country','CustomerId']
    #cols= ['CustomerID','Country','RFM_Score']
    
    x=train['CustomerID']
    y = train['RFM_Score']     
    
    #Finding clusters
    Nc = range(1, 10)
    kmeans = [KMeans(n_clusters=i) for i in Nc]    
    print (kmeans)    
    score = [kmeans[i].fit(y).score(y) for i in range(len(kmeans))]    
    print(score)
    
    #Plotting Elbow Curve
    pl.plot(Nc, score)    
    pl.xlabel('Number of Clusters')    
    pl.ylabel('Score')    
    pl.title('Elbow Curve')    
    pl.show()
    
    #Implementing Kmeans for 5 clusters
    kmeans=KMeans(n_clusters=5)    
    kmeansoutput=kmeans.fit(y)
    
    # These are our fitted labels for clusters -- the first cluster has label 0, and the second has label 1.
    labels = kmeans.labels_    
    print (kmeansoutput)    
    pl.figure('5 Cluster K-Means')    
    pl.scatter(x,y, c=kmeansoutput.labels_)    
    print(kmeansoutput.cluster_centers_)    
    pl.xlabel('CustomerID')    
    pl.ylabel('RFM_Score')    
    pl.title('5 Cluster K-Means')    
    pl.show()
    train['Cluster']=labels
    train.to_csv('labelled_Data.csv')

def data_manipulation(data):
    
    len(data['CustomerID'].unique()) 
    
    data['Total_Price']=data['Quantity']*data['UnitPrice']
    data['date']=data['InvoiceDate'].str.extract('(.*)/').str.extract('(.*)/')
    print ("Date Format",data['InvoiceDate'].str.extract('(.*)/'))
    data['date']=[str(i) for i in data['date']]
    #data['date']=data.date.astype(str).str.zfill(2)
    #print ('date format 11',data['date'])    
    #print ("Date Format 2",data['InvoiceDate'].str.extract('/(.*) ').str.extract('/(.*)'))
    data['date']=data['InvoiceDate'].str.extract('/(.*) ').str.extract('/(.*)') + data['date']
    print (data['date'])
    data.date = pd.to_numeric(data.date, errors='coerce')
    
    Cust_country=data[['Country','CustomerID']].drop_duplicates()
    
    #Calculating the distinct count of customer for each country
    Cust_country_count=Cust_country.groupby(['Country'])['CustomerID'].\
    aggregate('count').reset_index().sort('CustomerID', ascending=False) 
    
    #b=Cust_country['CustomerID'].unique()    
    print (Cust_country.groupby(['Country'])['CustomerID'].\
    aggregate('count').reset_index().sort('CustomerID', ascending=False))
    
    #Plotting the count of customers
    country=list(Cust_country_count['Country'])
    Cust_id=list(Cust_country_count['CustomerID'])
    plt.figure(figsize=(12,8))
    sns.barplot(country, Cust_id, alpha=0.8, color=color[2])
    plt.xticks(rotation='60')
    plt.show()
    
    return data
    
def Recency_Calculation(data):
        #Dropping Duplicates on Customerid and Date
    Cust_date=data[['CustomerID','date']].drop_duplicates()
    
    def date_bins(row):
        if row['date'] > 201110:
            val = 5
        elif row['date'] <= 201110 and row['date'] > 201108:
            val = 4
        elif row['date'] <= 201108 and row['date'] > 201106:
            val = 3
        elif row['date'] <= 201106 and row['date'] > 201104:
            val = 2
        else:
            val = 1
        return val
    
    
    Cust_date['Recency_Flag'] = Cust_date.apply(date_bins, axis=1)
    Cust_date = Cust_date.groupby('CustomerID',as_index=False)['Recency_Flag'].max()
    
    plt.figure(figsize=(12,8))
    sns.countplot(x='Recency_Flag', data=Cust_date, color=color[1])
    plt.ylabel('Count', fontsize=12)
    plt.xlabel('Recency_Flag', fontsize=12)
    plt.xticks(rotation='vertical')
    plt.title('Frequency of Recency_Flag', fontsize=15)
    plt.show()
    
    #b=Cust_date['CustomerID'].unique()
    
    return Cust_date
    
def Frequency_Calculation(data):   
    #FREQUENCY CALCULATION
    Cust_freq=data[['Country','InvoiceNo','CustomerID']].drop_duplicates()
    
    print(Cust_freq.loc[(Cust_freq['CustomerID']==16869)])
    
    #Calculating the count of unique purchase for each customer
    Cust_freq_count=Cust_freq.groupby(['CustomerID'])['InvoiceNo'].aggregate('count').\
    reset_index().sort('InvoiceNo', ascending=False)
    
    
    unique_invoice=Cust_freq_count[['InvoiceNo']].drop_duplicates()
    
    # Dividing in 5 equal parts
    unique_invoice['Freqency_Band'] = pd.qcut(unique_invoice['InvoiceNo'], 5)
    unique_invoice=unique_invoice[['Freqency_Band']].drop_duplicates()
    unique_invoice
    
    def invoice_bins(row):
        if row['InvoiceNo'] <= 13:
            val = 1
        elif row['InvoiceNo'] > 14 and row['InvoiceNo'] <= 26.6:
            val = 2
        elif row['InvoiceNo'] > 26.6 and row['InvoiceNo'] <= 40.4:
            val = 3
        elif row['InvoiceNo'] > 40.4 and row['InvoiceNo'] <= 62.2:
            val = 4
        else:
            val = 5
        return val
    
    Cust_freq_count['Freq_Flag'] = Cust_freq_count.apply(invoice_bins, axis=1)
    #Let us check the distribution of Frequency flags:
    plt.figure(figsize=(12,8))
    sns.countplot(x='Freq_Flag', data=Cust_freq_count, color=color[1])
    plt.ylabel('Count', fontsize=12)
    plt.xlabel('Freq_Flag', fontsize=12)
    plt.xticks(rotation='vertical')
    plt.title('Frequency of Freq_Flag', fontsize=15)
    plt.show()
    
    #c=Cust_freq_count['CustomerID'].unique()
    return Cust_freq_count

def Monetory_Calculation(data):    
    #Monetory Calculation
    #Calculating the Sum of total monetary purchase for each customer
    Cust_monetary = data.groupby(['CustomerID'])['Total_Price'].aggregate('sum').\
    reset_index().sort('Total_Price', ascending=False)    
    unique_price=Cust_monetary[['Total_Price']].drop_duplicates()
    unique_price=unique_price[unique_price['Total_Price'] > 0]
    unique_price['monetary_Band'] = pd.qcut(unique_price['Total_Price'], 5)
    unique_price=unique_price[['monetary_Band']].drop_duplicates()
    unique_price
    
    def M(row):
        if row['Total_Price'] <= 250:
            val = 1
        elif row['Total_Price'] > 250 and row['Total_Price'] <= 488:
            val = 2
        elif row['Total_Price'] > 488 and row['Total_Price'] <= 936:
            val = 3
        elif row['Total_Price'] > 936 and row['Total_Price'] <= 2036:
            val = 4
        else:
            val = 5
        return val
    
    Cust_monetary['Monetary_Flag'] = Cust_monetary.apply(M, axis=1)
    
    #Let us check the distribution of Monetary flags:
    plt.figure(figsize=(12,8))
    sns.countplot(x='Monetary_Flag', data=Cust_monetary, color=color[1])
    plt.ylabel('Count', fontsize=12)
    plt.xlabel('Monetary_Flag', fontsize=12)
    plt.xticks(rotation='vertical')
    plt.title('Frequency of Monetary_Flag', fontsize=15)
    plt.show()
    
    #d=Cust_monetary['CustomerID'].unique()
    
    return Cust_monetary


def Apriori_Data_Preparation(data):
    inputData_Unique = data.drop_duplicates('CustomerID')
    final = list()
    count = list()
    for i,j in inputData_Unique.iterrows():
        new = data.loc[inputData_Unique['CustomerID'][i] == data['CustomerID'],:]
        count.append(len(new))
        #print(inputData_Unique['CustomerID'][i])
        final.append(new["StockCode"].to_string(header=False,index=False).split('\n'))
    
    return final
    

if __name__ == "__main__":
    
    try:
        print("helloooo")
        data=pd.read_csv('D:\\Satander Data\\OnlineRetail.csv')
        data.head(10)
    except FileNotFoundError as e:
        print ('File Not Found')
    try:   
        data=data_manipulation(data)
    except Exception as e1:
        print ("Dataframe Not created for Manipulation")
    
    try:
        Recency_data=Recency_Calculation(data)
    except Exception as e2:
        print ("DF not created for Recency")
    try:
        Frequency_data=Frequency_Calculation(data)
    except Exception as e2:
        print ("DF not created for Frequency")
    try:
        Monetory_data=Monetory_Calculation(data)
    except Exception as e2:
        print ("DF not created for Monetory")
      
    #Merging All the data to one table for RFM Score Calculation.
    Cust_All=pd.merge(data,Recency_data[['CustomerID','Recency_Flag']],\
    on=['CustomerID'],how='left') 
    
    Cust_All=pd.merge(Cust_All,Frequency_data[['CustomerID','Freq_Flag']],\
    on=['CustomerID'],how='left')   
       
    Cust_All=pd.merge(Cust_All,Monetory_data[['CustomerID','Monetary_Flag']],\
    on=['CustomerID'],how='left')    
    print (Cust_All.head())
    
    e=Cust_All['CustomerID'].unique()
    ids = Cust_All["CustomerID"]
    print (e)
    
    #Cust_All['RFM_Score']=[i for i in Cust_All]    
    #Clustering_Analysis(Cust_All)
    #e=Cust_All['CustomerID'].unique()
    #ids = Cust_All["CustomerID"]
    #Cust_All[ids.isin(ids[ids.duplicated()])].sort("CustomerID")  
    
    Apriori_Data=Apriori_Data_Preparation(data)


