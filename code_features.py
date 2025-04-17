import pandas as pd
import math

PATH = "C:/CJIL/isds_data.xlsx"
df = pd.read_excel(PATH, sheet_name="Data")
country_df = pd.read_excel(PATH, sheet_name="Country")
assoc_df = pd.read_excel(PATH, sheet_name="Assoc")
crisis_df = pd.read_excel(PATH, sheet_name="Crisis")
termyr_df = pd.read_excel(PATH, sheet_name="TermYr")

feature_names = ["ID", "y", "Banking", "Currency", "Debt", "Adv_emg", "Prec", "Term_yr",
                 "Treatment", "Expropriation", "Procedure", "ISDS case-by-case consent", "ISDS limitation period", "ISDS local remedies first",
                 "Scope ex taxation", "Scope ex subsidies", "Scope ex procurement", "Scope ex others", "Post-BIT", "MFN exception integration",
                 "MFN exception taxation treaties", "MFN exception procedural issues", "Expropriation exception regulatory", "Expropriation exception compulsory licenses",
                 "Transparency States", "Transparency investors", "Health and environment", "Labor standards", "Right to regulate", "Corp soc resp",
                 "Corruption", "Not lowering of standards", "Voluntary ADR", "ISDS scope of claims", "ISDS limitation", "ISDS policy exclusion",
                 "ISDS taxation or prudential", "Limited remedies", "Allowing amicus curiae"]

no = df["No"].tolist()
parties_list = df["Parties"].tolist()
short_title = df["Short title"].tolist()
dataset = list()

crisis = {party: dict() for party in crisis_df["Country"].tolist()}
for _, row in crisis_df.iterrows():
    crisis[row["Country"]][row["Year"]] = [row["Banking"] if row["Banking"] else 0,
                                           row["Currency"] if row["Currency"] else 0,
                                           row["Debt"] if row["Debt"] else 0]
for i in range(len(no)):
    print(i)
    parties = parties_list[i].split(";\xa0")
    for party in parties:
        if "(" in party:
            members = ""
            for j in range(len(assoc_df["Association"])):
                if party == assoc_df["Association"][j]:
                    members = assoc_df["Members"][j]
            parties_list[i].replace(party, members)
    parties = parties_list[i].split(";\xa0")
    data2 = list()
    for j in range(8, len(feature_names)):
        data2.append(df[feature_names[j]].tolist()[i])
    for yr in range(1993, 2020):
        y = df[yr][i]
        if math.isnan(y):
            continue
        y = int(y)
        id = short_title[i] + '/' + str(yr)
        banking, currency, debt = 0, 0, 0
        advemg_vec = [0, 0]
        prec = 0
        for party in parties:
            try:
                c = crisis[party][yr]
                for k in range(len(c)):
                    if math.isnan(c[k]):
                        c[k] = 0
            except:
                c = [0, 0, 0]
            banking = 1 * (banking or int(c[0]))
            currency = 1 * (currency or int(c[1]))
            debt = 1 * (debt or int(c[2]))
            if advemg_vec != [1, 1]:
                for _, country in country_df.iterrows():
                    if party == country["Parties"]:
                        advemg_vec[0] = 1 * (not advemg_vec[0] and country["Adv"] >= yr)
                        prec += int(country[yr])
        adv_emg = 1 * (advemg_vec == [1, 1])
        term_yr = termyr_df.iloc[i][yr]
        if math.isnan(term_yr):
            term_yr = 0
        data1 = [id, y, banking, currency, debt, adv_emg, prec, term_yr]
        dataset.append(data1 + data2)

pd.DataFrame(dataset).to_excel("C:/CJIL/features.xlsx")