import csv
import numpy as np
import pandas as pd
from sklearn import preprocessing, model_selection, metrics 

DATA_FILE = "./loans_full_schema.csv"

class Case1Data:
    def __init__(self):
        self.data = pd.read_csv(DATA_FILE)

    
    def distribution(self, field):
        field_data = self.data[field]
        dist_dict = {}
        for f in field_data:
            if f not in dist_dict:
                dist_dict[f] = 0
            dist_dict[f] += 1
        return dist_dict
    
    def avg_std(self, field1, field2):
        f1 = self.data[field1]
        f2 = self.data[field2]

        data = {}
        for x,y in zip(f1, f2):
            if x not in data:
                data[x] = []
            data[x].append(float(y))
        
        ret = {}
        for k,v in data.items():
            ret[k] = (np.average(v), np.std(v))
        return ret
    
    def get_num(self, field):
        ret = []
        for f in self.data[field]:
            if f=="NA":
                ret.append(None)
            else:
                ret.append(float(f))
        return ret


DISCARD_FIELDS = ["state", "emp_title", "interest_rate", "installment", "grade", "sub_grade", "issue_month", "loan_status", "initial_listing_status", "disbursement_method", "balance", "paid_total", "paid_principal", "paid_interest", "paid_late_fees"]
CATGORICAL_FIELDS = ["homeownership", "verified_income", "verification_income_joint", "loan_purpose", "application_type"]

class RegressionData:
    def __init__(self, train_test_split):
        data = pd.read_csv(DATA_FILE)

        self.scaler = preprocessing.StandardScaler()
        self.ohe = preprocessing.OneHotEncoder(sparse=False)

        columns_to_scale = list(set(data.keys()) - set(CATGORICAL_FIELDS) - set(DISCARD_FIELDS))

        scaled_columns = self.scaler.fit_transform(data[columns_to_scale].fillna(0)) 
        encoded_columns = self.ohe.fit_transform(data[CATGORICAL_FIELDS])

        processed_data = np.concatenate([scaled_columns, encoded_columns], axis=1)
        y = data["interest_rate"]

        self.xtrain, self.xtest, self.ytrain, self.ytest = model_selection.train_test_split(processed_data, y, train_size=train_test_split)
    
    def train(self, model):
        model.fit(self.xtrain, self.ytrain)
    
    def test(self, model):
        ypred = model.predict(self.xtest)
        
        return ypred


class ClassificationData:
    def __init__(self, ylab, train_test_split):
        data = pd.read_csv(DATA_FILE)

        self.scaler = preprocessing.StandardScaler()
        self.ohe = preprocessing.OneHotEncoder(sparse=False)

        columns_to_scale = list(set(data.keys()) - set(CATGORICAL_FIELDS) - set(DISCARD_FIELDS))

        scaled_columns = self.scaler.fit_transform(data[columns_to_scale].fillna(0)) 
        encoded_columns = self.ohe.fit_transform(data[CATGORICAL_FIELDS])

        processed_data = np.concatenate([scaled_columns, encoded_columns], axis=1)
        y = data[ylab]

        self.xtrain, self.xtest, self.ytrain, self.ytest = model_selection.train_test_split(processed_data, y, train_size=train_test_split)

        f1 = data[ylab]
        f2 = data["interest_rate"]

        self.transform = {}
        counts = {}
        for x,y in zip(f1, f2):
            if x not in self.transform:
                self.transform[x] = 0
                counts[x] = 0
            self.transform[x] += float(y)
            counts[x] += 1
        
        for t in self.transform:
            self.transform[t] /= counts[t]
        
        self.interest_test = data["interest_rate"][self.ytest.index]
        
    
    def train(self, model):
        model.fit(self.xtrain, self.ytrain)
    
    def test(self, model):
        ypred = model.predict(self.xtest)
        r2 = model.score(self.xtest, self.ytest)
        print(f' Accuracy: {r2}')

        return ypred
    
    def transform_interest(self, arr):
        return [self.transform[x] for x in arr]
    
    





                    
                    
                
