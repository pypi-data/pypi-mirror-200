import numpy as np
from itertools import product
import pandas as pd
import statsmodels.formula.api as smf
from tqdm import tqdm
import plotly.graph_objects as go
from statsmodels.stats.outliers_influence import variance_inflation_factor
import plotly.graph_objs as go


def decay(var, labda_):
    decayVariable = []
    decayVariable.append(var.values[0])
    for i in range(1, len(var)):
        decayVariable.append(var.values[i] + labda_ * decayVariable[i - 1])
    return pd.Series(data=decayVariable, dtype=float)


def s_curve(var, alpha_):
    s_curve_values = alpha_ * (var / max(var)) * (1 - np.exp(-alpha_ * (var / max(var)))) / (
            1 + alpha_ * (var / max(var)))
    return s_curve_values


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


# def x_beta_fitted_actual(model):
#     beta = model.fit().params
#     X = pd.DataFrame(model.exog, columns=beta.index)
#     x_beta = X * 0
#     model_fit = model.fit()
#     for i in range(len(X)):
#         for j in range(len(model_fit.params)):
#             x_beta.iloc[i, j] = model.exog[i, j] * model_fit.params[j]
#
#     x_beta_intercept_correctie = []
#     if 'Intercept' in model.fit().params.index:   # negatieve waardes van intercept halen
#         sum_negatives = []
#         for i in range(x_beta.shape[0]):
#             negative_value = 0
#             for j in range(x_beta.shape[1]):
#                 if x_beta.iloc[i, j] < 0:
#                     negative_value += x_beta.iloc[i, j]
#             sum_negatives.append(negative_value)
#         sum_negatives_pd = pd.DataFrame(sum_negatives)
#         x_beta_intercept_correctie = x_beta.copy()
#         if 'Intercept' in model_fit.params.index:
#             x_beta_intercept_correctie.Intercept = x_beta_intercept_correctie.Intercept + sum_negatives_pd
#         return x_beta, x_beta_intercept_correctie


def extract_media_impact(model, media_vars):
    if 'np.log(' in model.endog_names:
        decomp = loglin_x_beta_fitted_actual(model)
    else:
        if 'Intercept' in model.fit().params.index:
            decomp = x_beta_fitted_actual(model)[1]
        else:
            decomp = x_beta_fitted_actual(model)[0]

    media_contributie = pd.DataFrame(index=decomp.index)
    for media_var in media_vars:
        media_contributie[media_var] = decomp.filter(like=media_var, axis=1)

    y_media = media_contributie.sum(axis=1)

    model_fit = model.fit()
    residu = model_fit.resid
    y_media_reside = y_media + residu
    y_media_reside[y_media_reside < 0] = 0 #geen negatieve waardes door media verklaren
    return y_media, y_media_reside, media_contributie


def variables_decay_rc_names(media):  # per media var een list
    '''creates a list with all the variables with their functional form in variables_name_decay
     -Input a dictionary with the media information that gets tested'''
    variables_name_decay = {}
    media_variables = list(media.keys())
    decays = []
    curves = []
    for media_var in media_variables:
        curves2 = []
        type_curve = media[media_var]['curve']
        for decay_value in media[media_var]['decay']:
            dec_var = 'decay(' +  media_var + ',' + str(decay_value) + ')'
            decays.append(dec_var)
            for alpha_ in media[media_var]['alpha']:
                curves_var = str(type_curve) + '(' + dec_var + ',' + str(alpha_) + ')'
                curves.append(curves_var)
                curves2.append(curves_var)
        variables_name_decay[media_var] = curves2
    return decays, curves, variables_name_decay


def create_media_formulas(media, log_lin=False, y_name='y_media'):
    or_variables_media = variables_decay_rc_names(media)[2]
    or_variables_list = pd.DataFrame([row for row in product(*or_variables_media.values())],
                                     columns=or_variables_media.keys())
    formules = []
    for z in range(len(or_variables_list)):
        of_var = list(or_variables_list.loc[z,])
        if log_lin:
            f = 'np.log(' + y_name + ') ~ -1 + '
        else:
            f = y_name + ' ~ -1 + '
        if len(of_var) > 0:
            f += " + ".join(of_var)
        formules.append(f)
    return formules

