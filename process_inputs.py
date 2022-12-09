# import necessary libraries

import pandas as pd
import sys 
import numpy as np
import seaborn as sns
from math import sqrt
from pylab import rcParams
import pickle
import csv
import ast


def missing(df):
	
	# drop theses columns due to large null values or many same values
	df = df.drop(['Utilities','PoolQC','MiscFeature','Alley'], axis=1)
	
	# Null value likely means No Fence so fill as "None"
	df["Fence"] = df["Fence"].fillna("None") 
	
	# Null value likely means No Fireplace so fill as "None"
	df["FireplaceQu"] = df["FireplaceQu"].fillna("None")
	
	# Lot frontage is the feet of street connected to property, which is likely similar to the neighbourhood houses, so fill Median value
	df["LotFrontage"] = df["LotFrontage"].fillna(69.0)
	
	# Null value likely means  typical(Typ)
	df["Functional"] = df["Functional"].fillna("Typ")
	
	# Only one null value so fill as the most frequent value(mode)
	df['KitchenQual'] = df['KitchenQual'].fillna("TA")  
	
	# Only one null value so fill as the most frequent value(mode)
	df['Electrical'] = df['Electrical'].fillna("SBrkr")
	
	# Very few null value so fill with the most frequent value(mode)
	df['SaleType'] = df['SaleType'].fillna("WD")
	
	# Null value likely means no masonry veneer
	df["MasVnrType"] = df["MasVnrType"].fillna("None") #so fill as "None" (since categorical feature)
	df["MasVnrArea"] = df["MasVnrArea"].fillna(0)      #so fill as o
	
	# Only one null value so fill as the most frequent value(mode)
	df['Exterior1st'] = df['Exterior1st'].fillna("VinylSd")
	df['Exterior2nd'] = df['Exterior2nd'].fillna("VinylSd")
	
	#MSZoning is general zoning classification,Very few null value so fill with the most frequent value(mode)
	df['MSZoning'] = df['MSZoning'].fillna("RL")
	
	#Null value likely means no Identified type of dwelling so fill as "None"
	df['MSSubClass'] = df['MSSubClass'].fillna("None")
	
	# Null value likely means No Garage, so fill as "None" (since these are categorical features)
	for col in ('GarageType', 'GarageFinish', 'GarageQual', 'GarageCond'):
		df[col] = df[col].fillna('None')
	
	# Null value likely means No Garage and no cars in garage, so fill as 0
	for col in ('GarageYrBlt', 'GarageArea', 'GarageCars'):
		df[col] = df[col].fillna(0)
	
	# Null value likely means No Basement, so fill as 0
	for col in ('BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF','TotalBsmtSF', 'BsmtFullBath', 'BsmtHalfBath'):
		df[col] = df[col].fillna(0)
	
	# Null value likely means No Basement, so fill as "None" (since these are categorical features)
	for col in ('BsmtQual', 'BsmtCond', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinType2'):
		df[col] = df[col].fillna('None')
	
	return df


def add_new_cols(df):
	
	df['Total_SF'] = df['TotalBsmtSF'] + df['1stFlrSF'] + df['2ndFlrSF']

	# df['Total_Bathrooms'] = (df['FullBath'] + (0.5 * float(df['HalfBath'])) + df['BsmtFullBath'] 
	#                          + (0.5 * float(df['BsmtHalfBath'])))

	df['Total_Porch_SF'] = (df['OpenPorchSF'] + df['3SsnPorch'] + df['EnclosedPorch'] + 
							df['ScreenPorch'] + df['WoodDeckSF'])

	df['Total_Square_Feet'] = (df['BsmtFinSF1'] + df['BsmtFinSF2'] + df['1stFlrSF'] + df['2ndFlrSF'])
	
	df['Total_Quality'] = df['OverallQual'] + df['OverallCond']
	
	return df

def write_csv(message):

	# Process the input data
	header = "Id,MSSubClass,MSZoning,LotFrontage,LotArea,Street,Alley,LotShape,LandContour,Utilities,LotConfig,LandSlope,Neighborhood,Condition1,Condition2,BldgType,HouseStyle,OverallQual,OverallCond,YearBuilt,YearRemodAdd,RoofStyle,RoofMatl,Exterior1st,Exterior2nd,MasVnrType,MasVnrArea,ExterQual,ExterCond,Foundation,BsmtQual,BsmtCond,BsmtExposure,BsmtFinType1,BsmtFinSF1,BsmtFinType2,BsmtFinSF2,BsmtUnfSF,TotalBsmtSF,Heating,HeatingQC,CentralAir,Electrical,1stFlrSF,2ndFlrSF,LowQualFinSF,GrLivArea,BsmtFullBath,BsmtHalfBath,FullBath,HalfBath,BedroomAbvGr,KitchenAbvGr,KitchenQual,TotRmsAbvGrd,Functional,Fireplaces,FireplaceQu,GarageType,GarageYrBlt,GarageFinish,GarageCars,GarageArea,GarageQual,GarageCond,PavedDrive,WoodDeckSF,OpenPorchSF,EnclosedPorch,3SsnPorch,ScreenPorch,PoolArea,PoolQC,Fence,MiscFeature,MiscVal,MoSold,YrSold,SaleType,SaleCondition\n"
	message = message[1:-1]
	f = open("test_entry.csv", "w")
	f.writelines([header, message])
	f.close()
	org = message.split(",")
	csv_path = "test_entry.csv"
	df_test = pd.read_csv(csv_path, sep = ',') 

	df_test.drop(['Id'], axis=1, inplace=True)
	df_test = missing(df_test)
	df_test = add_new_cols(df_test)
	df_test = pd.get_dummies(df_test)
	df_train = pickle.load(open("models/label.sav", "rb"))
	X_test = df_test.reindex(columns = df_train, fill_value=0)
	
	X_test.fillna(0)
	return X_test, org 

