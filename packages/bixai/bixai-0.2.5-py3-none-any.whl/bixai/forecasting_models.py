import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import statsmodels.formula.api as smf
from sklearn.metrics import r2_score
import plotly.graph_objects as go
import plotly.io as pio
from tqdm import tqdm

pio.renderers.default = "browser"
pd.set_option('display.max_seq_items', None)


class ForecastingModels:
    def __init__(self, df, df_forecast):
        self.df = df
        self.df_forecast = df_forecast

    def test_train(self, te_voorspellen, drawings, test_list):
        df_ols_train = self.df[~self.df[drawings].isin(test_list)]
        df_ols_test = self.df[self.df[drawings].isin(test_list)]

        df_rf = self.df.copy()
        del df_rf[te_voorspellen]
        df_rf_train = df_rf[~df_rf[drawings].isin(test_list)]
        df_rf_test = df_rf[df_rf[drawings].isin(test_list)]
        numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        df_rf_train = df_rf_train.select_dtypes(include=numerics)
        df_rf_test = df_rf_test.select_dtypes(include=numerics)

        return df_ols_train, df_ols_test, df_rf_train, df_rf_test

    def get_X_for_random_forest(self, te_voorspellen):
        df_rf = self.df.copy()
        del df_rf[te_voorspellen]
        numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        df_rf_final = df_rf.select_dtypes(include=numerics)
        return df_rf_final

    def model_residuals_with_rf(self, te_voorspellen, model): # , max_features=5, n_estimators=500
        y = get_residuals(model)
        model_rf = RandomForestRegressor(max_features=5, n_estimators=500) # , n_jobs=-1
        df_rf = self.get_X_for_random_forest(te_voorspellen)
        model_rf.fit(df_rf, y)
        fit_rf_on_residuals = model_rf.predict(df_rf)
        return fit_rf_on_residuals

    def actual_vs_fit_ols_graph(self, var_date, formule, color_kpi='deepskyblue', color_fit='dimgray',
                                title_graph='Actual vs model', residuals=True):

        model = smf.ols(formula=formule, data=self.df)
        if 'np.log(' in model.endog_names:
            y_model = np.exp(model.fit().fittedvalues)
            y_werkelijk = np.exp(model.endog)
        else:
            y_model = model.fit().fittedvalues
            y_werkelijk = model.endog
        fig = go.Figure()

        fig.add_trace(go.Scatter(x=self.df[var_date], y=y_werkelijk, name=model.endog_names,
                                 line_color=color_kpi))

        fig.add_trace(go.Scatter(x=self.df[var_date], y=y_model,
                                 name=model.endog_names + "_fitted",
                                 line_color=color_fit))

        if residuals:
            fig.add_trace(go.Scatter(x=self.df[var_date], y=get_residuals(model),
                                     name="residuals to explain with RF"))

        fig.update_layout(title_text=title_graph,
                          xaxis_rangeslider_visible=True)
        return fig

    def actual_vs_fit_graph_rf(self, te_voorspellen, var_date, formule, color_kpi='deepskyblue',
                               color_fit='dimgray', title_graph='Actual vs model on Residuals with RF'): #, max_features=5, n_estimators=500,

        model = smf.ols(formula=formule, data=self.df)
        y = get_residuals(model)
        fit_rf = self.model_residuals_with_rf(te_voorspellen, model)

        fig = go.Figure()

        fig.add_trace(go.Scatter(x=self.df[var_date], y=y, name='Residuals from ols model',
                                 line_color=color_kpi))

        fig.add_trace(go.Scatter(x=self.df[var_date], y=fit_rf,
                                 name="Random forest fit",
                                 line_color=color_fit))

        fig.update_layout(title_text=title_graph,
                          xaxis_rangeslider_visible=True)
        return fig

    def actual_vs_fit_graph_ols_and_rf(self, te_voorspellen, var_date, formule, max_features=5, n_estimators=500,
                                       color_kpi='deepskyblue', color_fit='dimgray',
                                       title_graph='Actual vs model on Residuals with RF'):

        model = smf.ols(formula=formule, data=self.df)
        if 'np.log(' in model.endog_names:
            y_model = np.exp(model.fit().fittedvalues)
            y_werkelijk = np.exp(model.endog)
        else:
            y_model = model.fit().fittedvalues
            y_werkelijk = model.endog
        fig = go.Figure()

        fig.add_trace(go.Scatter(x=self.df[var_date], y=y_werkelijk, name=model.endog_names,
                                 line_color=color_kpi))

        fig.add_trace(go.Scatter(x=self.df[var_date], y=y_model,
                                 name=model.endog_names + "_fitted",
                                 line_color=color_fit))

        # Random Forest contribution
        fit_rf = self.model_residuals_with_rf(te_voorspellen, model) # , max_features=max_features, n_estimators=n_estimators

        fig.add_trace(go.Bar(x=self.df[var_date], y=fit_rf, name="Contributie Random forest"))

        fig.update_layout(title_text=title_graph,
                          xaxis_rangeslider_visible=True)
        return fig

    def decomposition_graph_ols_rf(self, te_voorspellen, var_date, formule, color_kpi='deepskyblue'):
        '''
        This function has as output a bar plot with all the variables and
        the actual y used

        Input variables

            -model: model
                The model that you want to use
        '''
        model = smf.ols(formula=formule, data=self.df)

        if 'np.log(' in model.endog_names:
            data_decomp = loglin_x_beta_fitted_actual(model)
            y_model = np.exp(model.fit().fittedvalues)
            y_werkelijk = np.exp(model.endog)
        else:
            data_decomp = x_beta_fitted_actual(model)[0]
            y_model = model.fit().fittedvalues
            y_werkelijk = model.endog

        x = self.df[var_date]
        variabelen = data_decomp
        names = list(data_decomp)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y_model, name='y_model'))

        fig.add_trace(go.Scatter(x=x, y=y_werkelijk, name=model.endog_names,
                                 line_color=color_kpi))

        for i in range(0, variabelen.shape[1]):
            fig.add_trace(go.Bar(x=x, y=variabelen[names[i]], name=names[i]))

        fig.update_layout(barmode='relative', title_text='Decompositie', bargap=0)

        fit_rf = self.model_residuals_with_rf(te_voorspellen, model) # , max_features=max_features, n_estimators=n_estimators

        fig.add_trace(go.Bar(x=x, y=fit_rf, name="Contributie Random forest"))

        return fig

    def evaluate_all_drawings(self, formule, te_voorspellen, drawings, out_of_sample=True, n_estimators=500,
                              max_features=10):
        """
        :param formule: formule die het tijdreeks model weergeeft [als formule/text invoeren]
        :param te_voorspellen: de varialeben die je wilt verklaren  [als tekst invoeren]
        :param drawings: de variabelen die voor iedere 'drawing' een unieke waarde heeft (bij stl bijvoorbeeld maand_jaar) [als tekst invoeren]
        :param out_of_sample: Bij True wordt het model geschat op alle data behalve 1 drawing en hier dan een voorspelling overgemaakt met deze weggelaten data
        :param n_estimators: aantal bomen dat in het randomforest model gebruikt wordt
        :param max_features: maximaal aantal futures dat in een boom gebruikt mag worden
        :return: df met alle voorspelling per drawing
        """

        unique_drawings = list(self.df[drawings].unique())
        predictions_ols, predictions_rf, actuals = [], [], []

        if out_of_sample:
            for drawing in tqdm(unique_drawings):
                df_ols_train, df_ols_test, df_rf_train, df_rf_test = self.test_train(te_voorspellen, drawings,
                                                                                     [drawing])
                actual = df_ols_test[te_voorspellen].sum()
                actuals.append(actual)
                model_train_ols = smf.ols(formula=formule, data=df_ols_train)
                predictions_ols.append(get_ols_predictions_sum(model_train_ols, df_ols_test))

                # RandomForest
                y = get_residuals(model_train_ols)
                model_train_rf = RandomForestRegressor(max_features=max_features, n_estimators=n_estimators, n_jobs=-1)
                model_train_rf.fit(df_rf_train, y)
                predictions_rf.append(model_train_rf.predict(df_rf_test).sum())

        afwijking_ols = np.subtract(actuals, predictions_ols)
        predictions_ensemble = np.add(predictions_ols, predictions_rf)
        afwijking_ensemble = np.subtract(actuals, predictions_ensemble)
        predictions_df = pd.DataFrame(
            {'actuals': actuals, 'predictions_ols': predictions_ols, 'actuals_min_predictions_ols': afwijking_ols,
             'verklaring_random_forest': predictions_rf, 'actuals_min_predictions_ensemble': afwijking_ensemble,
             'predictions_ensemble': predictions_ensemble},
            index=unique_drawings)  # index=unique_drawings

        return predictions_df  # actuals, predictions

    def plot_all_drawing_predictions(self, formule, te_voorspellen, drawings, out_of_sample=True, n_estimators=500,
                                     max_features=10):
        """
        :param formule: formule die het tijdreeks model weergeeft [als formule/text invoeren]
        :param te_voorspellen: de varialeben die je wilt verklaren  [als tekst invoeren]
        :param drawings: de variabelen die voor iedere 'drawing' een unieke waarde heeft (bij stl bijvoorbeeld maand_jaar) [als tekst invoeren]
        :param out_of_sample: Bij True wordt het model geschat op alle data behalve 1 drawing en hier dan een voorspelling overgemaakt met deze weggelaten data
        :param n_estimators: aantal bomen dat in het randomforest model gebruikt wordt
        :param max_features: maximaal aantal futures dat in een boom gebruikt mag worden
        :return: Grafiek met iedere drawing en hoe goed het model de te voorspellen variabele kan verklaren.
        """
        df = self.evaluate_all_drawings(formule, te_voorspellen, drawings, out_of_sample, n_estimators, max_features)
        x = df.index
        fig = go.Figure(data=[
            go.Bar(name='Actuals', x=x, y=df.actuals),
            go.Bar(name='Predictions OLS', x=x, y=df.predictions_ols),
            go.Bar(name='Actuals - Predictions OLS', x=x, y=df.actuals_min_predictions_ols),
            go.Bar(name='Verklaring Random Forest', x=x, y=df.verklaring_random_forest),
            go.Bar(name='Actuals - Predictions OLS AND Random Forest', x=x, y=df.actuals_min_predictions_ensemble),
            go.Bar(name='Predictions OLS AND Random Forest', x=x, y=df.predictions_ensemble)

        ])
        return fig

    # OOS:
    def forecast_drawings_ols_randomforest_oos(self, formule, date, te_voorspellen, drawings, test_list,
                                               max_features=6, n_estimators=500,
                                               random_forest_forecast=True):
        """
        :param formule: formule die het tijdreeks model weergeeft [als formule/text invoeren]
        :param date: de variabelen in het dataframe die iets van een date weergeeft voor de grafiek  [als tekst invoeren]
        :param te_voorspellen: de varialeben die je wilt verklaren  [als tekst invoeren]
        :param drawings: de variabelen die voor iedere 'drawing' een unieke waarde heeft (bij stl bijvoorbeeld maand_jaar) [als tekst invoeren]
        :param test_list: de drawings waarop je wilt inzoomen, deze worden out of sample verklaard [als list ingeven]
        :param max_features: maximaal aantal variabelen dat meegnomen wordt in de random forest
        :param n_estimators: aantal bomen dat het random forest model gebruikt (nu op 500)
        :param random_forest_forecast: True als je wilt voorspellen mbv van random forest voor de error termen
        :return: Grafiek over tijd met iedere drawing uit de test list en hoe goed het model de te voorspellen variabele kan verklaren.
        """

        df_ols_train, df_ols_test, df_rf_train, df_rf_test = self.test_train(te_voorspellen, drawings, test_list)

        model_train_ols = smf.ols(formula=formule, data=df_ols_train)
        y_ols_residuals_train = get_residuals(model_train_ols)

        model_train_rf = RandomForestRegressor(max_features=max_features, n_estimators=n_estimators)
        model_train_rf.fit(df_rf_train, y_ols_residuals_train)

        # verklaarde Ytjes:
        predictions_ols = get_ols_predictions(model_train_ols, df_ols_test)
        y_error_explained_rf = model_train_rf.predict(df_rf_test)
        y_ensemble = y_error_explained_rf + predictions_ols

        x = df_ols_test[date]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=df_ols_test[te_voorspellen], name='y_werkelijk'))
        fig.add_trace(go.Scatter(x=x, y=predictions_ols, name='y_estimate_ols'))
        fig.add_trace(go.Scatter(x=x, y=y_ensemble, name='y_ensemble'))
        fig.add_trace(go.Bar(x=x, y=predictions_ols, name='y_ols_estimated_bars'))
        fig.add_trace(go.Bar(x=x, y=y_error_explained_rf, name='y_error_explained_rf_bars'))

        fit_ols = r2_score(df_ols_test[te_voorspellen], predictions_ols)
        fit_ensemble = r2_score(df_ols_test[te_voorspellen], y_ensemble)

        fig.update_layout(barmode='relative',
                          title_text='Fit OLS = ' + str(round(fit_ols, 2)) + ' Fit Ensemble = ' + str(
                              round(fit_ensemble, 2)), bargap=0)

        if random_forest_forecast:
            model_train_rf_y = RandomForestRegressor(max_features=max_features)
            model_train_rf_y.fit(df_rf_train, df_ols_train[te_voorspellen])
            y_explained_rf = model_train_rf_y.predict(df_rf_test)
            fit_rf = r2_score(df_ols_test[te_voorspellen], y_explained_rf)
            fig.add_trace(go.Scatter(x=x, y=y_explained_rf, name='y_explained_rf'))
            fig.update_layout(barmode='relative',
                              title_text='Fit OLS = ' + str(round(fit_ols, 2)) + ' Fit Ensemble = ' + str(
                                  round(fit_ensemble, 2)) + ' Fit RF ' + str(round(fit_rf, 2)), bargap=0)

        return fig.show()

    # OOS:
    def forecast_drawings_ols_randomforest_oos_data(self, formule, date, te_voorspellen, drawings,
                                                    test_list, max_features=6, n_estimators=500):
        """
        :param formule: formule die het tijdreeks model weergeeft [als formule/text invoeren]
        :param date: de variabelen in het dataframe die iets van een date weergeeft voor de grafiek  [als tekst invoeren]
        :param te_voorspellen: de varialeben die je wilt verklaren  [als tekst invoeren]
        :param drawings: de variabelen die voor iedere 'drawing' een unieke waarde heeft (bij stl bijvoorbeeld maand_jaar) [als tekst invoeren]
        :param test_list: de drawings waarop je wilt inzoomen, deze worden out of sample verklaard [als list ingeven]
        :param max_features: maximaal aantal variabelen dat meegnomen wordt in de random forest
        :param n_estimators: aantal bomen dat het random forest model gebruikt (nu op 500)
        :return: dataframe met de forecasts van de test_list
        """

        df_ols_train, df_ols_test, df_rf_train, df_rf_test = self.test_train(te_voorspellen, drawings, test_list)

        model_train_ols = smf.ols(formula=formule, data=df_ols_train)
        y_ols_residuals_train = get_residuals(model_train_ols)

        model_train_rf = RandomForestRegressor(max_features=max_features, n_estimators=n_estimators)
        model_train_rf.fit(df_rf_train, y_ols_residuals_train)

        # verklaarde Ytjes:
        predictions_ols = get_ols_predictions(model_train_ols, df_ols_test)
        y_error_explained_rf = model_train_rf.predict(df_rf_test)
        y_ensemble = y_error_explained_rf + predictions_ols

        data_oos = pd.DataFrame()
        data_oos['date'] = df_ols_test[date]
        data_oos['y_werkelijk'] = df_ols_test[te_voorspellen]
        data_oos['y_ensemble'] = y_ensemble
        data_oos['predictions_ols'] = predictions_ols
        data_oos['y_error_explained_rf'] = y_error_explained_rf

        return data_oos

        # Forecasting:
    def forecast(self, formule, date, te_voorspellen, show_graph=True, get_data=False, random_forest_forecast=True, max_features=6, n_estimators=500):
        """
        :param formule: formule die het tijdreeks model weergeeft [als formule/text invoeren]
        :param date: de variabelen in het dataframe die iets van een date weergeeft voor de grafiek  [als tekst invoeren]
        :param show_graph: Als je de grafiek met voorspellingen wilt
        :param get_data: als je een dataframe wilt met de voorspellingen
        :param max_features: maximaal aantal variabelen dat meegnomen wordt in de random forest
        :param n_estimators: aantal bomen dat het random forest model gebruikt (nu op 500)
        :param random_forest_forecast: True als je wilt voorspellen mbv van random forest voor de error termen
        :return: Grafiek over tijd met iedere drawing uit de test list en hoe goed het model de te voorspellen variabele kan verklaren.
        """
        # clean df for rf models
        numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        df_forecasting_rf = self.df_forecast.select_dtypes(include=numerics).dropna(axis=1)
        df_rf = self.df.select_dtypes(include=numerics).drop(te_voorspellen, axis=1)

        # Modellen trainen op data uit het verleden
        model_train_ols = smf.ols(formula=formule, data=self.df)
        if random_forest_forecast:
            y_ols_residuals_train = get_residuals(model_train_ols)
            model_train_rf = RandomForestRegressor(max_features=max_features, n_estimators=n_estimators)
            model_train_rf.fit(df_rf, y_ols_residuals_train)

        # Forecast maken
        predictions_ols = get_ols_predictions(model_train_ols, self.df_forecast)
        if random_forest_forecast:
            y_error_explained_rf = model_train_rf.predict(df_forecasting_rf)
            y_ensemble = y_error_explained_rf + predictions_ols

        if show_graph:
            x = self.df_forecast[date]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x, y=predictions_ols, name='y_estimate_ols'))
            fig.add_trace(go.Bar(x=x, y=predictions_ols, name='y_ols_estimated_bars'))

            if random_forest_forecast:
                fig.add_trace(go.Scatter(x=x, y=y_ensemble, name='y_ensemble'))
                fig.add_trace(go.Bar(x=x, y=y_error_explained_rf, name='y_error_explained_rf_bars'))

            fig.update_layout(barmode='relative',
                              title_text='Forecast',  yaxis_title=te_voorspellen, bargap=0)

            return fig.show()

        if get_data:
            forecast_data = pd.DataFrame()
            forecast_data['date'] = self.df_forecast[date]
            forecast_data['predictions_ols'] = predictions_ols
            if random_forest_forecast:
                forecast_data['part_explained_with_rf'] = y_error_explained_rf
                forecast_data['forecast_ols_and_rf'] = y_ensemble
            return forecast_data


