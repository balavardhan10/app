
# coding: utf-8

# In[6]:


from flask import Flask,jsonify,render_template,request
import sklearn
import pickle
import requests
import numpy as np

app = Flask(__name__)
model = pickle.load(open('random_reg.pkl', 'rb'))
    
@app.route('/')
def home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    if request.method == 'POST':
        Year = int(request.form['Model_Year'])
        Present_Price=float(request.form['Present_Price'])
        Kms_Driven=int(request.form['Kms_Driven'])
        Owner=int(request.form['Owner'])
        Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
        if(Fuel_Type_Petrol=='Petrol'):
                Fuel_Type_Petrol=1
                Fuel_Type_Diesel=0
        elif(Fuel_Type_Petrol=='Diesel'):
                Fuel_Type_Petrol=0
                Fuel_Type_Diesel=1
        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=0

        Year=2020-Year
        Seller_Type_Individual=request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0
        Transmission_Manual=request.form['Transmission_Manual']
        if(Transmission_Manual=='Manual'):
            Transmission_Manual=1
        else:
            Transmission_Manual=0
        prediction=model.predict([[Present_Price,Kms_Driven,Owner,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Manual,Year]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_texts="You Can Sell The Car at {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)