def decompositie_sum(model):
    '''
    for a given model, it returns the % contribution of a variable
    '''
    res = model.fit()
    if 'np.log(' in model.endog_names:
        X_beta = loglin_x_beta_fitted_actual(model)
        decomp_totaal = X_beta.sum() / np.exp(res.fittedvalues).sum()
    else:
        X = pd.DataFrame(model.exog, columns=model.exog_names)
        X_beta = X * res.params
        decomp_totaal = X_beta.sum() / res.fittedvalues.sum()
    return decomp_totaal

def roi_media_model(model, media_zelf, y_media,df):
    '''
    determines the roi for each variable you want to see
    '''
    decomp = decompositie_sum(model)
    media_roi = {}
    for media_var in list(media_zelf.keys()):
        try:
            contribution = decomp.filter(like=media_var, axis=0)[0]
            cost = media_zelf[media_var]['cost'][0]
            roi = (df[y_media].sum() * contribution) / cost
            media_roi[media_var] = roi
        except:
            media_roi[media_var] = ""
    return media_roi
# roi_media_model(model, media, 'y_media',df)

def roi_model(model, media, df, y):
    '''
    determines the roi for each variable you want to see
    '''
    decomp = decompositie_sum(model)
    media_roi = {}
    for media_var in list(media.keys()):
        try:
            contribution = decomp.filter(like=media_var, axis=0)[0]
            cost = media[media_var]['cost'][0]
            roi = (df[y].sum() * contribution) / cost
            media_roi[media_var] = roi
        except:
            media_roi[media_var] = ""
    return media_roi


def estimates(model):
    res = model.fit()
    return res.params, res.pvalues


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


def run_media_models(media, df, media_vars, orginal_model, log_lin = False, y_name = 'y_media'):
    '''
    This function
    '''

    rejected_model_statistics = []
    rejected_sign_betas = []  # Deze kijken we pas naar als de statistics voldoen
    # List met uitkomsten voor het model
    model_statistics = []
    formules_used = []
    estimates_model = []
    decomposition = []
    roi_models = []

    #Y var om te verklaren
    df[y_name] = extract_media_impact(orginal_model, media_vars)[2]
    #Formules om te testen:
    formules = create_media_formulas(media, log_lin, y_name=y_name)

    for i in tqdm(range(len(formules))):
        model = smf.ols(formula=formules[i], data=df)
        # Restriction alle beta's positief:
        if estimates(model)[0].min() >= 0:
                # Model not rejected:
                # Formula used appending
                formules_used.append(formules[i])
                # Model statistics appending
                model_statistics.append(model_characteristics(model))
                # Model estimates appending
                estimates_model.append(estimates(model))
                # Decomposition appending
                decomposition.append(decompositie_sum(model))
                #ROI
                roi_models.append(roi_media_model(model, media, 'y_media', df))

    betas = []
    p_values = []
    for i in range(len(estimates_model)):
        betas.append(estimates_model[i][0])
        p_values.append(estimates_model[i][1])

    betas_df = pd.DataFrame(betas)
    p_values_df = pd.DataFrame(p_values)
    roi_df = pd.DataFrame(roi_models)

    model_statistics_df = pd.DataFrame(model_statistics).join(pd.DataFrame(formules_used))
    formules_used_df = pd.DataFrame(formules_used)
    decomposition_df = pd.DataFrame(decomposition)

    return betas_df, p_values_df, model_statistics_df, formules_used_df, decomposition_df, roi_df


def decomposition_graph(var_date, model, color_kpi='deepskyblue'):
    '''
    This function has as output a bar plot with all the variables and
    the actual y used

    Input variables

        -model: model
            The model that you want to use
    '''
    if 'np.log(' in model.endog_names:
        data_decomp = loglin_x_beta_fitted_actual(model)
        y_model = np.exp(model.fit().fittedvalues)
        y_werkelijk = np.exp(model.endog)
    else:
        data_decomp = x_beta_fitted_actual(model)[0]
        y_model = model.fit().fittedvalues
        y_werkelijk = model.endog

    x = var_date
    variabelen = data_decomp
    names = list(data_decomp)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y_model, name='y_model'))

    fig.add_trace(go.Scatter(x=var_date, y=y_werkelijk, name=model.endog_names,
                             line_color=color_kpi))

    for i in range(0, variabelen.shape[1]):
        fig.add_trace(go.Bar(x=x, y=variabelen[names[i]], name=names[i]))

    fig.update_layout(barmode='relative', title_text='Decompositie', bargap=0)

    return fig