def check_variables_to_add(model, df):
    '''
    A function that uses all variables in de data used to model (incl. decays if added by media),
    to see what the effect is of adding one variable to the current chosen model.

    input:
        -a model

    returns:
        -AdjR2 change: the adjusted R2 from the model - the adjusted R2 from the model with the variable added.
            Keep in mind that this can be negative if the new variable doesn't add enough to the explained variance
            If you find variables that have a high number, they might be worth adding to the model

        -DW change: the DW from the model - the DW from the model with the variable added.
            Keep in mind that we want this variable to be as close as possible to 2.
            However, we expect it usually when it is between 1.6 and 2.4

        -'JB change': the JB from the model - the JB from the model with the variable added.
            Keep in mind that we want this variable (p_value) to be as big as possible (or usually bigger than 0.05).
            It is a H0 test to see if the error terms are not normally distributed

    '''

    # only use the variables that are not yet in the model and have no na's
    used = list(model.exog_names)
    used.append(list(model.endog_names))
    all_variables = list(df.dropna(axis=1, how='all')._get_numeric_data().columns)

    var_to_test = [x for x in all_variables if x not in used]

    df_results = pd.DataFrame(columns=['AdjR2 change', 'DW change', 'JB change'], index=var_to_test)

    old_model = model_characteristics(model)
    old_model_adjr2 = old_model['AdjR2']
    old_model_dw = old_model['DW']
    old_model_jb = old_model['JB']

    formule = model.formula
    # new model
    for var in var_to_test:
        new_formule = formule + ' +' + var
        try:
            new_model_results = smf.ols(formula=new_formule, data=df)

            new_model = model_characteristics(new_model_results)
            new_model_adjr2 = new_model['AdjR2']
            new_model_dw = new_model['DW']
            new_model_jb = new_model['JB']
            results = [new_model_adjr2 - old_model_adjr2, new_model_dw - old_model_dw, new_model_jb - old_model_jb]
            df_results.loc[var, :] = results
        except:
            print('Something goes wrong with variable: ', var)

    return df_results.sort_values(by=['AdjR2 change'], ascending=False)


