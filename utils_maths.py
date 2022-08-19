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


def freq_scaling(freq):
    scaling = {"d":365,"w":52, "m":12, "y":1}
    return scaling[freq]


def effective_rate(rate_year, freq):
    """
    Given a yearly interest rate, compute the effective rate to apply at a 
    sub-year frequency (daily, weekly, monthly etc.)
    
    ARGUMENTS
    rate_year
    --> rate as a %
    
    freq
    --> letter indicating the frequency to multiply in order to induce a rate
    of "rate_year"
    
    RETURNS
    quantity to multiply an amount by at frequency "freq" to yield a rate of
    "rate_year" after 1 calendar year
    """
    
    assert(freq in ["d", "w", "m", "y"])
    return 10**(np.log10(1+ 0.01*rate_year)/freq_scaling(freq))
    
    
def repayment_amount(principal, term_years, rate_year, freq):
    """
    Compute the minimum payment someone would need to make at a given frequency
    in order to clear a principal over a given term at a fixed rate
    """
    assert(freq in ["d", "w", "m", "y"])
    n_payments = freq_scaling(freq)*term_years
    rate_inc = effective_rate(rate_year, freq)
    return -principal*(1 - rate_inc)/(rate_inc**-n_payments - 1)