def actual_vs_fit_graph(var_date, model, color_kpi='deepskyblue', color_fit='dimgray',
                        title_graph='Actual vs model'):
    if 'np.log(' in model.endog_names:
        y_model = np.exp(model.fit().fittedvalues)
        y_werkelijk = np.exp(model.endog)
    else:
        y_model = model.fit().fittedvalues
        y_werkelijk = model.endog
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=var_date, y=y_werkelijk, name=model.endog_names,
                             line_color=color_kpi))

    fig.add_trace(go.Scatter(x=var_date, y=y_model,
                             name=model.endog_names + "_fitted",
                             line_color=color_fit))

    fig.update_layout(title_text='Actual vs model',
                      xaxis_rangeslider_visible=True)
    return fig

def select_n_largest_outliers(n, date, model):
    '''
    Selects the n largets outliers

    :param n: the amount of largest outliers you want
    :param date: the date variable that is used in the model
    :param model: the model you want the outliers from
    :return: the n largest outliers as 2 lists that can be used for a new formula
    '''
    model_fit = model.fit()
    outliers_index = list(abs(model_fit.resid).nlargest(n).index)
    outliers_names = list(date[outliers_index])

    outliers_names_d = []
    for name in outliers_names:
        outliers_names_d.append("d_" + name)

    f = ''
    for dummie in outliers_names_d:
        f = f + " + " + dummie
    return outliers_names_d, f.replace('-', '_')

def VIF(model):
    '''
    :param model: the model used
    :return: The VIF values
    '''
    X = pd.DataFrame(model.exog)
    vif = pd.Series([variance_inflation_factor(X.values, i)
                     for i in range(X.shape[1])], index=model.exog_names)
    return vif

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


def plot_curves(media_var, alphas_scurve, betas, df):
    # pio.renderers.default = 'browser'
    if len(media_var) == 1:
        max_value = df[media_var].max()
    else:
        max_value = max(df[media_var].max())
    x = np.arange(max_value + 0.1 * max_value)

    fig = go.Figure()

    for i in range(0,len(alphas_scurve)):
        fig.add_trace(go.Scatter(x=x, y=betas[i]*s_curve(x, alphas_scurve[i]),
                             name=str(media_var[i])))



        # to plot virtical lines min/mean/max
        l = [i for i in list(df[media_var[i]].array) if i > 0]  # remove all 0 values
        min_ = min(l)
        max_ = max(l)
        mean_ = sum(l) / len(l)

        fig.add_shape(
            # Line Vertical min
            dict(
                type="line",
                x0=min_,
                y0=0,
                x1=min_,
                y1=1,
                line=dict(
                    color="RoyalBlue",
                    width=4,
                    dash="dot",
                )
            ))
        fig.add_shape(
            # Line Vertical mean
            dict(
                type="line",
                x0=mean_,
                y0=0,
                x1=mean_,
                y1=1,
                line=dict(
                    color="Red",
                    width=4,
                    dash="dot",
                )
            ))
        fig.add_shape(
            # Line Vertical min
            dict(
                type="line",
                x0=max_,
                y0=0,
                x1=max_,
                y1=1,
                line=dict(
                    color="Orange",
                    width=4,
                    dash="dot",
                )
            ))
        # Create scatter trace of text labels
        fig.add_trace(go.Scatter(
            x=[min_, mean_, max_],
            y=[1.01, 1.01, 1.01],
            text=["Min media " + media_var[i],
                  "Average media "+ media_var[i],
                  "Max media "+ media_var[i]],
            mode="text",
            name="Inzet values",
        ))


    fig.update_layout(title='Response Curves in the model',
                      xaxis_title='Media-Inzet',
                      yaxis_title='Impact (will be multiplied with your estimated beta)',template='plotly_dark',
                      plot_bgcolor='rgba(0, 0, 0, 0)')

    return fig


