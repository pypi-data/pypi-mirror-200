import warnings
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import xgboost
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from itertools import chain
from tqdm import tqdm
import plotly.figure_factory as ff
from sklearn.linear_model import LogisticRegression
import joblib

warnings.filterwarnings("ignore")


class Models:
    def __init__(self, X_train, y_train):
        self.y_train = y_train
        self.X_train = X_train

    def random_forest_classifier(self, n_estimators=100, max_features="sqrt", verbose=False, n_jobs=None):
        if self.y_train.dtype == 'int64':
            rf = RandomForestClassifier(n_estimators=n_estimators, max_features=max_features,
                                        verbose=verbose, n_jobs=n_jobs)
            rf_classifier_model = rf.fit(self.X_train, self.y_train)
            return rf_classifier_model
        else:
            print('Seems like the y_train variable is no integer, use another model or change the y_train variable')

    def xgboost_classifier(self, n_estimators=100, verbose=False, eval_metric="logloss", max_depth=2, n_jobs=None):
        if self.y_train.dtype == 'int64':
            model = xgboost.XGBClassifier(n_estimators=n_estimators, max_depth=max_depth, verbose=verbose)
            xgboost_classifier_model = model.fit(self.X_train, self.y_train * 1, eval_metric=eval_metric)
            return xgboost_classifier_model
        else:
            print('Seems like the y_train variable is no integer, use another model or change the y_train variable')

    def multivariate_logistic_regression(self):
        model = LogisticRegression(multi_class='multinomial', solver='lbfgs')
        model_mvl = model.fit(self.X_train, self.y_train)
        return model_mvl

    def logistic_regression(self):
        model = LogisticRegression()
        model_logistic = model.fit(self.X_train, self.y_train)
        return model_logistic


