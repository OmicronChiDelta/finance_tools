# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 10:47:01 2022

@author: Alex White
"""
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
    
    term = 30
    princ = 208499
    rate = 1.04
    fix_years = 5
    over = 350
    
    m = calc_min_payment(princ, rate, term)
    
    month_ids = [i for i in range(12*term)]
    frac_years = [i/12 for i in month_ids]
    
    #Minimal payment
    t_min = [calc_balance(princ, rate, j, m) for j in month_ids]
    
    #Basic monthly overpayment
    t_1 = [calc_balance(princ, rate, j, m+over) for j in month_ids]
    
    #Lump overpayment near end of fixed term, respecting constraint that 10% of the balance can be overpaid in a given year
    t_2 = [calc_balance(princ, rate, j, m, 350*59, 59) for j in month_ids]
    
    fig, ax = plt.subplots()
    ax.set_xlabel("Decimal years")
    ax.set_ylabel("Balance")
    ax.axvline(fix_years, ls="-", c="k", label="end of fixed term")
    
    ax.plot(frac_years, t_min, c="b", label="minimal payments")
    ax.plot(frac_years, t_1, c="r", label=f"£{over} overpayment per month")
    ax.plot(frac_years, t_2, c="gold")
    
    for f in range(5):
        ax.axhline(f*princ/4, ls='--', c='k', alpha=0.1)
    
    ax.legend()
    # ax.set_xlim([0, 10])
    # ax.set_ylim([120000, 1.1*princ])
    plt.tight_layout()