def get_ols_predictions_sum(model, df_test):
    results = model.fit()
    if 'np.log(' in model.endog_names:
        prediction = np.exp(results.predict(df_test, transform=True)).sum()
    else:
        prediction = results.predict(df_test, transform=True).sum()
    return prediction


def get_ols_predictions(model, df_test):
    results = model.fit()
    if 'np.log(' in model.endog_names:
        prediction = np.exp(results.predict(df_test, transform=True))
    else:
        prediction = results.predict(df_test, transform=True)
    return prediction


def get_residuals(model):
    if 'np.log(' in model.endog_names:
        y_model = np.exp(model.fit().fittedvalues)
        y_werkelijk = np.exp(model.endog)
        residuals = y_werkelijk - y_model
    else:
        residuals = model.fit().resid
    return residuals


def model_characteristics(model):
    '''functie de DW, JB teruggeeft
    Input: een res.summary() van een ols model
    Output: AdjR2, DW, JB  '''
    results = model.fit()
    AdjR2 = round(results.rsquared_adj, 3)
    results_summary = results.summary()
    results_as_html2 = results_summary.tables[2].as_html()
    dwjb = pd.read_html(results_as_html2, index_col=0)[0]
    DW = round(dwjb.iloc[0, 2], 3)
    JB = round(dwjb.iloc[2, 2], 3)
    return {'AdjR2': AdjR2, 'DW': DW, 'JB': JB}


