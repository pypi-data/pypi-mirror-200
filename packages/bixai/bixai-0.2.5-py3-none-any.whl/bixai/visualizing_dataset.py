import warnings
import numpy as np
import pandas as pd
import json 
warnings.filterwarnings("ignore")


class VisualizingDataSet:
    def __init__(self, df):
        self.df = df

    def group_dataset(self, xvars, y):
        '''
        :param xvars: de lijst met variabelen waarover moet worden gegroepeerd
        :param y: de doelvariabele
        :return: de gegroepeerde dataset
        '''
        df_group = self.df.groupby(xvars)[y].agg(['count','mean'])

        return df_group

    def make_list(self, xvars, y):

        df_set = pd.DataFrame(columns=xvars)

        #for i in range(len(xvars)):
        #    df_group = self.group_dataset(xvars[:i+1], y).reset_index()
        #    df_set = pd.concat([df_set,df_group])
        #df_set.set_index(xvars)

        #print(df_set.head(5))

        df_set = self.group_dataset(xvars, y)

        result = {}
        nested_dict = {}

        for index, count, mean in df_set.itertuples():
            for i, key in enumerate(index):
                if i == 0:
                    if not key in result:
                        result[key] = {}
                    nested_dict = result[key]
                elif i == len(index)-1:
                    nested_dict[key] = count
                else:
                    if not key in nested_dict:
                        nested_dict[key] = {}
                    nested_dict = nested_dict[key]

        print(json.dumps(result, indent=4))