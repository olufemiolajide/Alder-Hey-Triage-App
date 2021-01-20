import streamlit as st
import pandas as pd
import numpy as np 
#from sklearn.ensemble import RandomForestRegressor,RandomForestClassifier
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import sklearn
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
# ML Libraries for Regression
import lightgbm as lgb
from sklearn.pipeline import Pipeline as Pipe
#from feature_engine import categorical_encoders as ce
#from feature_engine import discretisers as dsc
#from feature_engine import missing_data_imputers as mdi
#import feature_engine.missing_data_imputers as mdi
#from feature_engine import variable_transformers as vt
#from feature_engine.outlier_removers import Winsorizer
#from feature_engine.categorical_encoders import OneHotCategoricalEncoder,OrdinalCategoricalEncoder
#from xgboost import XGBClassifier
from sklearn.ensemble import ExtraTreesClassifier


import pickle

filename ='triage_rf_base_model.pkl'
rfr1 = pickle.load(open(filename, 'rb'))


#return a tuple
def makeprediction(df):
	prediction=rfr1.predict(df)
	prob=rfr1.predict_proba(df)
    
    #prob_df=pd.train_dfFrame(prob,columns=['Dead','Survived'])
    
	dead_prob=prob[0]
	#survived_prob=prob[1]
	return dead_prob,prediction#,survived_prob