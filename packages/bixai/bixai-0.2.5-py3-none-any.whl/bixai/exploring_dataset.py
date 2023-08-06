import warnings
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
warnings.filterwarnings("ignore")


class ExploringDataSet:

    def __init__(self, df, dictionary=None):
        self.df = df
        self.dictionary = dictionary

    def get_null_values(self):
        '''
        :return: lijst met alle variabelen waarvan tenminste een record leeg of null is
        '''
        df_null = pd.concat([self.df.isnull().sum(),self.df.eq('').sum()],keys=['Nulls','Empty'],axis=1)
        df_error = df_null[(df_null['Nulls'] > 0) | (df_null['Empty'] > 0)]

        return df_error

    def correlation_matrix(self, vars):
        '''
        :param vars: lijst met variabelen
        :return: de correlatiematrix
        '''
        fig = go.Figure()

        # Make variables numeric
        df_ordinal_ready = pd.DataFrame()

        ordinal_variables = list(self.dictionary.keys())

        df_ordinal = self.df[[var for var in vars if var in ordinal_variables]]
        df_other = self.df[[var for var in vars if var not in ordinal_variables]]

        for column in df_ordinal:
            df_ordinal_ready[column] = df_ordinal[column].map(self.dictionary[column])

        df_other_ready = df_other.select_dtypes(exclude=['category'])

        df_corr_ready = pd.concat([df_ordinal_ready,df_other_ready], axis=1) 

        # Compute the correlation matrix
        df_corr = df_corr_ready[vars].corr()

        # Generate a mask for the upper triangle
        mask = np.triu(np.ones_like(df_corr, dtype=bool))

        # Plot the figure
        fig.add_trace(go.Heatmap(z=df_corr.mask(mask), x=df_corr.columns, y=df_corr.columns, colorscale='Rdbu', zmin=-1, zmax=1))
        fig.update_layout(title='Correlation matrix', plot_bgcolor='rgba(0,0,0,0)')

        fig.show()

    def explore_variable(self, xvar, y, nrbins=20, order=[]):
        '''
        :param xvar: lijst met variabelen
        :param y: de doelvariabele
        :param nrbins: het aantal groepen
        :order: een lijst met de volgorde van de groepen
        :return: figuren waarin de doelvariabele wordt uitgezet tegen de variabelen
        '''
        fig = go.Figure()
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        length = len(self.df[xvar].unique())
        df_order = pd.DataFrame()

        # Make variable numeric
        if xvar in list(self.dictionary.keys()):
            sorted_dictionary= sorted(self.dictionary[xvar].items(), key=lambda x: x[1])
            order = [i[0] for i in sorted_dictionary]

        # Assign variable to bins and calcualte statistics on (binned) variable
        if (length > nrbins) and (self.df[xvar].dtype != 'categorical'):
            df_cut = self.df.copy()
            boundaries = pd.cut(self.df[xvar], nrbins, precision=10, duplicates='drop')
            df_cut[xvar] = boundaries
            df_cut[xvar] = [a.left for a in boundaries]
            df_group = df_cut.groupby(xvar)[y].agg(['count','mean']).reset_index()
        else:
            df_group = self.df.groupby(xvar)[y].agg(['count','mean']).reset_index()
    
        # Order df to draw line plot in right order
        if len(order) > 0:
            df_list = []
            for i in order:
                df_list.append(df_group[df_group[xvar]==i])
            df_order = pd.concat(df_list)
        else:
            df_order = df_group

        # Draw plots
        fig.add_trace(go.Bar(x=df_order[xvar], y=df_order['count'], name='aantal spelers', opacity=0.2, marker_color='grey'),secondary_y=False)
        fig.add_trace(go.Scatter(x=df_order[xvar], y=df_order['mean'], mode='lines', name=y, line=dict(color='orange', width=2)),secondary_y=True)

        fig.update_layout(title=str(xvar), plot_bgcolor='rgba(0,0,0,0)', yaxis2=dict(tickformat='.0%'))
        fig.update_yaxes(title_text='aantal spelers', secondary_y=False, showline=False)
        fig.update_yaxes(title_text=y, secondary_y=True, showline=False)

        fig.show()
