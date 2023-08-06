import pandas as pd
import numpy as np
from scipy.stats import skewnorm
import warnings
warnings.filterwarnings("ignore")


class GenerateData():

    def __init__(self, N=10000):
        self.N = N

    def generate_dataset(self):
        leeftijd = []
        for i in range(0, self.N):
            n = np.random.randint(18, 80)
            leeftijd.append(n)

        geslacht = []
        for i in range(0, self.N):
            random_number = np.random.uniform(0, 1)
            if random_number > 0.6:
                geslacht.append('Vrouw')
            if random_number < 0.55:
                geslacht.append('Man')
            if 0.55 < random_number < 0.6:
                geslacht.append('Anders')

        maxValue = 1
        skewness_left = -3  # Negative values are left skewed, positive values are right skewed.
        random_left = skewnorm.rvs(a=skewness_left, loc=maxValue, size=self.N)  # Skewnorm function
        random_left = random_left - min(random_left)  # Shift the set so the minimum value is equal to zero.
        random_left = random_left / max(random_left)  # Standadize all the vlues between 0 and 1.
        random_left = random_left * maxValue

        skewness_right = 3
        random_right = skewnorm.rvs(a=skewness_right, loc=maxValue, size=self.N)  # Skewnorm function
        random_right = random_right - min(random_right)  # Shift the set so the minimum value is equal to zero.
        random_right = random_right / max(random_right)  # Standadize all the vlues between 0 and 1.
        random_right = random_right * maxValue

        percentage_gelezen_mails = []
        for i in range(0, self.N):
            persoon = geslacht[i]
            if persoon == 'Man':
                percentage_gelezen_mails.append(random_right[i])
            if persoon == 'Vrouw':
                percentage_gelezen_mails.append(random_left[i])
            if persoon == 'Anders':
                percentage_gelezen_mails.append(np.random.uniform(0, 1))

        eerdere_mails = []
        for i in range(0, self.N):
            eerdere_mails.append(np.random.randint(0, 10))

        contact_vorm = []
        for i in range(0, self.N):
            if np.random.randint(0, 10) > 8:
                contact_vorm.append('bellen')
            else:
                contact_vorm.append('mailen')

        # rol = []
        # for i in range(0, self.N):
        #     persoon = geslacht[i]
        #     if persoon == 'Man':
        #         if random_right[i] > 0.5:
        #             rol.append('donateur')
        #         else:
        #             rol.append('vrijwilliger')
        #     if persoon == 'Vrouw':
        #         if random_right[i] < 0.4:
        #             rol.append('donateur')
        #         else:
        #             rol.append('vrijwilliger')
        #     if persoon == 'Anders':
        #         if np.random.uniform(0, 1) > 0.5:
        #             rol.append('donateur')
        #         else:
        #             rol.append('vrijwilliger')

        actie_instroom = []
        for i in range(0, self.N):
            persoon = geslacht[i]
            if persoon == 'Man':
                if np.random.uniform(0, 1) > 0.4:
                    actie_instroom.append('actie_A')
                else:
                    actie_instroom.append('actie_B')
            if persoon == 'Vrouw':
                if np.random.uniform(0, 1) > 0.6:
                    actie_instroom.append('actie_A')
                else:
                    actie_instroom.append('actie_B')
            if persoon == 'Anders':
                if np.random.uniform(0, 1) > 0.5:
                    actie_instroom.append('actie_A')
                else:
                    actie_instroom.append('actie_B')

        kanaal_instroom = []
        for i in range(0, self.N):
            random_number = np.random.uniform(0, 1)
            if random_number > 0.6:
                kanaal_instroom.append('instroom_website')
            if random_number < 0.55:
                kanaal_instroom.append('instroom_mailing')
            if 0.55 < random_number < 0.6:
                kanaal_instroom.append('instroom_anders')

        maanden_lid = []
        for i in range(0, self.N):
            maanden_lid.append(np.random.randint(0, 100))

        mail = []
        for i in range(0, self.N):
            random_number = np.random.uniform(0, 1)
            if random_number > 0.8:
                mail.append('type_A_gelezen')
            if random_number < 0.55:
                mail.append('type_B_gelezen')
            if 0.55 < random_number < 0.8:
                mail.append('geen_ontvangen')

        results = {
            'maanden_lid': maanden_lid,
            'kanaal_instroom': kanaal_instroom,
            'actie_instroom': actie_instroom,
            # 'rol': rol,
            'contact_vorm': contact_vorm,
            'eerdere_mails': eerdere_mails,
            'percentage_gelezen_mails': percentage_gelezen_mails,
            'geslacht': geslacht,
            'leeftijd': leeftijd,
            'mail': mail
        }

        df = pd.DataFrame(results)
        X = pd.get_dummies(df)
        # + 1 * X['rol_donateur'] + -5 * X['rol_vrijwilliger']
        likelihood_y = -0.1 * X['maanden_lid'] + -1 * X['eerdere_mails'] + 10 * X['percentage_gelezen_mails'] + 0.01 * \
                       X[
                           'leeftijd'] - 1 * X['kanaal_instroom_instroom_mailing'] + 2 * X[
                           'kanaal_instroom_instroom_anders'] + -0.5 * X[
                           'kanaal_instroom_instroom_website'] + 2 * X['actie_instroom_actie_A'] + -3 * X[
                           'actie_instroom_actie_B'] + -3 * X[
                           'contact_vorm_bellen'] + 2 * X['contact_vorm_mailen'] + 0 * X['geslacht_Anders'] + -2 * X[
                           'geslacht_Man'] + -3 * X['geslacht_Vrouw'] + -5 * X['mail_geen_ontvangen'] + -8 * X[
                           'mail_type_A_gelezen'] + 3 * X['mail_type_B_gelezen'] + -13 * X['mail_type_B_gelezen'] * X[
                           'geslacht_Vrouw'] + 8 * X['mail_type_A_gelezen'] * X[
                           'geslacht_Vrouw'] + -20 * np.random.uniform(-1, 1)

        likelihood_y = likelihood_y - min(likelihood_y)  # Shift the set so the minimum value is equal to zero.
        likelihood_y = likelihood_y / max(likelihood_y)  # Standadize all the values between 0 and 1.


        # meerdere merken kiezen
        likelihood_ejp = 8 + -0.1 * X['maanden_lid'] + -0.01 * X['leeftijd'] + 0 * X['geslacht_Anders'] + 2 * X[
            'geslacht_Man'] + -3 * X['geslacht_Vrouw'] + 2 * X['actie_instroom_actie_A'] + -3 * X[
                             'actie_instroom_actie_B'] + -10 * np.random.uniform(-1, 1)

        likelihood_lotto = 7 + -0.2 * X['maanden_lid'] + -0.001 * X['leeftijd'] + 2 * X['geslacht_Anders'] + 0.5 * X[
            'geslacht_Man'] + -1 * X['geslacht_Vrouw'] + 4 * X['actie_instroom_actie_A'] + -1 * X[
                               'actie_instroom_actie_B'] + -10 * np.random.uniform(-1, 1)

        likelihood_mjs = 2 + -0.1 * X['maanden_lid'] + -0.005 * X['leeftijd'] + 1 * X['geslacht_Anders'] + 1.5 * X[
            'geslacht_Man'] + 2 * X['geslacht_Vrouw'] + 1 * X['actie_instroom_actie_A'] + 1 * X[
                             'actie_instroom_actie_B'] + -10 * np.random.uniform(-1, 1)

        likelihood_ld = 1 + -0.15 * X['maanden_lid'] + -0.015 * X['leeftijd'] + 0 * X['geslacht_Anders'] + 2.5 * X[
            'geslacht_Man'] - 2 * X['geslacht_Vrouw'] + 2 * X['actie_instroom_actie_A'] + -1 * X[
                            'actie_instroom_actie_B'] + -10 * np.random.uniform(-1, 1)

        likelihood_geen = 22 + -0.07 * X['maanden_lid'] + -0.02 * X['leeftijd'] + 1 * X['geslacht_Anders'] - 2 * X[
            'geslacht_Man'] + -5 * X['geslacht_Vrouw'] + 1 * X['actie_instroom_actie_A'] + -2 * X[
                              'actie_instroom_actie_B'] + -10 * np.random.uniform(-1, 1)

        likelihoods_merken = pd.DataFrame()
        likelihoods_merken['ejp'] = likelihood_ejp
        likelihoods_merken['lotto'] = likelihood_lotto
        likelihoods_merken['mjs'] = likelihood_mjs
        likelihoods_merken['ld'] = likelihood_ld
        likelihoods_merken['geen'] = likelihood_geen
        likelihoods_merken = likelihoods_merken + abs(likelihoods_merken.min().min())
        likelihoods_merken = likelihoods_merken.div(likelihoods_merken.sum(axis=1), axis=0)

        keuze_tweede_merk_stl_spelers = ['ejp', 'lotto', 'mjs', 'ld', 'geen']
        tweede_merk_keuze_stl_spelers = []
        for i in range(0, len(likelihoods_merken)):
            likelihoods_merken.iloc[0].values
            d = dict(zip(keuze_tweede_merk_stl_spelers, likelihoods_merken.iloc[0].values))
            tweede_merk_keuze_stl_spelers.append(loting(d))

        churn = np.where(likelihood_y > 0.6, 1, 0)
        df['churn'] = churn
        df['tweede_merk_keuze_stl_spelers'] = tweede_merk_keuze_stl_spelers

        return df


def loting(merken_kansen):
    ordered_kansen = dict(sorted(merken_kansen.items(), key=lambda x: x[1]))
    random_nr = np.random.uniform(0, 1)
    kans_1 = list(ordered_kansen.values())[0]
    kans_2 = list(ordered_kansen.values())[1] + kans_1
    kans_3 = list(ordered_kansen.values())[2] + kans_2
    kans_4 = list(ordered_kansen.values())[3] + kans_3
    kans_5 = list(ordered_kansen.values())[4]
    results = [np.where(random_nr <= kans_1, list(ordered_kansen.keys())[0], '').item(),
               np.where((random_nr > kans_1) & (random_nr <= kans_2), list(ordered_kansen.keys())[1], '').item(),
               np.where((random_nr > kans_2) & (random_nr <= kans_3), list(ordered_kansen.keys())[2], '').item(),
               np.where((random_nr > kans_3) & (random_nr <= kans_4), list(ordered_kansen.keys())[3], '').item(),
               np.where(random_nr > 1 - kans_5, list(ordered_kansen.keys())[4], '').item()]
    while '' in results:
        results.remove('')
    return results[0]

