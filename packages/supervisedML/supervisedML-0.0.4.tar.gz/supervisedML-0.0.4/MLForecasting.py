import pandas as pd
import numpy as np
import seaborn as sns
from sklearn import model_selection
from sklearn.linear_model import LinearRegression, ElasticNet, Ridge, Lasso, RANSACRegressor, Lars, HuberRegressor, TheilSenRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor, RadiusNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import QuantileTransformer
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor, StackingRegressor, AdaBoostRegressor, BaggingRegressor, ExtraTreesRegressor, HistGradientBoostingRegressor, VotingRegressor, GradientBoostingRegressor
from sklearn.metrics import *
from sklearn.model_selection import train_test_split
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from math import sqrt
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

import warnings
warnings.filterwarnings("ignore")

class MLForecasting:
    def preprocess(self, df, test_size, random_state):
        le = LabelEncoder()
        df_encoded = pd.DataFrame()
        for column in df.columns:
            df_encoded[column] = le.fit_transform(df[column])
        X = df_encoded[df_encoded.columns[1:]]
        y = df_encoded[df_encoded.columns[0]]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

        de_X_test = X_test.copy()
        for column in X.columns:
            le.fit(df[column])
            de_X_test[column] = le.inverse_transform(X_test[column])

        return X_train, X_test, y_train, y_test, de_X_test
    

    def future_enconding(self, new_df, df):
        le = LabelEncoder()
        new_df_encoded = pd.DataFrame()
        for column in new_df.columns:
                new_df_encoded[column] = le.fit_transform(new_df[column])
        return new_df_encoded[df.columns[1:].tolist()]
    
    def regression_models(self, depth, df, fut_df, test_size, num_estimator, num_nonzero_coefs, random_state, num_neighbor, reg_para, epsilon, radius, learning_rate, loss, iter_):
        X_train, X_test, y_train, y_test, decoded_X_test = self.preprocess(df, test_size, random_state)
        new_df = self.future_enconding(fut_df, df)
        LR_model = LinearRegression()
        LR_model.fit(X_train, y_train)
        LR_test_prediction = LR_model.predict(X_test)
        LR_train_prediction = LR_model.predict(X_train)
        LR_future_prediction = LR_model.predict(new_df)
        DTR_model = DecisionTreeRegressor(max_depth=depth)
        DTR_model.fit(X_train, y_train)
        DTR_test_prediction = DTR_model.predict(X_test)
        DTR_train_prediction = DTR_model.predict(X_train)
        DTR_future_prediction = DTR_model.predict(new_df)
        RFR_model = RandomForestRegressor(n_estimators=num_estimator, oob_score=True, random_state=random_state)
        RFR_model.fit(X_train, y_train)
        RFR_test_prediction = RFR_model.predict(X_test)
        RFR_train_prediction = RFR_model.predict(X_train)
        RFR_future_prediction = RFR_model.predict(new_df)
        knn_model = KNeighborsRegressor(n_neighbors=num_neighbor)
        knn_model.fit(X_train, y_train)
        knn_test_prediction = knn_model.predict(X_test)
        knn_train_prediction = knn_model.predict(X_train)
        knn_future_prediction = knn_model.predict(new_df)
        EN_model = ElasticNet(random_state=random_state)
        EN_model.fit(X_train, y_train)
        EN_test_prediction = EN_model.predict(X_test)
        EN_train_prediction = EN_model.predict(X_train)
        EN_future_prediction = EN_model.predict(new_df)
        Lasso_model = Lasso()
        Lasso_model.fit(X_train, y_train)
        Lasso_test_prediction = Lasso_model.predict(X_test)
        Lasso_train_prediction = Lasso_model.predict(X_train)
        Lasso_future_prediction = Lasso_model.predict(new_df)
        Ridge_model = Ridge()
        Ridge_model.fit(X_train, y_train)
        Ridge_test_prediction = Ridge_model.predict(X_test)
        Ridge_train_prediction = Ridge_model.predict(X_train)
        Ridge_future_prediction = Ridge_model.predict(new_df)
        GBR_model = GradientBoostingRegressor(n_estimators = num_estimator, learning_rate = learning_rate, max_depth = depth, random_state=random_state, loss = loss)
        GBR_model.fit(X_train, y_train)
        GBR__test_pred = GBR_model.predict(X_test)
        GBR_train_prediction = GBR_model.predict(X_train)
        GBR_future_prediction = GBR_model.predict(new_df)
        VR_model = VotingRegressor(estimators=[('gb', GBR_model), ('rf', RFR_model), ('lr', LR_model)])
        VR_model.fit(X_train, y_train)
        VR_test_pred = VR_model.predict(X_test)
        VR_train_pred = VR_model.predict(X_train)
        VR_future_pred = VR_model.predict(new_df)
        H_model = HuberRegressor()
        H_model.fit(X_train, y_train)
        H_test_pred = H_model.predict(X_test)
        H_train_pred = H_model.predict(X_train)
        H_future_pred = H_model.predict(new_df)
        L_model = Lars(n_nonzero_coefs = num_nonzero_coefs)
        L_model.fit(X_train, y_train)
        L_test_pred = L_model.predict(X_test)
        L_train_pred = L_model.predict(X_train)
        L_future_pred = L_model.predict(new_df)
        RANSACR_model = RANSACRegressor(random_state=random_state)
        RANSACR_model.fit(X_train, y_train)
        RANSACR_test_pred = RANSACR_model.predict(X_test)
        RANSACR_train_pred = RANSACR_model.predict(X_train)
        RANSACR_future_pred = RANSACR_model.predict(new_df)
        SVR_model = make_pipeline(StandardScaler(), SVR(C=reg_para, epsilon=epsilon))
        SVR_model.fit(X_train, y_train)
        SVR_test_pred = SVR_model.predict(X_test)
        SVR_train_pred = SVR_model.predict(X_train)
        SVR_future_pred = SVR_model.predict(new_df)
        TSR_model = TheilSenRegressor(random_state=random_state)
        TSR_model.fit(X_train, y_train)
        TSR_test_pred = TSR_model.predict(X_test)
        TSR_train_pred = TSR_model.predict(X_train)
        TSR_future_pred = TSR_model.predict(new_df)
        HGBR_model = HistGradientBoostingRegressor()
        HGBR_model.fit(X_train, y_train)
        HGBR_test_pred = HGBR_model.predict(X_test)
        HGBR_train_pred = HGBR_model.predict(X_train)
        HGBR_future_pred = HGBR_model.predict(new_df)
        RNR_model = RadiusNeighborsRegressor(radius = radius)
        RNR_model.fit(X_train, y_train)
        RNR_test_pred = RNR_model.predict(X_test)
        RNR_train_pred = RNR_model.predict(X_train)
        RNR_future_pred = RNR_model.predict(new_df)
        HGBR_model = HistGradientBoostingRegressor()
        HGBR_model.fit(X_train, y_train)
        HGBR_test_pred = HGBR_model.predict(X_test)
        HGBR_train_pred = HGBR_model.predict(X_train)
        HGBR_future_pred = HGBR_model.predict(new_df)
        ET_model = ExtraTreesRegressor(n_estimators=num_estimator, random_state=random_state)
        ET_model.fit(X_train, y_train)
        ET_test_pred = ET_model.predict(X_test)
        ET_train_pred = ET_model.predict(X_train)
        ET_future_pred = ET_model.predict(new_df)
        ABR_model = AdaBoostRegressor(random_state=random_state, n_estimators=num_estimator)
        ABR_model.fit(X_train, y_train)
        ABR_test_pred = ABR_model.predict(X_test)
        ABR_train_pred = ABR_model.predict(X_train)
        ABR_future_pred = ABR_model.predict(new_df)
        BR_model = BaggingRegressor(base_estimator=RandomForestRegressor(n_estimators=num_estimator, oob_score=True, random_state=random_state), n_estimators=num_estimator, random_state=random_state)
        BR_model.fit(X_train, y_train)
        BR_test_pred = BR_model.predict(X_test)
        BR_train_pred = BR_model.predict(X_train)
        BR_future_pred = BR_model.predict(new_df)
        SR_model = StackingRegressor(estimators = [('rfr', RFR_model), ('gbr', GBR_model)])
        SR_model.fit(X_train, y_train)
        SR_test_pred = SR_model.predict(X_test)
        SR_train_pred = SR_model.predict(X_train)
        SR_future_pred = SR_model.predict(new_df)
        NNregressor = MLPRegressor(random_state=random_state, max_iter=iter_)
        NNregressor.fit(X_train, y_train)
        NN_test_pred = NNregressor.predict(X_test)
        NN_train_pred = NNregressor.predict(X_train)
        NN_future_pred = NNregressor.predict(new_df)

        return LR_test_prediction, DTR_test_prediction, RFR_test_prediction, knn_test_prediction, EN_test_prediction, Lasso_test_prediction, Ridge_test_prediction, GBR__test_pred, VR_test_pred, H_test_pred, L_test_pred, RANSACR_test_pred, SVR_test_pred, TSR_test_pred, HGBR_test_pred, RNR_test_pred, HGBR_test_pred, ET_test_pred, ABR_test_pred, BR_test_pred, SR_test_pred, NN_test_pred, LR_future_prediction, DTR_future_prediction, RFR_future_prediction, knn_future_prediction, EN_future_prediction, Lasso_future_prediction, Ridge_future_prediction, GBR_future_prediction, VR_future_pred, H_future_pred, L_future_pred, RANSACR_future_pred, SVR_future_pred, TSR_future_pred, HGBR_future_pred, RNR_future_pred, HGBR_future_pred, ET_future_pred, ABR_future_pred, BR_future_pred, SR_future_pred, NN_future_pred


    def mean_squared(self, df, fut_df, test_size, random_state, depth, num_estimator, num_nonzero_coefs, iter_, num_neighbor, reg_para, epsilon, radius, learning_rate, loss):
        new_df = self.future_enconding(fut_df, df)
        LR_test_prediction, DTR_test_prediction, RFR_test_prediction, knn_test_prediction, EN_test_prediction, Lasso_test_prediction, Ridge_test_prediction, GBR__test_pred, VR_test_pred, H_test_pred, L_test_pred, RANSACR_test_pred, SVR_test_pred, TSR_test_pred, HGBR_test_pred, RNR_test_pred, HGBR_test_pred, ET_test_pred, ABR_test_pred, BR_test_pred, SR_test_pred, NN_test_pred, LR_future_prediction, DTR_future_prediction, RFR_future_prediction, knn_future_prediction, EN_future_prediction, Lasso_future_prediction, Ridge_future_prediction, GBR_future_prediction, VR_future_pred, H_future_pred, L_future_pred, RANSACR_future_pred, SVR_future_pred, TSR_future_pred, HGBR_future_pred, RNR_future_pred, HGBR_future_pred, ET_future_pred, ABR_future_pred, BR_future_pred, SR_future_pred, NN_future_pred = self.regression_models(depth, df, fut_df, test_size, num_estimator, num_nonzero_coefs, random_state, num_neighbor, reg_para, epsilon, radius, learning_rate, loss, iter_)
        X_train, X_test, y_train, y_test, decoded_X_test = self.preprocess(df, test_size, random_state)
        
        pred_list = [LR_test_prediction, DTR_test_prediction, RFR_test_prediction, knn_test_prediction, EN_test_prediction, Lasso_test_prediction, Ridge_test_prediction, GBR__test_pred, VR_test_pred, H_test_pred, L_test_pred, RANSACR_test_pred, SVR_test_pred, TSR_test_pred, HGBR_test_pred, RNR_test_pred, HGBR_test_pred, ET_test_pred, ABR_test_pred, BR_test_pred, SR_test_pred, NN_test_pred]
        pred_fut = [LR_future_prediction, DTR_future_prediction, RFR_future_prediction, knn_future_prediction, EN_future_prediction, Lasso_future_prediction, Ridge_future_prediction, GBR_future_prediction, VR_future_pred, H_future_pred, L_future_pred, RANSACR_future_pred, SVR_future_pred, TSR_future_pred, HGBR_future_pred, RNR_future_pred, HGBR_future_pred, ET_future_pred, ABR_future_pred, BR_future_pred, SR_future_pred, NN_future_pred]
        biggest_err = np.sqrt(mean_squared_error(y_test,pred_list[0]))
        pred_fut = [LR_future_prediction, DTR_future_prediction, RFR_future_prediction, knn_future_prediction, EN_future_prediction, Lasso_future_prediction, Ridge_future_prediction, GBR_future_prediction, VR_future_pred, H_future_pred, L_future_pred, RANSACR_future_pred, SVR_future_pred, TSR_future_pred, HGBR_future_pred, RNR_future_pred, HGBR_future_pred, ET_future_pred, ABR_future_pred, BR_future_pred, SR_future_pred, NN_future_pred]
        biggest_pred = pred_list[0]
        biggest_fut = pred_fut[0]
        for i in range(len(pred_list)):
            temp_err = np.sqrt(mean_squared_error(y_test,pred_list[i]))
            temp_pred = pred_list[i]
            temp_fut = pred_fut[i]
            if((temp_err <= biggest_err) & (len(str(round(temp_err))) == 2)  & (sum(temp_pred) > 0)):
                biggest_err = temp_err
                biggest_pred = temp_pred
                biggest_fut = temp_fut
        decoded_X_test.insert(0,'predictions',np.rint(biggest_pred).astype(int))
        fut_df.insert(0,'predictions',np.rint(biggest_fut).astype(int))
        return biggest_err, decoded_X_test.reset_index(drop = True), fut_df.reset_index(drop = True)
    
    def r2(self, df, fut_df, test_size, random_state, depth, num_estimator, num_nonzero_coefs, iter_, num_neighbor, reg_para, epsilon, radius, learning_rate, loss):
        new_df = self.future_enconding(fut_df, df)
        LR_test_prediction, DTR_test_prediction, RFR_test_prediction, knn_test_prediction, EN_test_prediction, Lasso_test_prediction, Ridge_test_prediction, GBR__test_pred, VR_test_pred, H_test_pred, L_test_pred, RANSACR_test_pred, SVR_test_pred, TSR_test_pred, HGBR_test_pred, RNR_test_pred, HGBR_test_pred, ET_test_pred, ABR_test_pred, BR_test_pred, SR_test_pred, NN_test_pred, LR_future_prediction, DTR_future_prediction, RFR_future_prediction, knn_future_prediction, EN_future_prediction, Lasso_future_prediction, Ridge_future_prediction, GBR_future_prediction, VR_future_pred, H_future_pred, L_future_pred, RANSACR_future_pred, SVR_future_pred, TSR_future_pred, HGBR_future_pred, RNR_future_pred, HGBR_future_pred, ET_future_pred, ABR_future_pred, BR_future_pred, SR_future_pred, NN_future_pred = self.regression_models(depth, df, fut_df, test_size, num_estimator, num_nonzero_coefs, random_state, num_neighbor, reg_para, epsilon, radius, learning_rate, loss, iter_)
        X_train, X_test, y_train, y_test, decoded_X_test = self.preprocess(df, test_size, random_state)
        
        pred_list = [LR_test_prediction, DTR_test_prediction, RFR_test_prediction, knn_test_prediction, EN_test_prediction, Lasso_test_prediction, Ridge_test_prediction, GBR__test_pred, VR_test_pred, H_test_pred, L_test_pred, RANSACR_test_pred, SVR_test_pred, TSR_test_pred, HGBR_test_pred, RNR_test_pred, HGBR_test_pred, ET_test_pred, ABR_test_pred, BR_test_pred, SR_test_pred, NN_test_pred]
        pred_fut = [LR_future_prediction, DTR_future_prediction, RFR_future_prediction, knn_future_prediction, EN_future_prediction, Lasso_future_prediction, Ridge_future_prediction, GBR_future_prediction, VR_future_pred, H_future_pred, L_future_pred, RANSACR_future_pred, SVR_future_pred, TSR_future_pred, HGBR_future_pred, RNR_future_pred, HGBR_future_pred, ET_future_pred, ABR_future_pred, BR_future_pred, SR_future_pred, NN_future_pred]
        biggest_err = r2_score(y_test,pred_list[0])
        biggest_pred = pred_list[0]
        biggest_fut = pred_fut[0]
        for i in range(len(pred_list)):
            temp_err = r2_score(y_test,pred_list[i])
            temp_pred = pred_list[i]
            temp_fut = pred_fut[i]
            if(temp_err >= biggest_err):
                biggest_err = temp_err
                biggest_pred = temp_pred
                biggest_fut = temp_fut
        decoded_X_test.insert(0,'predictions',np.rint(biggest_pred).astype(int))
        fut_df.insert(0,'predictions',np.rint(biggest_fut).astype(int))
        return biggest_err, decoded_X_test.reset_index(drop = True), fut_df.reset_index(drop = True)
    
    def mean_absolute(self, df, fut_df, test_size, random_state, depth, num_estimator, num_nonzero_coefs, iter_, num_neighbor, reg_para, epsilon, radius, learning_rate, loss):
        new_df = self.future_enconding(fut_df, df)
        LR_test_prediction, DTR_test_prediction, RFR_test_prediction, knn_test_prediction, EN_test_prediction, Lasso_test_prediction, Ridge_test_prediction, GBR__test_pred, VR_test_pred, H_test_pred, L_test_pred, RANSACR_test_pred, SVR_test_pred, TSR_test_pred, HGBR_test_pred, RNR_test_pred, HGBR_test_pred, ET_test_pred, ABR_test_pred, BR_test_pred, SR_test_pred, NN_test_pred, LR_future_prediction, DTR_future_prediction, RFR_future_prediction, knn_future_prediction, EN_future_prediction, Lasso_future_prediction, Ridge_future_prediction, GBR_future_prediction, VR_future_pred, H_future_pred, L_future_pred, RANSACR_future_pred, SVR_future_pred, TSR_future_pred, HGBR_future_pred, RNR_future_pred, HGBR_future_pred, ET_future_pred, ABR_future_pred, BR_future_pred, SR_future_pred, NN_future_pred = self.regression_models(depth, df, fut_df, test_size, num_estimator, num_nonzero_coefs, random_state, num_neighbor, reg_para, epsilon, radius, learning_rate, loss, iter_)
        X_train, X_test, y_train, y_test, decoded_X_test = self.preprocess(df, test_size, random_state)
        
        pred_list = [LR_test_prediction, DTR_test_prediction, RFR_test_prediction, knn_test_prediction, EN_test_prediction, Lasso_test_prediction, Ridge_test_prediction, GBR__test_pred, VR_test_pred, H_test_pred, L_test_pred, RANSACR_test_pred, SVR_test_pred, TSR_test_pred, HGBR_test_pred, RNR_test_pred, HGBR_test_pred, ET_test_pred, ABR_test_pred, BR_test_pred, SR_test_pred, NN_test_pred]
        pred_fut = [LR_future_prediction, DTR_future_prediction, RFR_future_prediction, knn_future_prediction, EN_future_prediction, Lasso_future_prediction, Ridge_future_prediction, GBR_future_prediction, VR_future_pred, H_future_pred, L_future_pred, RANSACR_future_pred, SVR_future_pred, TSR_future_pred, HGBR_future_pred, RNR_future_pred, HGBR_future_pred, ET_future_pred, ABR_future_pred, BR_future_pred, SR_future_pred, NN_future_pred]
        biggest_err = round(np.sqrt(mean_absolute_error(y_test,pred_list[0])))
        biggest_pred = pred_list[0]
        biggest_fut = pred_fut[0]
        for i in range(len(pred_list)):
            temp_err = round(np.sqrt(mean_absolute_error(y_test,pred_list[i])))
            temp_pred = pred_list[i]
            temp_fut = pred_fut[i]
            if((temp_err >= biggest_err) & (len(str(round(temp_err))) == 2)):
                biggest_err = temp_err
                biggest_pred = temp_pred
                biggest_fut = temp_fut
        decoded_X_test.insert(0,'predictions',np.rint(biggest_pred).astype(int))
        fut_df.insert(0,'predictions',np.rint(biggest_fut).astype(int))
        return biggest_err, decoded_X_test.reset_index(drop = True), fut_df.reset_index(drop = True)
    
    
    def explained_variance(self, df, fut_df, test_size, random_state, depth, num_estimator, num_nonzero_coefs, iter_, num_neighbor, reg_para, epsilon, radius, learning_rate, loss):
        new_df = self.future_enconding(fut_df, df)
        LR_test_prediction, DTR_test_prediction, RFR_test_prediction, knn_test_prediction, EN_test_prediction, Lasso_test_prediction, Ridge_test_prediction, GBR__test_pred, VR_test_pred, H_test_pred, L_test_pred, RANSACR_test_pred, SVR_test_pred, TSR_test_pred, HGBR_test_pred, RNR_test_pred, HGBR_test_pred, ET_test_pred, ABR_test_pred, BR_test_pred, SR_test_pred, NN_test_pred, LR_future_prediction, DTR_future_prediction, RFR_future_prediction, knn_future_prediction, EN_future_prediction, Lasso_future_prediction, Ridge_future_prediction, GBR_future_prediction, VR_future_pred, H_future_pred, L_future_pred, RANSACR_future_pred, SVR_future_pred, TSR_future_pred, HGBR_future_pred, RNR_future_pred, HGBR_future_pred, ET_future_pred, ABR_future_pred, BR_future_pred, SR_future_pred, NN_future_pred = self.regression_models(depth, df, fut_df, test_size, num_estimator, num_nonzero_coefs, random_state, num_neighbor, reg_para, epsilon, radius, learning_rate, loss, iter_)
        X_train, X_test, y_train, y_test, decoded_X_test = self.preprocess(df, test_size, random_state)
        
        pred_list = [LR_test_prediction, DTR_test_prediction, RFR_test_prediction, knn_test_prediction, EN_test_prediction, Lasso_test_prediction, Ridge_test_prediction, GBR__test_pred, VR_test_pred, H_test_pred, L_test_pred, RANSACR_test_pred, SVR_test_pred, TSR_test_pred, HGBR_test_pred, RNR_test_pred, HGBR_test_pred, ET_test_pred, ABR_test_pred, BR_test_pred, SR_test_pred, NN_test_pred]
        pred_fut = [LR_future_prediction, DTR_future_prediction, RFR_future_prediction, knn_future_prediction, EN_future_prediction, Lasso_future_prediction, Ridge_future_prediction, GBR_future_prediction, VR_future_pred, H_future_pred, L_future_pred, RANSACR_future_pred, SVR_future_pred, TSR_future_pred, HGBR_future_pred, RNR_future_pred, HGBR_future_pred, ET_future_pred, ABR_future_pred, BR_future_pred, SR_future_pred, NN_future_pred]
        biggest_err = explained_variance_score(y_test,pred_list[0])
        biggest_pred = pred_list[0]
        biggest_fut = pred_fut[0]
        for i in range(len(pred_list)):
            temp_err = explained_variance_score(y_test,pred_list[i])
            temp_pred = pred_list[i]
            temp_fut = pred_fut[i]
            if((temp_err >= biggest_err) & (len(str(round(temp_err))) == 2)):
                biggest_err = temp_err
                biggest_pred = temp_pred
                biggest_fut = temp_fut
        decoded_X_test.insert(0,'predictions',np.rint(biggest_pred).astype(int))
        fut_df.insert(0,'predictions',np.rint(biggest_fut).astype(int))
        return biggest_err, decoded_X_test.reset_index(drop = True), fut_df.reset_index(drop = True)
    
    
    def max_error_(self, df, fut_df, test_size, random_state, depth, num_estimator, num_nonzero_coefs, iter_, num_neighbor, reg_para, epsilon, radius, learning_rate, loss):
        new_df = self.future_enconding(fut_df, df)
        LR_test_prediction, DTR_test_prediction, RFR_test_prediction, knn_test_prediction, EN_test_prediction, Lasso_test_prediction, Ridge_test_prediction, GBR__test_pred, VR_test_pred, H_test_pred, L_test_pred, RANSACR_test_pred, SVR_test_pred, TSR_test_pred, HGBR_test_pred, RNR_test_pred, HGBR_test_pred, ET_test_pred, ABR_test_pred, BR_test_pred, SR_test_pred, NN_test_pred, LR_future_prediction, DTR_future_prediction, RFR_future_prediction, knn_future_prediction, EN_future_prediction, Lasso_future_prediction, Ridge_future_prediction, GBR_future_prediction, VR_future_pred, H_future_pred, L_future_pred, RANSACR_future_pred, SVR_future_pred, TSR_future_pred, HGBR_future_pred, RNR_future_pred, HGBR_future_pred, ET_future_pred, ABR_future_pred, BR_future_pred, SR_future_pred, NN_future_pred = self.regression_models(depth, df, fut_df, test_size, num_estimator, num_nonzero_coefs, random_state, num_neighbor, reg_para, epsilon, radius, learning_rate, loss, iter_)
        X_train, X_test, y_train, y_test, decoded_X_test = self.preprocess(df, test_size, random_state)
        
        pred_list = [LR_test_prediction, DTR_test_prediction, RFR_test_prediction, knn_test_prediction, EN_test_prediction, Lasso_test_prediction, Ridge_test_prediction, GBR__test_pred, VR_test_pred, H_test_pred, L_test_pred, RANSACR_test_pred, SVR_test_pred, TSR_test_pred, HGBR_test_pred, RNR_test_pred, HGBR_test_pred, ET_test_pred, ABR_test_pred, BR_test_pred, SR_test_pred, NN_test_pred]
        pred_fut = [LR_future_prediction, DTR_future_prediction, RFR_future_prediction, knn_future_prediction, EN_future_prediction, Lasso_future_prediction, Ridge_future_prediction, GBR_future_prediction, VR_future_pred, H_future_pred, L_future_pred, RANSACR_future_pred, SVR_future_pred, TSR_future_pred, HGBR_future_pred, RNR_future_pred, HGBR_future_pred, ET_future_pred, ABR_future_pred, BR_future_pred, SR_future_pred, NN_future_pred]
        biggest_err = max_error(y_test,pred_list[0])
        biggest_pred = pred_list[0]
        biggest_fut = pred_fut[0]
        for i in range(len(pred_list)):
            temp_err = max_error(y_test,pred_list[i])
            temp_pred = pred_list[i]
            temp_fut = pred_fut[i]
            if((temp_err >= biggest_err) & (len(str(round(temp_err))) == 2)):
                biggest_err = temp_err
                biggest_pred = temp_pred
                biggest_fut = temp_fut
        decoded_X_test.insert(0,'predictions',np.rint(biggest_pred).astype(int))
        fut_df.insert(0,'predictions',np.rint(biggest_fut).astype(int))
        return biggest_err, decoded_X_test.reset_index(drop = True), fut_df.reset_index(drop = True)
    
    def mean_squared_log(self, df, fut_df, test_size, random_state, depth, num_estimator, num_nonzero_coefs, iter_, num_neighbor, reg_para, epsilon, radius, learning_rate, loss):
        new_df = self.future_enconding(fut_df, df)
        LR_test_prediction, DTR_test_prediction, RFR_test_prediction, knn_test_prediction, EN_test_prediction, Lasso_test_prediction, Ridge_test_prediction, GBR__test_pred, VR_test_pred, H_test_pred, L_test_pred, RANSACR_test_pred, SVR_test_pred, TSR_test_pred, HGBR_test_pred, RNR_test_pred, HGBR_test_pred, ET_test_pred, ABR_test_pred, BR_test_pred, SR_test_pred, NN_test_pred, LR_future_prediction, DTR_future_prediction, RFR_future_prediction, knn_future_prediction, EN_future_prediction, Lasso_future_prediction, Ridge_future_prediction, GBR_future_prediction, VR_future_pred, H_future_pred, L_future_pred, RANSACR_future_pred, SVR_future_pred, TSR_future_pred, HGBR_future_pred, RNR_future_pred, HGBR_future_pred, ET_future_pred, ABR_future_pred, BR_future_pred, SR_future_pred, NN_future_pred = self.regression_models(depth, df, fut_df, test_size, num_estimator, num_nonzero_coefs, random_state, num_neighbor, reg_para, epsilon, radius, learning_rate, loss, iter_)
        X_train, X_test, y_train, y_test, decoded_X_test = self.preprocess(df, test_size, random_state)
        
        pred_list = [LR_test_prediction, DTR_test_prediction, RFR_test_prediction, knn_test_prediction, EN_test_prediction, Lasso_test_prediction, Ridge_test_prediction, GBR__test_pred, VR_test_pred, H_test_pred, L_test_pred, RANSACR_test_pred, SVR_test_pred, TSR_test_pred, HGBR_test_pred, RNR_test_pred, HGBR_test_pred, ET_test_pred, ABR_test_pred, BR_test_pred, SR_test_pred, NN_test_pred]
        pred_fut = [LR_future_prediction, DTR_future_prediction, RFR_future_prediction, knn_future_prediction, EN_future_prediction, Lasso_future_prediction, Ridge_future_prediction, GBR_future_prediction, VR_future_pred, H_future_pred, L_future_pred, RANSACR_future_pred, SVR_future_pred, TSR_future_pred, HGBR_future_pred, RNR_future_pred, HGBR_future_pred, ET_future_pred, ABR_future_pred, BR_future_pred, SR_future_pred, NN_future_pred]
        biggest_err = mean_squared_log_error(y_test,pred_list[0])
        biggest_pred = pred_list[0]
        biggest_fut = pred_fut[0]
        for i in range(len(pred_list)):
            if(sum([1 for i in pred_list[i].tolist() if i<0 ]) <0):
                temp_err = mean_squared_log_error(y_test,pred_list[i])
                temp_pred = pred_list[i]
                temp_fut = pred_fut[i]
                if((temp_err >= biggest_err) & (len(str(round(temp_err))) == 2)):
                    biggest_err = temp_err
                    biggest_pred = temp_pred
                    biggest_fut = temp_fut
        decoded_X_test.insert(0,'predictions',np.rint(biggest_pred).astype(int))
        fut_df.insert(0,'predictions',np.rint(biggest_fut).astype(int))
        return biggest_err, decoded_X_test.reset_index(drop = True), fut_df.reset_index(drop = True)
    
    
    def median_abs_error(self, df, fut_df, test_size, random_state, depth, num_estimator, num_nonzero_coefs, iter_, num_neighbor, reg_para, epsilon, radius, learning_rate, loss):
        new_df = self.future_enconding(fut_df, df)
        LR_test_prediction, DTR_test_prediction, RFR_test_prediction, knn_test_prediction, EN_test_prediction, Lasso_test_prediction, Ridge_test_prediction, GBR__test_pred, VR_test_pred, H_test_pred, L_test_pred, RANSACR_test_pred, SVR_test_pred, TSR_test_pred, HGBR_test_pred, RNR_test_pred, HGBR_test_pred, ET_test_pred, ABR_test_pred, BR_test_pred, SR_test_pred, NN_test_pred, LR_future_prediction, DTR_future_prediction, RFR_future_prediction, knn_future_prediction, EN_future_prediction, Lasso_future_prediction, Ridge_future_prediction, GBR_future_prediction, VR_future_pred, H_future_pred, L_future_pred, RANSACR_future_pred, SVR_future_pred, TSR_future_pred, HGBR_future_pred, RNR_future_pred, HGBR_future_pred, ET_future_pred, ABR_future_pred, BR_future_pred, SR_future_pred, NN_future_pred = self.regression_models(depth, df, fut_df, test_size, num_estimator, num_nonzero_coefs, random_state, num_neighbor, reg_para, epsilon, radius, learning_rate, loss, iter_)
        X_train, X_test, y_train, y_test, decoded_X_test = self.preprocess(df, test_size, random_state)
        
        pred_list = [LR_test_prediction, DTR_test_prediction, RFR_test_prediction, knn_test_prediction, EN_test_prediction, Lasso_test_prediction, Ridge_test_prediction, GBR__test_pred, VR_test_pred, H_test_pred, L_test_pred, RANSACR_test_pred, SVR_test_pred, TSR_test_pred, HGBR_test_pred, RNR_test_pred, HGBR_test_pred, ET_test_pred, ABR_test_pred, BR_test_pred, SR_test_pred, NN_test_pred]
        pred_fut = [LR_future_prediction, DTR_future_prediction, RFR_future_prediction, knn_future_prediction, EN_future_prediction, Lasso_future_prediction, Ridge_future_prediction, GBR_future_prediction, VR_future_pred, H_future_pred, L_future_pred, RANSACR_future_pred, SVR_future_pred, TSR_future_pred, HGBR_future_pred, RNR_future_pred, HGBR_future_pred, ET_future_pred, ABR_future_pred, BR_future_pred, SR_future_pred, NN_future_pred]
        biggest_err = median_absolute_error(y_test,pred_list[0])
        biggest_pred = pred_list[0]
        biggest_fut = pred_fut[0]
        for i in range(len(pred_list)):
            if(sum([1 for i in pred_list[i].tolist() if i<0 ]) <0):
                temp_err = median_absolute_error(y_test,pred_list[i])
                temp_pred = pred_list[i]
                temp_fut = pred_fut[i]
                if((temp_err >= biggest_err) & (len(str(round(temp_err))) == 2)):
                    biggest_err = temp_err
                    biggest_pred = temp_pred
                    biggest_fut = temp_fut
        decoded_X_test.insert(0,'predictions',np.rint(biggest_pred).astype(int))
        fut_df.insert(0,'predictions',np.rint(biggest_fut).astype(int))
        return biggest_err, decoded_X_test.reset_index(drop = True), fut_df.reset_index(drop = True)


    
    def mnbs_percentage_error(self, df, fut_df, test_size, random_state, depth, num_estimator, num_nonzero_coefs, iter_, num_neighbor, reg_para, epsilon, radius, learning_rate, loss):
        new_df = self.future_enconding(fut_df, df)
        LR_test_prediction, DTR_test_prediction, RFR_test_prediction, knn_test_prediction, EN_test_prediction, Lasso_test_prediction, Ridge_test_prediction, GBR__test_pred, VR_test_pred, H_test_pred, L_test_pred, RANSACR_test_pred, SVR_test_pred, TSR_test_pred, HGBR_test_pred, RNR_test_pred, HGBR_test_pred, ET_test_pred, ABR_test_pred, BR_test_pred, SR_test_pred, NN_test_pred, LR_future_prediction, DTR_future_prediction, RFR_future_prediction, knn_future_prediction, EN_future_prediction, Lasso_future_prediction, Ridge_future_prediction, GBR_future_prediction, VR_future_pred, H_future_pred, L_future_pred, RANSACR_future_pred, SVR_future_pred, TSR_future_pred, HGBR_future_pred, RNR_future_pred, HGBR_future_pred, ET_future_pred, ABR_future_pred, BR_future_pred, SR_future_pred, NN_future_pred = self.regression_models(depth, df, fut_df, test_size, num_estimator, num_nonzero_coefs, random_state, num_neighbor, reg_para, epsilon, radius, learning_rate, loss, iter_)
        X_train, X_test, y_train, y_test, decoded_X_test = self.preprocess(df, test_size, random_state)
        
        pred_list = [LR_test_prediction, DTR_test_prediction, RFR_test_prediction, knn_test_prediction, EN_test_prediction, Lasso_test_prediction, Ridge_test_prediction, GBR__test_pred, VR_test_pred, H_test_pred, L_test_pred, RANSACR_test_pred, SVR_test_pred, TSR_test_pred, HGBR_test_pred, RNR_test_pred, HGBR_test_pred, ET_test_pred, ABR_test_pred, BR_test_pred, SR_test_pred, NN_test_pred]
        pred_fut = [LR_future_prediction, DTR_future_prediction, RFR_future_prediction, knn_future_prediction, EN_future_prediction, Lasso_future_prediction, Ridge_future_prediction, GBR_future_prediction, VR_future_pred, H_future_pred, L_future_pred, RANSACR_future_pred, SVR_future_pred, TSR_future_pred, HGBR_future_pred, RNR_future_pred, HGBR_future_pred, ET_future_pred, ABR_future_pred, BR_future_pred, SR_future_pred, NN_future_pred]
        biggest_err = mean_absolute_percentage_error(y_test,pred_list[0])
        biggest_pred = pred_list[0]
        biggest_fut = pred_fut[0]
        for i in range(len(pred_list)):
            if(sum([1 for i in pred_list[i].tolist() if i<0 ]) <0):
                temp_err = mean_absolute_percentage_error(y_test,pred_list[i])
                temp_pred = pred_list[i]
                temp_fut = pred_fut[i]
                if((temp_err >= biggest_err) & (len(str(round(temp_err))) == 2)):
                    biggest_err = temp_err
                    biggest_pred = temp_pred
                    biggest_fut = temp_fut
        decoded_X_test.insert(0,'predictions',np.rint(biggest_pred).astype(int))
        fut_df.insert(0,'predictions',np.rint(biggest_fut).astype(int))
        return biggest_err, decoded_X_test.reset_index(drop = True), fut_df.reset_index(drop = True)
    
    
    def mean_poisson_dev(self, df, fut_df, test_size, random_state, depth, num_estimator, num_nonzero_coefs, iter_, num_neighbor, reg_para, epsilon, radius, learning_rate, loss):
        new_df = self.future_enconding(fut_df, df)
        LR_test_prediction, DTR_test_prediction, RFR_test_prediction, knn_test_prediction, EN_test_prediction, Lasso_test_prediction, Ridge_test_prediction, GBR__test_pred, VR_test_pred, H_test_pred, L_test_pred, RANSACR_test_pred, SVR_test_pred, TSR_test_pred, HGBR_test_pred, RNR_test_pred, HGBR_test_pred, ET_test_pred, ABR_test_pred, BR_test_pred, SR_test_pred, NN_test_pred, LR_future_prediction, DTR_future_prediction, RFR_future_prediction, knn_future_prediction, EN_future_prediction, Lasso_future_prediction, Ridge_future_prediction, GBR_future_prediction, VR_future_pred, H_future_pred, L_future_pred, RANSACR_future_pred, SVR_future_pred, TSR_future_pred, HGBR_future_pred, RNR_future_pred, HGBR_future_pred, ET_future_pred, ABR_future_pred, BR_future_pred, SR_future_pred, NN_future_pred = self.regression_models(depth, df, fut_df, test_size, num_estimator, num_nonzero_coefs, random_state, num_neighbor, reg_para, epsilon, radius, learning_rate, loss, iter_)
        X_train, X_test, y_train, y_test, decoded_X_test = self.preprocess(df, test_size, random_state)
        
        pred_list = [LR_test_prediction, DTR_test_prediction, RFR_test_prediction, knn_test_prediction, EN_test_prediction, Lasso_test_prediction, Ridge_test_prediction, GBR__test_pred, VR_test_pred, H_test_pred, L_test_pred, RANSACR_test_pred, SVR_test_pred, TSR_test_pred, HGBR_test_pred, RNR_test_pred, HGBR_test_pred, ET_test_pred, ABR_test_pred, BR_test_pred, SR_test_pred, NN_test_pred]
        pred_fut = [LR_future_prediction, DTR_future_prediction, RFR_future_prediction, knn_future_prediction, EN_future_prediction, Lasso_future_prediction, Ridge_future_prediction, GBR_future_prediction, VR_future_pred, H_future_pred, L_future_pred, RANSACR_future_pred, SVR_future_pred, TSR_future_pred, HGBR_future_pred, RNR_future_pred, HGBR_future_pred, ET_future_pred, ABR_future_pred, BR_future_pred, SR_future_pred, NN_future_pred]
        biggest_err = mean_poisson_deviance(y_test,pred_list[0])
        biggest_pred = pred_list[0]
        biggest_fut = pred_fut[0]
        for i in range(len(pred_list)):
            if(sum([1 for i in pred_list[i].tolist() if i<0 ]) <0):
                temp_err = mean_poisson_deviance(y_test,pred_list[i])
                temp_pred = pred_list[i]
                temp_fut = pred_fut[i]
                if((temp_err >= biggest_err) & (len(str(round(temp_err))) == 2)):
                    biggest_err = temp_err
                    biggest_pred = temp_pred
                    biggest_fut = temp_fut
        decoded_X_test.insert(0,'predictions',np.rint(biggest_pred).astype(int))
        fut_df.insert(0,'predictions',np.rint(biggest_fut).astype(int))
        return biggest_err, decoded_X_test.reset_index(drop = True), fut_df.reset_index(drop = True)
    
    def d2t_score(self, df, fut_df, test_size, random_state, depth, num_estimator, num_nonzero_coefs, iter_, num_neighbor, reg_para, epsilon, radius, learning_rate, loss):
        new_df = self.future_enconding(fut_df, df)
        LR_test_prediction, DTR_test_prediction, RFR_test_prediction, knn_test_prediction, EN_test_prediction, Lasso_test_prediction, Ridge_test_prediction, GBR__test_pred, VR_test_pred, H_test_pred, L_test_pred, RANSACR_test_pred, SVR_test_pred, TSR_test_pred, HGBR_test_pred, RNR_test_pred, HGBR_test_pred, ET_test_pred, ABR_test_pred, BR_test_pred, SR_test_pred, NN_test_pred, LR_future_prediction, DTR_future_prediction, RFR_future_prediction, knn_future_prediction, EN_future_prediction, Lasso_future_prediction, Ridge_future_prediction, GBR_future_prediction, VR_future_pred, H_future_pred, L_future_pred, RANSACR_future_pred, SVR_future_pred, TSR_future_pred, HGBR_future_pred, RNR_future_pred, HGBR_future_pred, ET_future_pred, ABR_future_pred, BR_future_pred, SR_future_pred, NN_future_pred = self.regression_models(depth, df, fut_df, test_size, num_estimator, num_nonzero_coefs, random_state, num_neighbor, reg_para, epsilon, radius, learning_rate, loss, iter_)
        X_train, X_test, y_train, y_test, decoded_X_test = self.preprocess(df, test_size, random_state)
        
        pred_list = [LR_test_prediction, DTR_test_prediction, RFR_test_prediction, knn_test_prediction, EN_test_prediction, Lasso_test_prediction, Ridge_test_prediction, GBR__test_pred, VR_test_pred, H_test_pred, L_test_pred, RANSACR_test_pred, SVR_test_pred, TSR_test_pred, HGBR_test_pred, RNR_test_pred, HGBR_test_pred, ET_test_pred, ABR_test_pred, BR_test_pred, SR_test_pred, NN_test_pred]
        pred_fut = [LR_future_prediction, DTR_future_prediction, RFR_future_prediction, knn_future_prediction, EN_future_prediction, Lasso_future_prediction, Ridge_future_prediction, GBR_future_prediction, VR_future_pred, H_future_pred, L_future_pred, RANSACR_future_pred, SVR_future_pred, TSR_future_pred, HGBR_future_pred, RNR_future_pred, HGBR_future_pred, ET_future_pred, ABR_future_pred, BR_future_pred, SR_future_pred, NN_future_pred]
        biggest_err = d2_tweedie_score(y_test,pred_list[0])
        biggest_pred = pred_list[0]
        biggest_fut = pred_fut[0]
        for i in range(len(pred_list)):
            if(sum([1 for i in pred_list[i].tolist() if i<0 ]) <0):
                temp_err = d2_tweedie_score(y_test,pred_list[i])
                temp_pred = pred_list[i]
                temp_fut = pred_fut[i]
                if((temp_err >= biggest_err) & (len(str(round(temp_err))) == 2)):
                    biggest_err = temp_err
                    biggest_pred = temp_pred
                    biggest_fut = temp_fut
        decoded_X_test.insert(0,'predictions',np.rint(biggest_pred).astype(int))
        fut_df.insert(0,'predictions',np.rint(biggest_fut).astype(int))
        return biggest_err, decoded_X_test.reset_index(drop = True), fut_df.reset_index(drop = True)
    
    def d2p_score(self, df, fut_df, test_size, random_state, depth, num_estimator, num_nonzero_coefs, iter_, num_neighbor, reg_para, epsilon, radius, learning_rate, loss):
        new_df = self.future_enconding(fut_df, df)
        LR_test_prediction, DTR_test_prediction, RFR_test_prediction, knn_test_prediction, EN_test_prediction, Lasso_test_prediction, Ridge_test_prediction, GBR__test_pred, VR_test_pred, H_test_pred, L_test_pred, RANSACR_test_pred, SVR_test_pred, TSR_test_pred, HGBR_test_pred, RNR_test_pred, HGBR_test_pred, ET_test_pred, ABR_test_pred, BR_test_pred, SR_test_pred, NN_test_pred, LR_future_prediction, DTR_future_prediction, RFR_future_prediction, knn_future_prediction, EN_future_prediction, Lasso_future_prediction, Ridge_future_prediction, GBR_future_prediction, VR_future_pred, H_future_pred, L_future_pred, RANSACR_future_pred, SVR_future_pred, TSR_future_pred, HGBR_future_pred, RNR_future_pred, HGBR_future_pred, ET_future_pred, ABR_future_pred, BR_future_pred, SR_future_pred, NN_future_pred = self.regression_models(depth, df, fut_df, test_size, num_estimator, num_nonzero_coefs, random_state, num_neighbor, reg_para, epsilon, radius, learning_rate, loss, iter_)
        X_train, X_test, y_train, y_test, decoded_X_test = self.preprocess(df, test_size, random_state)
        
        pred_list = [LR_test_prediction, DTR_test_prediction, RFR_test_prediction, knn_test_prediction, EN_test_prediction, Lasso_test_prediction, Ridge_test_prediction, GBR__test_pred, VR_test_pred, H_test_pred, L_test_pred, RANSACR_test_pred, SVR_test_pred, TSR_test_pred, HGBR_test_pred, RNR_test_pred, HGBR_test_pred, ET_test_pred, ABR_test_pred, BR_test_pred, SR_test_pred, NN_test_pred]
        pred_fut = [LR_future_prediction, DTR_future_prediction, RFR_future_prediction, knn_future_prediction, EN_future_prediction, Lasso_future_prediction, Ridge_future_prediction, GBR_future_prediction, VR_future_pred, H_future_pred, L_future_pred, RANSACR_future_pred, SVR_future_pred, TSR_future_pred, HGBR_future_pred, RNR_future_pred, HGBR_future_pred, ET_future_pred, ABR_future_pred, BR_future_pred, SR_future_pred, NN_future_pred]
        biggest_err = d2_pinball_score(y_test,pred_list[0])
        biggest_pred = pred_list[0]
        biggest_fut = pred_fut[0]
        for i in range(len(pred_list)):
            if(sum([1 for i in pred_list[i].tolist() if i<0 ]) <0):
                temp_err = d2_pinball_score(y_test,pred_list[i])
                temp_pred = pred_list[i]
                temp_fut = pred_fut[i]
                if((temp_err >= biggest_err) & (len(str(round(temp_err))) == 2)):
                    biggest_err = temp_err
                    biggest_pred = temp_pred
                    biggest_fut = temp_fut
        decoded_X_test.insert(0,'predictions',np.rint(biggest_pred).astype(int))
        fut_df.insert(0,'predictions',np.rint(biggest_fut).astype(int))
        return biggest_err, decoded_X_test.reset_index(drop = True), fut_df.reset_index(drop = True)
    
    def d2ab_error_score(self, df, fut_df, test_size, random_state, depth, num_estimator, num_nonzero_coefs, iter_, num_neighbor, reg_para, epsilon, radius, learning_rate, loss):
        new_df = self.future_enconding(fut_df, df)
        LR_test_prediction, DTR_test_prediction, RFR_test_prediction, knn_test_prediction, EN_test_prediction, Lasso_test_prediction, Ridge_test_prediction, GBR__test_pred, VR_test_pred, H_test_pred, L_test_pred, RANSACR_test_pred, SVR_test_pred, TSR_test_pred, HGBR_test_pred, RNR_test_pred, HGBR_test_pred, ET_test_pred, ABR_test_pred, BR_test_pred, SR_test_pred, NN_test_pred, LR_future_prediction, DTR_future_prediction, RFR_future_prediction, knn_future_prediction, EN_future_prediction, Lasso_future_prediction, Ridge_future_prediction, GBR_future_prediction, VR_future_pred, H_future_pred, L_future_pred, RANSACR_future_pred, SVR_future_pred, TSR_future_pred, HGBR_future_pred, RNR_future_pred, HGBR_future_pred, ET_future_pred, ABR_future_pred, BR_future_pred, SR_future_pred, NN_future_pred = self.regression_models(depth, df, fut_df, test_size, num_estimator, num_nonzero_coefs, random_state, num_neighbor, reg_para, epsilon, radius, learning_rate, loss, iter_)
        X_train, X_test, y_train, y_test, decoded_X_test = self.preprocess(df, test_size, random_state)
        
        pred_list = [LR_test_prediction, DTR_test_prediction, RFR_test_prediction, knn_test_prediction, EN_test_prediction, Lasso_test_prediction, Ridge_test_prediction, GBR__test_pred, VR_test_pred, H_test_pred, L_test_pred, RANSACR_test_pred, SVR_test_pred, TSR_test_pred, HGBR_test_pred, RNR_test_pred, HGBR_test_pred, ET_test_pred, ABR_test_pred, BR_test_pred, SR_test_pred, NN_test_pred]
        pred_fut = [LR_future_prediction, DTR_future_prediction, RFR_future_prediction, knn_future_prediction, EN_future_prediction, Lasso_future_prediction, Ridge_future_prediction, GBR_future_prediction, VR_future_pred, H_future_pred, L_future_pred, RANSACR_future_pred, SVR_future_pred, TSR_future_pred, HGBR_future_pred, RNR_future_pred, HGBR_future_pred, ET_future_pred, ABR_future_pred, BR_future_pred, SR_future_pred, NN_future_pred]
        biggest_err = d2_absolute_error_score(y_test,pred_list[0])
        biggest_pred = pred_list[0]
        biggest_fut = pred_fut[0]
        for i in range(len(pred_list)):
            if(sum([1 for i in pred_list[i].tolist() if i<0 ]) <0):
                temp_err = d2_absolute_error_score(y_test,pred_list[i])
                temp_pred = pred_list[i]
                temp_fut = pred_fut[i]
                if((temp_err >= biggest_err) & (len(str(round(temp_err))) == 2)):
                    biggest_err = temp_err
                    biggest_pred = temp_pred
                    biggest_fut = temp_fut
        decoded_X_test.insert(0,'predictions',np.rint(biggest_pred).astype(int))
        fut_df.insert(0,'predictions',np.rint(biggest_fut).astype(int))
        return biggest_err, decoded_X_test.reset_index(drop = True), fut_df.reset_index(drop = True)
    
    def meanp_loss(self, df, fut_df, test_size, random_state, depth, num_estimator, num_nonzero_coefs, iter_, num_neighbor, reg_para, epsilon, radius, learning_rate, loss):
        new_df = self.future_enconding(fut_df, df)
        LR_test_prediction, DTR_test_prediction, RFR_test_prediction, knn_test_prediction, EN_test_prediction, Lasso_test_prediction, Ridge_test_prediction, GBR__test_pred, VR_test_pred, H_test_pred, L_test_pred, RANSACR_test_pred, SVR_test_pred, TSR_test_pred, HGBR_test_pred, RNR_test_pred, HGBR_test_pred, ET_test_pred, ABR_test_pred, BR_test_pred, SR_test_pred, NN_test_pred, LR_future_prediction, DTR_future_prediction, RFR_future_prediction, knn_future_prediction, EN_future_prediction, Lasso_future_prediction, Ridge_future_prediction, GBR_future_prediction, VR_future_pred, H_future_pred, L_future_pred, RANSACR_future_pred, SVR_future_pred, TSR_future_pred, HGBR_future_pred, RNR_future_pred, HGBR_future_pred, ET_future_pred, ABR_future_pred, BR_future_pred, SR_future_pred, NN_future_pred = self.regression_models(depth, df, fut_df, test_size, num_estimator, num_nonzero_coefs, random_state, num_neighbor, reg_para, epsilon, radius, learning_rate, loss, iter_)
        X_train, X_test, y_train, y_test, decoded_X_test = self.preprocess(df, test_size, random_state)
        
        pred_list = [LR_test_prediction, DTR_test_prediction, RFR_test_prediction, knn_test_prediction, EN_test_prediction, Lasso_test_prediction, Ridge_test_prediction, GBR__test_pred, VR_test_pred, H_test_pred, L_test_pred, RANSACR_test_pred, SVR_test_pred, TSR_test_pred, HGBR_test_pred, RNR_test_pred, HGBR_test_pred, ET_test_pred, ABR_test_pred, BR_test_pred, SR_test_pred, NN_test_pred]
        pred_fut = [LR_future_prediction, DTR_future_prediction, RFR_future_prediction, knn_future_prediction, EN_future_prediction, Lasso_future_prediction, Ridge_future_prediction, GBR_future_prediction, VR_future_pred, H_future_pred, L_future_pred, RANSACR_future_pred, SVR_future_pred, TSR_future_pred, HGBR_future_pred, RNR_future_pred, HGBR_future_pred, ET_future_pred, ABR_future_pred, BR_future_pred, SR_future_pred, NN_future_pred]
        biggest_pred = pred_list[0]
        biggest_fut = pred_fut[0]
        biggest_err = 0
        for i in range(len(pred_list)):
            if(sum([1 for i in pred_list[i].tolist() if i<0 ]) <0):
                biggest_err = mean_pinball_loss(y_test,pred_list[0])
                temp_err = mean_pinball_loss(y_test,pred_list[i])
                temp_pred = pred_list[i]
                temp_fut = pred_fut[i]
                if((temp_err >= biggest_err) & (len(str(round(temp_err))) == 2)):
                    biggest_err = temp_err
                    biggest_pred = temp_pred
                    biggest_fut = temp_fut
        decoded_X_test.insert(0,'predictions',np.rint(biggest_pred).astype(int))
        fut_df.insert(0,'predictions',np.rint(biggest_fut).astype(int))
        return biggest_err, decoded_X_test.reset_index(drop = True), fut_df.reset_index(drop = True)
    
    def mean_tweedie_dev(self, df, fut_df, test_size, random_state, depth, num_estimator, num_nonzero_coefs, iter_, num_neighbor, reg_para, epsilon, radius, learning_rate, loss):
        new_df = self.future_enconding(fut_df, df)
        LR_test_prediction, DTR_test_prediction, RFR_test_prediction, knn_test_prediction, EN_test_prediction, Lasso_test_prediction, Ridge_test_prediction, GBR__test_pred, VR_test_pred, H_test_pred, L_test_pred, RANSACR_test_pred, SVR_test_pred, TSR_test_pred, HGBR_test_pred, RNR_test_pred, HGBR_test_pred, ET_test_pred, ABR_test_pred, BR_test_pred, SR_test_pred, NN_test_pred, LR_future_prediction, DTR_future_prediction, RFR_future_prediction, knn_future_prediction, EN_future_prediction, Lasso_future_prediction, Ridge_future_prediction, GBR_future_prediction, VR_future_pred, H_future_pred, L_future_pred, RANSACR_future_pred, SVR_future_pred, TSR_future_pred, HGBR_future_pred, RNR_future_pred, HGBR_future_pred, ET_future_pred, ABR_future_pred, BR_future_pred, SR_future_pred, NN_future_pred = self.regression_models(depth, df, fut_df, test_size, num_estimator, num_nonzero_coefs, random_state, num_neighbor, reg_para, epsilon, radius, learning_rate, loss, iter_)
        X_train, X_test, y_train, y_test, decoded_X_test = self.preprocess(df, test_size, random_state)
        
        pred_list = [LR_test_prediction, DTR_test_prediction, RFR_test_prediction, knn_test_prediction, EN_test_prediction, Lasso_test_prediction, Ridge_test_prediction, GBR__test_pred, VR_test_pred, H_test_pred, L_test_pred, RANSACR_test_pred, SVR_test_pred, TSR_test_pred, HGBR_test_pred, RNR_test_pred, HGBR_test_pred, ET_test_pred, ABR_test_pred, BR_test_pred, SR_test_pred, NN_test_pred]
        pred_fut = [LR_future_prediction, DTR_future_prediction, RFR_future_prediction, knn_future_prediction, EN_future_prediction, Lasso_future_prediction, Ridge_future_prediction, GBR_future_prediction, VR_future_pred, H_future_pred, L_future_pred, RANSACR_future_pred, SVR_future_pred, TSR_future_pred, HGBR_future_pred, RNR_future_pred, HGBR_future_pred, ET_future_pred, ABR_future_pred, BR_future_pred, SR_future_pred, NN_future_pred]
        biggest_pred = pred_list[0]
        biggest_fut = pred_fut[0]
        biggest_err = 0
        for i in range(len(pred_list)):
            if(sum([1 for i in pred_list[i].tolist() if i<0 ]) <0):
                biggest_err = mean_tweedie_deviance(y_test,pred_list[0])
                temp_err = mean_tweedie_deviance(y_test,pred_list[i])
                temp_pred = pred_list[i]
                temp_fut = pred_fut[i]
                if((temp_err >= biggest_err) & (len(str(round(temp_err))) == 2)):
                    biggest_err = temp_err
                    biggest_pred = temp_pred
                    biggest_fut = temp_fut
        decoded_X_test.insert(0,'predictions',np.rint(biggest_pred).astype(int))
        fut_df.insert(0,'predictions',np.rint(biggest_fut).astype(int))
        return biggest_err, decoded_X_test.reset_index(drop = True), fut_df.reset_index(drop = True)
    
    def mean_gamma_dev(self, df, fut_df, test_size, random_state, depth, num_estimator, num_nonzero_coefs, iter_, num_neighbor, reg_para, epsilon, radius, learning_rate, loss):
        new_df = self.future_enconding(fut_df, df)
        LR_test_prediction, DTR_test_prediction, RFR_test_prediction, knn_test_prediction, EN_test_prediction, Lasso_test_prediction, Ridge_test_prediction, GBR__test_pred, VR_test_pred, H_test_pred, L_test_pred, RANSACR_test_pred, SVR_test_pred, TSR_test_pred, HGBR_test_pred, RNR_test_pred, HGBR_test_pred, ET_test_pred, ABR_test_pred, BR_test_pred, SR_test_pred, NN_test_pred, LR_future_prediction, DTR_future_prediction, RFR_future_prediction, knn_future_prediction, EN_future_prediction, Lasso_future_prediction, Ridge_future_prediction, GBR_future_prediction, VR_future_pred, H_future_pred, L_future_pred, RANSACR_future_pred, SVR_future_pred, TSR_future_pred, HGBR_future_pred, RNR_future_pred, HGBR_future_pred, ET_future_pred, ABR_future_pred, BR_future_pred, SR_future_pred, NN_future_pred = self.regression_models(depth, df, fut_df, test_size, num_estimator, num_nonzero_coefs, random_state, num_neighbor, reg_para, epsilon, radius, learning_rate, loss, iter_)
        X_train, X_test, y_train, y_test, decoded_X_test = self.preprocess(df, test_size, random_state)
        
        pred_list = [LR_test_prediction, DTR_test_prediction, RFR_test_prediction, knn_test_prediction, EN_test_prediction, Lasso_test_prediction, Ridge_test_prediction, GBR__test_pred, VR_test_pred, H_test_pred, L_test_pred, RANSACR_test_pred, SVR_test_pred, TSR_test_pred, HGBR_test_pred, RNR_test_pred, HGBR_test_pred, ET_test_pred, ABR_test_pred, BR_test_pred, SR_test_pred, NN_test_pred]
        pred_fut = [LR_future_prediction, DTR_future_prediction, RFR_future_prediction, knn_future_prediction, EN_future_prediction, Lasso_future_prediction, Ridge_future_prediction, GBR_future_prediction, VR_future_pred, H_future_pred, L_future_pred, RANSACR_future_pred, SVR_future_pred, TSR_future_pred, HGBR_future_pred, RNR_future_pred, HGBR_future_pred, ET_future_pred, ABR_future_pred, BR_future_pred, SR_future_pred, NN_future_pred]
        biggest_pred = pred_list[0]
        biggest_fut = pred_fut[0]
        biggest_err = 0
        for i in range(len(pred_list)):
            if(sum([1 for i in pred_list[i].tolist() if i<0 ]) <0):
                biggest_err = mean_gamma_deviance(y_test,pred_list[0])
                temp_err = mean_gamma_deviance(y_test,pred_list[i])
                temp_pred = pred_list[i]
                temp_fut = pred_fut[i]
                if((temp_err >= biggest_err) & (len(str(round(temp_err))) == 2)):
                    biggest_err = temp_err
                    biggest_pred = temp_pred
                    biggest_fut = temp_fut
        decoded_X_test.insert(0,'predictions',np.rint(biggest_pred).astype(int))
        fut_df.insert(0,'predictions',np.rint(biggest_fut).astype(int))
        return biggest_err, decoded_X_test.reset_index(drop = True), fut_df.reset_index(drop = True)
    
    
    def accuracy(self, input_, df, fut_df, test_size, random_state, depth, num_estimator, num_nonzero_coefs, iter_, num_neighbor, reg_para, epsilon, radius, learning_rate, loss):
        if(input_ == "mean_squared"):
            return self.mean_squared(df, fut_df, test_size, random_state, depth, num_estimator, num_nonzero_coefs, iter_, num_neighbor, reg_para, epsilon, radius, learning_rate, loss)
        elif(input_ == "mean_absolute"):
            return self.mean_absolute(df, fut_df, test_size, random_state, depth, num_estimator, num_nonzero_coefs, iter_, num_neighbor, reg_para, epsilon, radius, learning_rate, loss)
        elif(input_ == "r2"):
            return self.r2(df, fut_df, test_size, random_state, depth, num_estimator, num_nonzero_coefs, iter_, num_neighbor, reg_para, epsilon, radius, learning_rate, loss)
        elif(input_ == "explained_variance"):
            return self.explained_variance(df, fut_df, test_size, random_state, depth, num_estimator, num_nonzero_coefs, iter_, num_neighbor, reg_para, epsilon, radius, learning_rate, loss)
        elif(input_ == "max_error"):
            return self.max_error_(df, fut_df, test_size, random_state, depth, num_estimator, num_nonzero_coefs, iter_, num_neighbor, reg_para, epsilon, radius, learning_rate, loss)
        elif(input_ == "explained_variance"):
            return self.explained_variance(df, fut_df, test_size, random_state, depth, num_estimator, num_nonzero_coefs, iter_, num_neighbor, reg_para, epsilon, radius, learning_rate, loss)
        elif(input_ == "mean_squared_log"):
            return self.mean_squared_log(df, fut_df, test_size, random_state, depth, num_estimator, num_nonzero_coefs, iter_, num_neighbor, reg_para, epsilon, radius, learning_rate, loss)
        elif(input_ == "median_absolute_error"):
            return self.median_abs_error(df, fut_df, test_size, random_state, depth, num_estimator, num_nonzero_coefs, iter_, num_neighbor, reg_para, epsilon, radius, learning_rate, loss)
        elif(input_ == "d2_tweedie_score"):
            return self.d2t_score(df, fut_df, test_size, random_state, depth, num_estimator, num_nonzero_coefs, iter_, num_neighbor, reg_para, epsilon, radius, learning_rate, loss)
        elif(input_ == "d2_pinball_score"):
            return self.d2p_score(df, fut_df, test_size, random_state, depth, num_estimator, num_nonzero_coefs, iter_, num_neighbor, reg_para, epsilon, radius, learning_rate, loss)
        elif(input_ == "d2_absolute_error_score"):
            return self.d2ab_error_score(df, fut_df, test_size, random_state, depth, num_estimator, num_nonzero_coefs, iter_, num_neighbor, reg_para, epsilon, radius, learning_rate, loss)
        elif(input_ == "mean_absolute_percentage_error"):
            return self.mnbs_percentage_error(df, fut_df, test_size, random_state, depth, num_estimator, num_nonzero_coefs, iter_, num_neighbor, reg_para, epsilon, radius, learning_rate, loss)
        elif(input_ == "mean_poisson_deviance"):
            return self.mean_poisson_dev(df, fut_df, test_size, random_state, depth, num_estimator, num_nonzero_coefs, iter_, num_neighbor, reg_para, epsilon, radius, learning_rate, loss)
        elif(input_ == "mean_gamma_deviance"):
            return self.mean_gamma_dev(df, fut_df, test_size, random_state, depth, num_estimator, num_nonzero_coefs, iter_, num_neighbor, reg_para, epsilon, radius, learning_rate, loss)
        elif(input_ == "mean_tweedie_deviance"):
            return self.mean_tweedie_dev(df, fut_df, test_size, random_state, depth, num_estimator, num_nonzero_coefs, iter_, num_neighbor, reg_para, epsilon, radius, learning_rate, loss)
        elif(input_ == "mean_pinball_loss"):
            return self.meanp_loss(df, fut_df, test_size, random_state, depth, num_estimator, num_nonzero_coefs, iter_, num_neighbor, reg_para, epsilon, radius, learning_rate, loss)
        else:
            return "Please insert an error metric!"
