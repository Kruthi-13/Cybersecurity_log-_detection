import os
import streamlit as st
from dotenv import load_dotenv
import pandas as pd
import joblib


model=joblib.load("fraud_detection_pipeline.pkl")

st.title("Fraud Detection Prediction App")

st.markdown("Please enter the transaction detailes and use the predict button")

st.divider()

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") 


def validate_GOOGLE_API_KEY():
    if not GOOGLE_API_KEY:
        return "GOOGLE_API_KEY not found. Add it to your .env file."

    if not GOOGLE_API_KEY.startswith("AIza"):
        return (
            "GOOGLE_API_KEY is not a valid Google AI Studio/Gemini API key. "
            "Create a Gemini API key from Google AI Studio and paste it in .env."
        )

    return None

transaction_type=st.selectbox("Transaction Type",["PAYMENT","TRANSFER","CASH_OUT","DEPOSIT"])
amount =st.number_input("Amount",min_value=0.0, value=1000.0)
oldbalanceOrg=st.number_input("Old Balance(Sender)", min_value=0.0, value=10000.0)
newbalanceOrig=st.number_input("New Balance (Sender)", min_value=0.0, value=9000.0)
oldbalanceDest=st.number_input("Old Balance (Receiver)", min_value=0.0, value=0.0)
newbalanceDest=st.number_input("New Balance (Receiver)", min_value=0.0, value=0.0)

if st.button("Predict"):
    input_data=pd.DataFrame([{
        "type": transaction_type,
        "amount": amount,
        "oldbalanceOrg" : oldbalanceOrg,
        "newbalanceOrig" : newbalanceOrig,
        "oldbalanceDest" : oldbalanceDest,
        "newbalanceDest" : newbalanceDest
    }])
    
    
    prediction = model.predict(input_data)[0]
    
    st.subheader(f"Prediction : '{int(prediction)}")
    
    if prediction == 1:
        st.error("This transaction can be fraud")
    else:
        st.success("This transaction looks like it is not a fraud")