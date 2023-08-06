import warnings
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
warnings.filterwarnings("ignore")


class CreatingDataSet:
    def __init__(self, df, dictionary={}):
        self.df = df
        self.dictionary = dictionary

    def get_subset(self, size=1, random_state=12):
        '''
        :param df: de dataset
        :param size: de grootte van de subset
        :param random state: de seed
        '''    
        df_subset = self.df.sample(n=size, random_state=random_state)
        return df_subset

    def make_df_ML_ready(self, df, X_vars):
        '''
        :param df: de dataset
        :param X_vars: lijst met variabelen
        :param dictionary: een dictionary voor oridnale variabelen
        :return: dataframe met alleen numerieke variabelen
        '''
        ordinal_variables = list(self.dictionary.keys())

        df_ordinal = df[[var for var in X_vars if var in ordinal_variables]]
        df_other = df[[var for var in X_vars if var not in ordinal_variables]]

        df_ordinal_ready = pd.DataFrame()
        df_other_ready = pd.DataFrame()

        for column in df_ordinal:
            df_ordinal_ready[column] = df_ordinal[column].map(self.dictionary[column])

        if not df_other.empty:
            df_other_ready = pd.get_dummies(df_other)

        df_ML_ready = pd.concat([df_ordinal_ready, df_other_ready], axis=1)

        return df_ML_ready

    def append_random_variables(self, df, add_random_int=False, add_random_cont=False, set_seed=2):
        '''
        :param df: de dataset
        :param add_random_int: voeg random integer variabele toe
        :param add_random_cont: voeg random continue variabele toe
        :param set_seed: de seed
        :return: de aangepaste dataset
        '''
        np.random.seed(set_seed)

        if add_random_cont:
            df['random_cont'] = np.random.rand(len(df))
        if add_random_int:
            df['random_int'] = np.random.randint(2,size=len(df))

        return df

    def scale_data(self, df, with_mean=True, with_std=True):
        '''
        :param df: de dataset
        :param with_mean: standaardiseer de data rond het gemiddelde van de trainingsset (anders 0)
        :param with_std: standaardiseer de data met de standaarddeviatie van de trainingsset (anders 1)
        :return: de gestandaardiseerde dataset
        '''
        scaler = StandardScaler(with_mean=with_mean, with_std=with_std)
        df_scaled = pd.DataFrame(scaler.fit_transform(df), index=df.index, columns=df.columns)

        return df_scaled

    def get_train_test(self, y, X_vars, divided_by_max=True, scale_data=True, add_random_int=False,
                       add_random_cont=False, set_seed=2, size=10000, test_size=0.25,
                       random_state=12, with_mean=True, with_std=True):
        '''
        :param divided_by_max: Als je wilt dat de variabelen nog duur hun maximale waarde worden gedeeld (bv handig bij jackpot)
        :param y: te verklaren variabele
        :param X_vars: lijst met variabelen
        :param add_random_int: voeg random integer variabele toe
        :param add_random_cont: voeg random continue variabele toe
        :param set_seed: de seed
        :param size: de grootte van de subset
        :param test_size: verhouding test- en trainingsset
        :param random_state: de seed
        :param scale_data: de data wordt gestandaardizeerd
        :param with_mean: standaardiseer de data rond het gemiddelde van de trainingsset (anders 0)
        :param with_std: standaardiseer de data met de standaarddeviatie van de trainingsset (anders 1)
        :return: test- en trainingsset
        '''
        df_subset = self.get_subset(size, random_state)

        df_ready = self.make_df_ML_ready(df_subset, X_vars)

        df_X = self.append_random_variables(df_ready, add_random_int, add_random_cont, set_seed)
        
        df_y = df_subset[y]

        X_train, X_test, y_train, y_test = train_test_split(df_X, df_y, test_size=test_size, random_state=random_state)

        # for col_ in df_X.columns():
        #     if (df_X[col_] == 0).all():
        #         print('De volgende variabele heeft alleen maar 0-en: ' + col_ + ' dit gaat mis met modelleren ')

        if scale_data:
            X_train_scaled = self.scale_data(X_train, with_mean, with_std)
            X_test_scaled = self.scale_data(X_test, with_mean, with_std)
            return X_train_scaled, X_test_scaled, y_train, y_test
        if divided_by_max:
            return X_train/X_train.max(), X_test/X_test.max(), y_train/y_train.max(), y_test/y_test.max()
        else:
            return X_train, X_test, y_train, y_test