class EvaluateModels:
    def __init__(self, X_train, X_test, y_train, y_test):
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test

    def accuracy_models(self, models):
        accuracy_results = []
        model_name = []

        for model in models:
            y_pred = model.predict(self.X_test)
            accuracy = accuracy_score(self.y_test, y_pred)
            accuracy_results.append(accuracy)
            model_name.append(str(model))

        results = {'Modellen': model_name, 'Accuracy': accuracy_results}

        return pd.DataFrame(results)

    def find_optimal_alpha(self, alphas=list(10 ** i for i in range(-10, 10, 1)), plot=True, return_values=True):
        df_lasso = pd.DataFrame()
        var_names = self.X_train.columns
        df_coeffs = pd.DataFrame(columns=var_names)

        fig = make_subplots(rows=1, cols=2, subplot_titles=('Accuracy', 'Coefficients'))

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(self.X_train)

        for i in alphas:
            lasso = LogisticRegression(penalty='l1', C=(1 / i), solver='saga')
            lasso.fit(X_train_scaled, self.y_train)
            accuracy = lasso.score(self.X_test, self.y_test)
            df_lasso.at[i, 'aantal_variabelen'] = np.count_nonzero(lasso.coef_)
            df_lasso.at[i, 'accuracy'] = accuracy
            df_coeffs.loc[i, :] = lasso.coef_
            print(i)

        if plot:
            # fig.add_trace(go.Scatter(x=df_lasso.index, y=df_lasso['aantal_variabelen'], mode='lines'), row=1, col=1)
            fig.add_trace(go.Scatter(x=df_lasso.index, y=df_lasso['accuracy'], mode='lines', name='accuracy'), row=1,
                          col=1)
            for var in var_names:
                fig.add_trace(go.Scatter(x=df_coeffs.index, y=df_coeffs[var], mode='lines', name=var), row=1, col=2)
            fig.update_layout(xaxis_type='log', xaxis2_type='log', yaxis_range=[0, 1])
            fig.show()

        if return_values:
            return df_coeffs

    def visualize_probabilities(self, model, queries=[], rename_queries=[], bin_size=0.01,
                                title='Verdeling van kansen ', xaxis='Kans',
                                yaxis='Aantallen bij gegeven kans'):
        if len(queries) == 0:
            model_kansen = model.predict_proba(self.X_train)
            model_kansen_list = [item[1] for item in model_kansen]
            # Group data together
            hist_data = [model_kansen_list]
            group_labels = ['Kans per speler']
            # Create distplot with custom bin_size
            fig = ff.create_distplot(hist_data, group_labels, bin_size=bin_size)
            fig.update_layout(title=title, xaxis_title=xaxis, yaxis_title=yaxis)
            fig.show()
        else:
            hist_data = []
            for query in queries:
                model_kansen = model.predict_proba(self.X_train.query(query))
                model_kansen_list = [item[1] for item in model_kansen]
                hist_data.append(model_kansen_list)
                # Create distplot with custom bin_size
            if len(rename_queries) > 0:
                groups = rename_queries
            else:
                groups = queries
            fig = ff.create_distplot(hist_data, groups, bin_size=bin_size)
            fig.update_layout(title=title, xaxis_title=xaxis, yaxis_title=yaxis)
            fig.show()

    def determine_drivers_binary_model(self, model, y=[], plot=True, get_data=False, scaling_to_mean_odds_model=True,
                                       scaling_to_actual_odds=False, title='Impact variabelen ',
                                       yaxis='Absolute impact op de kans'):
        model_kans = model.predict_proba(self.X_train)
        model_kans_list = [item[1] for item in model_kans]
        gemiddelde_kans = np.mean(model_kans_list)
        impact_vars = {}
        vars_ = self.X_train.columns

        for var in vars_:
            X_model = self.X_train.copy()
            X_model[var] = 0
            model_kans_var = model.predict_proba(X_model)
            model_kans_list_var = [item[1] for item in model_kans_var]
            gemiddelde_kans_var = np.mean(model_kans_list_var)
            impact_var = gemiddelde_kans - gemiddelde_kans_var
            impact_vars[var] = impact_var

        kans_intercept = model.predict_proba(self.X_train * 0)
        impact_vars['intercept'] = kans_intercept[0][1]

        if scaling_to_mean_odds_model:
            scalar = gemiddelde_kans / sum(impact_vars.values())
            print(scalar)
            for key in impact_vars:
                impact_vars[key] = impact_vars[key] * scalar
        if not scaling_to_mean_odds_model:
            if scaling_to_actual_odds:
                scalar = np.mean(y) / sum(impact_vars.values())
                print(scalar)
                for key in impact_vars:
                    impact_vars[key] = impact_vars[key] * scalar
        if get_data:
            return impact_vars
        if plot:
            fig = go.Figure()
            fig.add_trace(go.Bar(x=list(impact_vars.keys()), y=list(impact_vars.values()), name='Impact op de kans'))
            fig.update_layout(barmode='relative', title_text=title, yaxis_title=yaxis, bargap=0)
            fig.show()

    # Impact variables multivariate logistic regression
    def visualize_probabilities_mvlogit(self, model, selection='', bin_size=0.01,
                                        title='Verdeling van kansen van de selectie ', xaxis='Kans',
                                        yaxis='Aantallen bij gegeven kans'):

        if len(selection) > 0:
            list_merken, list_kansen = get_df_ordered_for_figure_factory(model,
                                                                         get_df_selection(self.X_train, selection))
        else:
            list_merken, list_kansen = get_df_ordered_for_figure_factory(model, self.X_train)

        fig = ff.create_distplot(list_kansen, list_merken, bin_size=bin_size)
        fig.update_layout(title=title + selection, xaxis_title=xaxis, yaxis_title=yaxis)

        # title = "Plot Title",
        # xaxis_title = "X Axis Title",
        # yaxis_title = "Y Axis Title"
        return fig

    # NAAM MVLogit worden..
    def determine_drivers_mvlogit(self, model, X_vars_to_show=[], merken_x_as=True,
                                  title='Impact variabelen op de kans', yaxis='absolute toename in kans'):
        results_dict = determine_impact(model, self.X_train, X_vars_to_show)
        fig = go.Figure()
        if merken_x_as:
            for vars_ in results_dict.keys():
                fig.add_trace(go.Bar(name=vars_, x=results_dict[vars_].index, y=results_dict[vars_].values))
        else:
            df_results = pd.DataFrame()
            for vars_ in results_dict.keys():
                df_results[vars_] = results_dict[vars_].values
                df_results.index = results_dict[vars_].index
            for merk_ in df_results.index:
                fig.add_trace(go.Bar(name=merk_, x=df_results.loc[merk_].index, y=df_results.loc[merk_].values))
        fig.update_layout(barmode='group', title=title, yaxis_title=yaxis)
        return fig


