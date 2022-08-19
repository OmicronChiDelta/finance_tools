import pytest
from utils_maths import freq_scaling, effective_rate, repayment_amount

@pytest.mark.parametrize("rate_year, freq", [(5, "d"), 
                                             (5, "w"), 
                                             (5, "m"), 
                                             (5, "y")])
def test_effective_rate(rate_year, freq):
    back_to_year = effective_rate(rate_year, freq)**freq_scaling(freq)
    year_mult = 1 + 0.01*rate_year
    assert(abs(back_to_year - year_mult) < 0.0001)
    
@pytest.mark.parametrize("principal, term_years, rate_year, target", [(200000, 10, 5, 2122), 
                                                                      (300000, 20, 3, 1664),
                                                                      (100000, 30, 1, 321)])
def test_minimal_repayment(principal, term_years, rate_year, target):
    assert(int(repayment_amount(principal, term_years, rate_year, "m")) + target < 1)