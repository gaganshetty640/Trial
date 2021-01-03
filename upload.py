# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 14:31:03 2020

@author: gagan.shetty
"""


from flask import Flask, flash, request, redirect,render_template
from werkzeug.utils import secure_filename
app = Flask(__name__)

import os
import pandas as pd

ALLOWED_EXTENSIONS = set(['xlsx','xls', 'csv'])
UPLOAD_FOLDER = './uploads/'    

from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings("ignore")  
 
@app.route('/')  
def upload():  
    return render_template("file_upload_form.html") 

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 
 
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST': 
        
        
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
                # if user does not select file, browser also
                # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            global filename
            filename = secure_filename(file.filename)
            
            
            
            file.save(os.path.join(UPLOAD_FOLDER, filename))
                    
            data=pd.read_csv(os.path.join(UPLOAD_FOLDER, filename),encoding = "ISO-8859-1")
                
            data_cols= list(data.columns.values)
            
    
#    colours = ['Red', 'Blue', 'Black', 'Orange']
    return render_template('success.html', data_cols=data_cols) 
    

@app.route('/RFM', methods=['POST', 'GET'])
def RFM_page():
    #currentuser = request.args.get("currentuser")

    CID =  request.form["CustomerID"]
    IDate =  request.form["InvoiceDate"]
#    INo =  request.form["InvoiceNo"]
#    Quant =  request.form["Quantity"]
    Rev =  request.form["Revenue"]

#    return str(Quanti)
    data= pd.read_csv(os.path.join(UPLOAD_FOLDER, filename),encoding = "ISO-8859-1")
    uk_data =data[[CID,IDate,Rev]]
    uk_data.columns=["CustomerID","InvoiceDate","Revenue"]
    
#    return render_template('simple.html',  tables=[dataq.to_html(classes='data')], titles=dataq.columns.values)
    
#    data = pd.read_csv('../API/data/OnlineRetail.csv',encoding = "ISO-8859-1")
#    uk_data=data[["CustomerID","InvoiceDate","Quantity","UnitPrice"]]

#    cols = ['CustomerID','InvoiceDate','InvoiceNo','Quantity','UnitPrice']
#    cols=[CustomerI,InvoiceDa,InvoiceN,Quanti,UnitPri]
#    uk_data=pd.DataFrame(cols)
#    data= pd.read_csv(os.path.join(UPLOAD_FOLDER, filename),encoding = "ISO-8859-1")
#    print(uk_data)
##    uk_data=pd.DataFrame(CustomerID,InvoiceDate,InvoiceNo,Quantity,UnitPrice)
##    data = data[(data['Quantity']>0)]
    
    
#    uk_data = uk_data[(uk_data['Quantity']>0)]
    
    uk_data['InvoiceDate']= pd.to_datetime(uk_data['InvoiceDate'])
#    uk_data['TotalPurchase'] = uk_data['Quantity'] * uk_data['UnitPrice']
#    print(uk_data)
#    
#    if 'TotalPurchase' not in uk_data:
#        uk_data['TotalPurchase'] = uk_data['Quantity'] * uk_data['UnitPrice'] 
#        
##        uk_data_group = pd.DataFrame()
#    
#    if 'Recency' not in uk_data.columns:
#        Recency = (uk_data.groupby('CustomerID').agg({'InvoiceDate': lambda date: (date.max() - date.min()).days})).reset_index().rename(columns={'CustomerID':'CustomerID','InvoiceDate' : 'Recency'})
#    else:
#        Recency = uk_data.groupby('CustomerID').Recency.sum().reset_index().rename(columns={'CustomerID':'CustomerID','InvoiceDate' : 'Recency'})
#
#    if 'Frequency' not in uk_data.columns:
#        Frequency = (uk_data.groupby('CustomerID').agg({'InvoiceNo': lambda num: len(num)})).reset_index().rename(columns={'CustomerID':'CustomerID','InvoiceNo' : 'Frequency'})
#    else:
#        Frequency = uk_data.groupby('CustomerID').Frequency.sum().reset_index().rename(columns={'CustomerID':'CustomerID','InvoiceNo' : 'Frequency'})
#    if 'Revenue' not in uk_data.columns:
#        Revenue = uk_data.groupby('CustomerID').agg({'TotalPurchase': lambda price: price.sum()}).reset_index().rename(columns={'CustomerID':'CustomerID','TotalPurchase' : 'Revenue'})
#    else:
#        Revenue = uk_data.groupby('CustomerID').Revenue.sum().reset_index().rename(columns={'CustomerID':'CustomerID','TotalPurchase' : 'Revenue'})
#        
#    if 'Quantity' not in uk_data.columns:   
#        Quantity = (uk_data.groupby('CustomerID').agg({'Quantity': lambda quant: quant.sum()})).reset_index().rename(columns={'CustomerID':'CustomerID','Quantity' : 'Quantity'})
#    else:
#        Quantity = uk_data.groupby('CustomerID').Quantity.sum().reset_index().rename(columns={'CustomerID':'CustomerID','Quantity' : 'Quantity'})
#        
#    
#    cols=[Recency,Frequency,Revenue,Quantity] 
#    uk_data_group = functools.reduce(lambda left,right: pd.merge(left,right,on='CustomerID'), cols)
#        uk_data_group["Recency"]=uk_data.groupby('CustomerID').agg({'InvoiceDate': lambda date: (date.max() - date.min()).days})
#        uk_data_group["Frequency"]=uk_data.groupby('CustomerID').agg({'InvoiceDate': lambda num: num.count()})
#        uk_data_group["Quantity"]=uk_data.groupby('CustomerID').agg({'Quantity': lambda quant: quant.sum()})
#        uk_data_group["Revenue"]=uk_data.groupby('CustomerID').agg({'TotalPurchase': lambda price: price.sum()})

                                  
    
    uk_data_group1=uk_data.groupby('CustomerID').agg({'InvoiceDate': lambda date: (date.max() - date.min()).days,
                                           # 'InvoiceDate': lambda num: num.count(),
#                                            'Quantity': lambda quant: quant.sum(),
                                            'Revenue': lambda price: price.sum()}).reset_index()
    Frequency= uk_data.groupby('CustomerID').agg({'InvoiceDate': lambda num: num.count()}).reset_index()
    uk_data_group= pd.merge(uk_data_group1,Frequency,on="CustomerID")
    

    uk_data_group.columns=['CustomerID','Recency','Revenue','Frequency']
    uk_data_group["Recency"]=round(uk_data_group["Recency"]/30,0)
    uk_data_group['Recency'] = uk_data_group['Recency'].replace(0,1)
    final_data = uk_data_group.to_dict()
    new_data= pd.DataFrame(final_data)    
    def order_cluster(cluster_field_name, target_field_name,df,ascending):
        new_cluster_field_name = 'new_' + cluster_field_name
        df_new = df.groupby(cluster_field_name)[target_field_name].mean().reset_index()
        df_new = df_new.sort_values(by=target_field_name,ascending=ascending).reset_index(drop=True)
        df_new['index'] = df_new.index
        df_final = pd.merge(df,df_new[[cluster_field_name,'index']], on=cluster_field_name)
        df_final = df_final.drop([cluster_field_name],axis=1)
        df_final = df_final.rename(columns={"index":cluster_field_name})
        return df_final

    kmeans_rec = KMeans(n_clusters=4)
    kmeans_rec.fit(new_data[['Recency']])
    new_data['RecencyCluster'] = kmeans_rec.predict(new_data[['Recency']])
    new_data = order_cluster('RecencyCluster', 'Recency',new_data,False)

    kmeans_fre = KMeans(n_clusters=4)
    kmeans_fre.fit(new_data[['Frequency']])
    new_data['FrequencyCluster'] = kmeans_fre.predict(new_data[['Frequency']])
    new_data = order_cluster('FrequencyCluster', 'Frequency',new_data,True)
    
    kmeans_rev = KMeans(n_clusters=4)
    kmeans_rev.fit(new_data[['Revenue']])
    new_data['RevenueCluster'] = kmeans_rev.predict(new_data[['Revenue']])    
    new_data = order_cluster('RevenueCluster', 'Revenue',new_data,True)
    
    new_data['OverallScore'] = new_data['RecencyCluster'] + new_data['FrequencyCluster'] + new_data['RevenueCluster']
    new_data['Segment'] = 'Low-Value'
    new_data.loc[new_data['OverallScore']>2,'Segment'] = 'Mid-Value' 
    new_data.loc[new_data['OverallScore']>4,'Segment'] = 'High-Value'
    
#    new_data1 = new_data.to_dict()
#    return jsonify(new_data1)
    return render_template('simple.html',  tables=[new_data.to_html(classes='data')], titles=new_data.columns.values)

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)