def plot_out_of_sample(formule, df, split, y, date):

    model = smf.ols(formula=formule, data=df[:split])
    model.fit().summary()
    results = model.fit()

    actual = df[y]
    model_fit = list(model.fit().predict()) + [None for x in range(len(actual) - split)]
    forecast = [None for x in range(split)] + list(results.predict(df[split:], transform=True))

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=date, y=actual, name='actual sales '))
    fig.add_trace(go.Scatter(x=date, y=model_fit, name='model_fit'))
    fig.add_trace(go.Scatter(x=date, y=forecast, name='forecast out of sample'))

    return fig


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
        x_beta_intercept_correctie.Intercept = x_beta_intercept_correctie.Intercept + sum_negatives_pd

    return x_beta, x_beta_intercept_correctie



def grid_search_decays_one_model(decay_var_to_test, media_curve, alpha, formule_without_vars_to_test, df,
                       decay_values=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], positive=False):
    p_values = []
    decay_accepted = []
    for decay_value in decay_values:
        test_var = '{}(decay({}, {}), {})'.format(media_curve, decay_var_to_test, decay_value, alpha)
        formule_test = formule_without_vars_to_test + ' + ' + test_var
        model = smf.ols(formula=formule_test, data=df)
        p_value_test = model.fit().pvalues[test_var]
        # print(model.fit().params[test_var])
        if positive:
            if model.fit().params[test_var] > 0:
                p_values.append(p_value_test)
                decay_accepted.append(decay_value)
        else:
            p_values.append(p_value_test)
            decay_accepted.append(decay_value)

    df_decay_results = pd.DataFrame()
    df_decay_results['decay'] = decay_accepted
    df_decay_results['p_value'] = p_values

    most_significant_decay = df_decay_results.loc[
        df_decay_results.p_value == df_decay_results.p_value.min()].decay
    return df_decay_results, most_significant_decay


# formule_without_vars_to_test = 'stl_retail_omzet_totaal ~  stl_online_spend + dag_2 + dag_3 + dag_4 + dag_5 + dag_6 + dag_7 + dag_8 + dag_9 + dag_10 + ' \
#                                'jp_gegarandeerd_dummy + dag_maandag + dag_vrijdag + dag_zaterdag + dag_zondag + zondag_10e + zondag_9e ' \
#                                '+ s_curve(decay(radio_grps,0.2),5)'
# decay_var_to_test = 'tv_grps'
# alpha = 5
# media_curve = 's_curve'
# test = grid_search_decays(decay_var_to_test, media_curve, alpha, formule_without_vars_to_test, df,
#                    decay_values=[0.1, 0.2, 0.3, 0.4, 0.45, 0.5, 0.6, 0.7, 0.8, 0.9], positive = False)

def grid_search_alphas_one_model(alpha_var_to_test, media_curve, decay_value, formule_without_vars_to_test, df,
                       alpha_values=list(range(1, 101)), positive=False):
    p_values = []
    alpha_accepted = []
    for alpha_value in alpha_values:
        test_var = '{}(decay({}, {}), {})'.format(media_curve, alpha_var_to_test, decay_value, alpha_value)

        formule_test = formule_without_vars_to_test + ' + ' + test_var
        model = smf.ols(formula=formule_test, data=df)
        p_value_test = model.fit().pvalues[test_var]
        # print(model.fit().params[test_var])
        if positive:
            if model.fit().params[test_var] > 0:
                p_values.append(p_value_test)
                alpha_accepted.append(alpha_value)
        else:
            p_values.append(p_value_test)
            alpha_accepted.append(alpha_value)

    df_alpha_results = pd.DataFrame()
    df_alpha_results['alpha'] = alpha_accepted
    df_alpha_results['p_value'] = p_values

    most_significant_alpha = df_alpha_results.loc[
        df_alpha_results.p_value == df_alpha_results.p_value.min()].alpha
    return df_alpha_results, most_significant_alpha