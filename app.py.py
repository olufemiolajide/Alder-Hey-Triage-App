import streamlit as st
import pandas as pd
import numpy as np 
import time
import module.MODEL as modu
from PIL import Image
from sklearn.preprocessing import StandardScaler
import datetime

def is_authenticated(password):
    return password == "admin"

pwd_placeholder = st.sidebar.empty()

pwd = pwd_placeholder.text_input("Password:", value="", type="password")


def main():
   
   ##Main Page if password is correct##
    
    #Title
    st.title("Alder Hey Emergency Triage App")

    # Add a placeholder
    latest_iteration = st.empty()
    bar = st.progress(0)

    for i in range(100):
      # Update the progress bar with each iteration.
      latest_iteration.text(f'Iteration {i+1}')
      bar.progress(i + 1)
      time.sleep(0.01)

    #display image.
    image = Image.open('alderhey.jpeg')
    st.image(image, caption= "Alder Hey Children's Hospital, Liverpool",use_column_width=True)
                                                                                                                                      
    #setting empty dataframe for stremalit to add too.
    zero_list=(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
    test_df=pd.DataFrame([zero_list],columns=['Transport','Age','Male','Time_Slot','day_of_week','month','IMD','IDACI','IDAOPI','Disability_Decile','SAFE_GUARDING','ETHNIC_CODE','Visit_Reason','REFER_SOURCE','AVPU','PulseRate','RespiratoryRate','SP02','Temperature'])
    
    ########## Patient Details ##############
    
    st.title("Patient Details")
    
    #Age
    Age = st.slider('Please select patients age.', min_value=0, max_value=20, value=6)
    test_df['Age']=Age 
    
    #gender
    gender_option = st.selectbox('Please select patients gender.',('Male','Female'))
    #'You selected:', gender_option

    if (gender_option=='Male'):
                  test_df['Male']=1
    else:
                  test_df['Male']=0
                           
    #ETHNIC_CODE
    ETHNIC_CODE=st.selectbox('Please select patients ethnicity.',('Asian'
    ,'Black'
    ,'Mixed'
    ,'Other'
    ,'White'
    ))
    test_df['ETHNIC_CODE']=ETHNIC_CODE
    
    def load():
        df=pd.read_csv("IMD_Scores.csv")
        return df
    df=load()
    
    #Using postcodes to get IMD scores
    user_input = st.text_input("Please enter patients postcode (Leave blank if not found)")
    
    # try catch statment to use entered postcode to find IMD, Disability_Decile, IDACI and IDAOPI.
    try:
        user_input = user_input.upper()
            
        Post = df.loc[df['Postcode'] == user_input]
        
        IMD = Post['Index_of_Multiple_Deprivation_Decile'].values
        IMD = IMD[0]
        st.write(IMD, 'IMD decile')
        test_df['IMD']=IMD
        
        Disability_Decile = Post['Health_and_Disability_Decile'].values
        Disability_Decile = Disability_Decile[0]
        st.write(Disability_Decile, 'Disability decile')
        test_df['Disability_Decile']=Disability_Decile
        
        IDACI = Post['IDACI_Decile'].values
        IDACI = IDACI[0]
        st.write(IDACI, 'IDACI decile')
        test_df['IDACI']=IDACI
        
        IDAOPI = Post['IDAOPI_Decile'].values
        IDAOPI = IDAOPI[0]
        st.write(IDAOPI, 'IDAOPI decile')
        test_df['IDAOPI']=IDAOPI
    except:
        st.write('Please input a vaild UK postcode')
    
    #Safe Guarding. 
    SAFE_GUARDING=st.selectbox('Safe Guarding?',('Yes'
    ,'No'
    
    ))
    test_df['SAFE_GUARDING']=SAFE_GUARDING
    
    ########## Presenting Problem ##############
    
    st.title("Presenting Problem")
    
    #Visit Reasons
    Visit_Reason=st.selectbox('Visit Reason?',('Allergy (Including Anaphylaxis)'
    ,'Bites/Stings'
    ,'Burns and Scalds'
    ,'Cardiac Conditions'
    ,'Central Nervous System Conditions (Excluding Strokes)'
    ,'Cerebro-Vascular Conditions'
    ,'Contusion/Abrasion'
    ,'Dermatological Conditions'
    ,'Diabetes and Other Endocrinological Conditions'
    ,'Diagnosis Not Classifiable'
    ,'Dislocation/Fracture/Joint Injury/Amputation'
    ,'ENT Conditions'
    ,'Facio-Maxillary Conditions'
    ,'Foreign Body'
    ,'Gastrointestinal Conditions'
    ,'Gynaecological Conditions'
    ,'Haematological Conditions'
    ,'Head Injury'
    ,'Infectious Disease'
    ,'Laceration'
    ,'Local Infection'
    ,'Muscle/Tendon Injury'
    ,'Near Drowning'
    ,'Nerve Injury'
    ,'Nothing Abnormal Detected'
    ,'Obstetric Conditions'
    ,'Ophthalmological Conditions'
    ,'Other Vascular Conditions'
    ,'Poisoning (Including Overdose)'
    ,'Psychiatric Conditions'
    ,'Respiratory Conditions'
    ,'Social Problem (Includes Chronic Alcoholism and Homelessness)'
    ,'Soft Tissue Inflammation'
    ,'Sprain/Ligament Injury'
    ,'Urological Conditions (Including Cystitis)'
    ,'Vascular Injury'
    ,'Visceral Injury'
    ))

    test_df['Visit_Reason']=Visit_Reason

    #test_df=modu.preprocessing(test_df)

    #REFER_SOURCE
    REFER_SOURCE=st.selectbox('Refer Source?',('SELF' ,'AE','CONS IN HOSP','OTHER'))

    test_df['REFER_SOURCE']=REFER_SOURCE
    
    #Transport Selector.
    Transport=st.selectbox('Mode of Arrival? ',
    ('Other','Ambulance','Helicopter'))
    test_df['Transport']=Transport
        
    ############ ED Vitial Signs #################
    
    st.title("ED Vitial Signs")
    
    #PulseRate
    PulseRate = st.slider('Pulse Rate', min_value=40, max_value=150, value=70)
    test_df['PulseRate']=PulseRate

    #Respiratory Rate
    RespiratoryRate = st.slider('Respiratory Rate', min_value=10, max_value=40, value=25)
    test_df['RespiratoryRate']=RespiratoryRate

    #Temperature
    Temperature = st.slider('Temperature', min_value=34, max_value=40, value=37)
    test_df['Temperature']=Temperature

    #SP02
    SP02=st.number_input('SP02',min_value=34,max_value=100, value=100, step=1)
    test_df['SP02']=SP02
    
    #AVPU
    AVPU=st.selectbox('AVPU',('Alert','Pain','Unresponsive','Verbal'))
    test_df['AVPU']=AVPU
    
    ################# Automatic Features ##########################
    
    # Gets current time stamp to fill in time slot, day_of_week and month.
    mydate = datetime.datetime.now()
    
    if (mydate.hour >=0 and mydate.hour <= 5):
                  test_df['Time_Slot']='0_5'
    elif (mydate.hour >=6 and mydate.hour <= 11):
                  test_df['Time_Slot']='6_11'
    elif (mydate.hour >=12 and mydate.hour <= 17):
                  test_df['Time_Slot']='12_17'
    elif (mydate.hour >=18 and mydate.hour <= 23):
                  test_df['Time_Slot']='18_23'
    
    WeekDay = mydate.strftime("%A")
    test_df['day_of_week']=WeekDay
    
    Month = mydate.strftime("%B")   
    test_df['month']=Month
    
    ############### Predictions ####################################

    #Using Model from module folder to make probability of class likelyhood.
    prob, prediction=modu.makeprediction(test_df)

    ##Show survival probability
    if st.checkbox(' Show the Result ! '):
        st.subheader('Result')
        st.write('Likelihood Minor Risk (out of 100) = %0.0f %%'%(prob[0]*100))
        st.write('Likelihood Moderate Risk (out of 100) = %0.0f %%'%(prob[1]*100))
        st.write('Likelihood Urgent Risk (out of 100) = %0.0f %% '%(prob[2]*100))
            
if is_authenticated(pwd):
    #pwd_placeholder.empty()
    main()
    
elif pwd == '':
      st.write("Please Enter A Password.")  
else:
    st.error("the password you entered is incorrect")



