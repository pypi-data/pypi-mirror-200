import numpy as np
import pandas as pd
from tqdm import tqdm
import plotly.graph_objects as go


class LogisticDecomposition:
    def __init__(self, model):
        self.model = model

    def determine_impact(self, X, y=[], scaling_to_mean_odds_model=True,
                         scaling_to_actual_odds=False):
        model_kans = self.model.predict_proba(X)
        model_kans_list = [item[1] for item in model_kans]
        gemiddelde_kans = np.mean(model_kans_list)
        impact_vars = {}
        vars_ = X.columns

        for var in tqdm(vars_):
            X_model = X.copy()
            X_model[var] = 0
            model_kans_var = self.model.predict_proba(X_model)
            model_kans_list_var = [item[1] for item in model_kans_var]
            gemiddelde_kans_var = np.mean(model_kans_list_var)
            impact_var = gemiddelde_kans - gemiddelde_kans_var
            impact_vars[var] = impact_var

        kans_intercept = self.model.predict_proba(X * 0)
        impact_vars['intercept'] = kans_intercept[0][1]

        if scaling_to_mean_odds_model:
            scalar = gemiddelde_kans / sum(impact_vars.values())
            for key in impact_vars:
                impact_vars[key] = impact_vars[key] * scalar
        if scaling_to_actual_odds:
            scalar = np.mean(y) / sum(impact_vars.values())
            for key in impact_vars:
                impact_vars[key] = impact_vars[key] * scalar
        return impact_vars

    def decomposition_logistic(self, X, split_var=[], plot=True, y=[], X_vars_to_show=[],
                               scaling_to_mean_odds_model=True,
                               scaling_to_actual_odds=False):
        bijdrage_tov_0 = self.determine_impact(X, y=y,
                                               scaling_to_mean_odds_model=scaling_to_mean_odds_model,
                                               scaling_to_actual_odds=scaling_to_actual_odds)

        # bijdrage_tov_0 = determine_impact(model, X)
        results = pd.DataFrame(index=bijdrage_tov_0.keys())

        if len(X_vars_to_show) > 0:
            vars_to_plot = X_vars_to_show
        else:
            vars_to_plot = results.index

        if len(split_var) > 0:
            X_split = X.copy()
            X_split['split_var'] = split_var
            for split_value in X_split['split_var'].unique():
                bijdrage_tov_0_split = self.determine_impact(
                    X_split[X_split['split_var'] == split_value].drop('split_var', axis=1))
                results[str(split_value)] = bijdrage_tov_0_split.values()

            if plot:
                fig = go.Figure()
                for var in vars_to_plot:
                    fig.add_trace(go.Bar(x=X_split['split_var'].unique(), y=results.loc[var], name=var))
                fig.update_layout(barmode='relative', title_text='Decompositie', bargap=0)
                fig.show()
        else:
            if plot:
                fig = go.Figure()
                for var in vars_to_plot:
                    fig.add_trace(go.Bar(x=['Bijdrage'], y=[bijdrage_tov_0[var]], name=var))
                fig.update_layout(barmode='relative', title_text='Decompositie', bargap=0)
                fig.show()
        return bijdrage_tov_0, results