def save_model(model, filename, opmerking=['geen opmerking'], gemaakt_door=['helaas, geen naam opgegeven'], data_used=[],
               N_rows_data=10, save_estimates=True):
    # Save the model
    joblib.dump(model, filename + '.joblib')

    # Text file met opmerkingen
    with open(filename + '_opmerkingen.txt', 'w+') as fh:
        fh.write('Opmerking: ')
        fh.write(opmerking)
        fh.write('\n')
        fh.write('Made by: ')
        fh.write(gemaakt_door)

    # Data die gebruikt is bij het model opslaan als sample size N_rows_data
    if len(data_used) > 0:
        data_used.head(N_rows_data).to_csv(filename + '_data_used_sample.csv', sep='\t', encoding='utf-8')

    # Schattingen opslaan
    if len(data_used) > 0:
        if save_estimates:
            try:
                index = data_used.columns
                model_coef = model.coef_
                # als model met meer dan 2 uitkomsten is (mvl)
                if len(model.classes_) > 2:
                    df_estimates = pd.DataFrame(index=index, columns=model.classes_)
                    for i in range(0, len(model.classes_)):
                        df_estimates.iloc[:, i] = model_coef[i]
                else:
                    df_estimates = pd.DataFrame(index=index)
                    df_estimates['estimates'] = model_coef[0]
                df_estimates.loc['intercept'] = model.intercept_[0]
                df_estimates.to_csv(filename + '_estimates.csv', sep='\t', encoding='utf-8')
            except:
                print("___")
                print("You can't save the estimates from this type of model")
                print("___")

    print('The actual model is saved as: ' + filename + '.joblib')
    print('The remarks of the model are saved as: ' + filename + '_opmerkingen')
    print('The first N rows (' + str(
        N_rows_data) + ') of the data model is saved as: ' + filename + '_data_used_sample.csv')
    if save_estimates:
        print('The estimates are saved as: ' + filename + '_estimates.csv')


def feature_importance(models, return_values=True, plot=True):
    feature_importances_dict = {}
    fig = go.Figure()

    for model in models:
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1]
        var_names = model.feature_names_in_[indices]
        feature_importances_df = pd.DataFrame()
        feature_importances_df['var_names'] = var_names
        feature_importances_df['feature_importance'] = importances[indices]
        feature_importances_dict[str(model)[0:13]] = feature_importances_df

    if plot:
        fig.add_trace(go.Bar(x=model.feature_names_in_, y=model.feature_importances_, name=str(model)[0:13]))

    if plot:
        fig.show()

    if return_values:
        return feature_importances_dict


def get_df_long_mvlogistic(model, X):
    n = len(X)
    x = list(model.classes_) * n
    y_probs = model.predict_proba(X)
    y_probs_list = list(chain.from_iterable(y_probs))

    return x, y_probs_list


def get_df_ordered_for_figure_factory(model, X):
    x, y = get_df_long_mvlogistic(model, X)

    results = pd.DataFrame()
    results['Merken'] = x
    results['Kans_op_tweede_merk'] = y

    list_merken = []
    list_kansen = []
    for merk in results['Merken'].unique():
        list_merken.append(merk)
        list_kansen.append(np.array(results[results['Merken'] == merk]['Kans_op_tweede_merk']))
    return list_merken, list_kansen


def get_df_selection(df, selection):
    return df.query(selection)


def determine_impact(model, X, X_vars_to_show=[]):
    x, y = get_df_long_mvlogistic(model, X)
    model_results = pd.DataFrame()
    model_results['merk'] = x
    model_results['kans'] = y
    model_results.groupby(['merk'])['kans'].mean()

    impact_vars = {}
    if len(X_vars_to_show) > 0:
        vars_ = X_vars_to_show
    else:
        vars_ = X.columns

    for var in tqdm(vars_):
        X_model = X.copy()
        X_model[var] = 0
        x, y = get_df_long_mvlogistic(model, X_model)
        model_results_var = pd.DataFrame()
        model_results_var['merk'] = x
        model_results_var['kans'] = y
        model_results_var.groupby(['merk'])['kans'].mean()
        impact_var = model_results.groupby(['merk'])['kans'].mean() - model_results_var.groupby(['merk'])[
            'kans'].mean()
        impact_vars[var] = impact_var
    return impact_vars