def x_beta_fitted_actual(model):
    '''
    Functie die vanuit een log lin model een decompostie geeft
    Input:
        -Model
        -Dataframe met de variabelen in het model
    '''

    beta = model.fit().params
    X = pd.DataFrame(model.exog, columns=beta.index)
    x_beta = X * 0
    model_fit = model.fit()
    for i in range(len(X)):
        for j in range(len(model_fit.params)):
            x_beta.iloc[i, j] = model.exog[i, j] * model_fit.params[j]
            # negatieve waardes van intercept halen
    sum_negatives = []
    for i in range(x_beta.shape[0]):
        negative_value = 0
        for j in range(x_beta.shape[1]):
            if x_beta.iloc[i, j] < 0:
                negative_value += x_beta.iloc[i, j]
        sum_negatives.append(negative_value)
    sum_negatives_pd = pd.DataFrame(sum_negatives)
    x_beta_intercept_correctie = x_beta.copy()
    if 'Intercept' in model_fit.params.index:
        x_beta_intercept_correctie.Intercept = x_beta_intercept_correctie.Intercept + sum_negatives_pd[0]

    return x_beta, x_beta_intercept_correctie


def loglin_x_beta_fitted_actual(model):
    ''''
    Functie die vanuit een log lin model een decompostie geeft
    Input:
        -Model
        -Dataframe met de variabelen in het model

    Het idee:
    log(y)  = c + a1*x1 + a2*x2 + ...
    hence: y = exp(c) * exp(a1*x1) * exp(a2*x2)*...

    first_contribution = [exp(c), exp(a1*x2), exp(a2*x2), ...]
    total_contribution = exp(c)*exp(a1*x2)*exp(a2*x2)...
    individual_contribution = [total_contribution - total_contribution/first_contribution[0], total_contribution - total_contribution/first_contribution[1],...]
    actual_contribibution = [individual_contribution[0] + abs(individual_contribution[0]) * (y_estimated - sum(individual_contribution) / (abs(individual_contribution[0]) + abs(individual_contribution[1]+ ...) , ...]
    '''
    # get the first_contribution
    res = model.fit()

    X = pd.DataFrame(model.exog, columns=model.exog_names)
    X_beta = X * res.params
    first_contribution = np.exp(X_beta)
    total_contribution = first_contribution.prod(axis=1)

    # get the individual_contribution
    individual_contribution = pd.DataFrame(columns=model.exog_names)
    for x_var in model.exog_names:
        individual_contribution[x_var] = total_contribution - total_contribution / first_contribution[x_var]

    # actual_contribibution
    actual_contribibution = pd.DataFrame(columns=model.exog_names)
    for x_var in model.exog_names:
        actual_contribibution[x_var] = individual_contribution[x_var] + abs(individual_contribution[x_var]) * (
                total_contribution - individual_contribution.sum(axis=1)) / abs(individual_contribution).sum(
            axis=1)

    return actual_contribibution

