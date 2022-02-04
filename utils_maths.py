# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 10:47:01 2022

@author: Alex White
"""
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def calc_min_payment(principal, rate, term_years):
    """
    Given mortgage deal information, deduce the moinimum monthly payment to pay off the loan
    """
    phi = 1 + rate/1200
    term_months = 12*term_years
    m_min = principal*(1 - phi**-1)/(1 - phi**-term_months)
    return m_min

def calc_balance(principal, rate, month_idx, payment, spot_over=0, spot_idx=0):
    """
    Given an initial amount, rate and month index since payment started, and the monthly repayment, calculate the balance
    """
    phi = 1 + rate/1200
    phi_k = phi**month_idx
    payment_factor = (1 - 1/phi_k)/(1 - 1/phi)
    balance = phi_k*(principal - payment*payment_factor)
    
    if month_idx >= spot_idx and spot_over > 0:
        balance = balance - spot_over*phi**(month_idx - spot_idx + 1)

    #Catch redemption
    balance = 0 if balance < 0 else balance
    return balance


if __name__ == "__main__":
    
    plt.close("all")
    
    
    #%% Interest rate info
    # rates = pd.read_csv("E:\\finance_tools\\data\\variable_rates.csv")
    rates = pd.read_csv(".\\data\\variable_rates.csv")
    rates["Date"] = pd.to_datetime(rates["Date"])
    rates.sort_values(by="Date", ascending=True, inplace=True)
    rates.reset_index(drop=True, inplace=True)
    
    #tidy columns
    rate_columns = rates.columns[1::]
    actual_rates = [c.split(" LTV)")[0][-3::] for c in rate_columns]
    rates.rename({a:b for a, b in zip(rate_columns, actual_rates)}, axis=1, inplace=True)
    for r in actual_rates:
        rates[r].replace("..", np.nan, inplace=True)
        rates[r] = rates[r].astype(float)
        
    fig, ax = plt.subplots()
    for r in actual_rates:
        ax.plot(rates.index, rates[r], label=f"LTV: {r}")
    ax.legend()
    

    #%%Intelligent interpolation
    
    
    #%%possible futures
    future_field = "75%"
    num_reps = 500
    num_months = 30*12
    vals = list(rates[future_field].dropna().values)
    
    #create num_reps futures of length num_months
    futures = [random.choices(vals, k=num_months) for j in range(num_reps)]

    #empirical 95% CI
    month_sims = [[row[i] for row in futures] for i in range(num_months)]
    q_low  = [np.quantile(i, 0.025) for i in month_sims]
    q_high = [np.quantile(i, 0.975) for i in month_sims]
    
    fig, ax = plt.subplots()
    ax.fill_between(range(num_months), q_low, q_high)

    
    #%%
    # term = 30
    # princ = 208499
    # rate = 1.04
    # fix_years = 5
    # over = 350
    
    # m = calc_min_payment(princ, rate, term)
    
    # month_ids = [i for i in range(12*term)]
    # frac_years = [i/12 for i in month_ids]
    
    # #Minimal payment
    # t_min = [calc_balance(princ, rate, j, m) for j in month_ids]
    
    # #Basic monthly overpayment
    # t_1 = [calc_balance(princ, rate, j, m+over) for j in month_ids]
    
    # #Lump overpayment near end of fixed term, respecting constraint that 10% of the balance can be overpaid in a given year
    # t_2 = [calc_balance(princ, rate, j, m, 350*59, 59) for j in month_ids]
    
    # fig, ax = plt.subplots()
    # ax.set_xlabel("Decimal years")
    # ax.set_ylabel("Balance")
    # ax.axvline(fix_years, ls="-", c="k", label="end of fixed term")
    
    # ax.plot(frac_years, t_min, c="b", label="minimal payments")
    # ax.plot(frac_years, t_1, c="r", label=f"£{over} overpayment per month")
    # ax.plot(frac_years, t_2, c="gold")
    
    # for f in range(5):
    #     ax.axhline(f*princ/4, ls='--', c='k', alpha=0.1)
    
    # ax.legend()
    # # ax.set_xlim([0, 10])
    # # ax.set_ylim([120000, 1.1*princ])
    # plt.tight_layout()