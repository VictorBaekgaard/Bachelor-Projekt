#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Built in calibration:

import sciris as sc
import covasim as cv

# Create default simulation

total_pop    = 5.806e6 # DK population size
pop_size     = 100e3 # Actual simulated population
pop_scale    = int(total_pop/pop_size)

trace_probs = dict(h=1, s=0.5, w=0.5, c=0.3)
trace_time  = dict(h=0, s=1, w=1, c=2)

beta_days = ['2020-10-23', '2020-11-20', '2020-12-15', '2020-12-20', '2021-01-01', '2021-02-01']

h_beta_changes = [1.0, 1.3, 1.2, 2.0, 1.2, 1.0] 
s_beta_changes = [0.85, 1.3, 0.05, 0.05, 0.15, 1.0]
w_beta_changes = [0.75, 1.3, 0.25, 0.25, 0.45, 1.0]
c_beta_changes = [0.95, 1.3, 0.20, 1.5, 0.25, 1.0]

# Define the beta changes
h_beta = cv.change_beta(days=beta_days, changes=h_beta_changes, layers='h')
s_beta = cv.change_beta(days=beta_days, changes=s_beta_changes, layers='s')
w_beta = cv.change_beta(days=beta_days, changes=w_beta_changes, layers='w')
c_beta = cv.change_beta(days=beta_days, changes=c_beta_changes, layers='c')    


interventions = [
        h_beta,
        w_beta,
        s_beta,
        c_beta,
        cv.test_num(daily_tests='data'),
        cv.contact_tracing(start_day='2020-10-02', trace_probs=trace_probs, trace_time=trace_time)
        ]
    
pars = sc.objdict(
    pop_size       = pop_size,
    pop_scale      = pop_scale,
    pop_infected   = 6436, #active cases in dk 1/10/2020
    beta           = 0.016,
    asymp_factor   = 1,
    rel_death_prob = 1,
    pop_type       = 'hybrid',
    start_day      = '2020-10-01',
    end_day        = '2021-03-25',
    location       = 'Denmark',
    rescale        = True,
    #rescale_factor = 2,
    rand_seed      = 1,
    interventions  = interventions,
    verbose        = 0,
)

sim = cv.Sim(pars=pars, datafile='superdata.csv')

# Parameters to calibrate -- format is best, low, high
calib_pars = dict(
    beta           = [pars.beta, 0.017, 0.020],
    asymp_factor   = [pars.asymp_factor, 1.0, 1.3],
    rel_death_prob = [pars.rel_death_prob, 0.80, 1.0]
)

if __name__ == '__main__':

    # Run the calibration simulates 100 x 4 = 400 trials
    n_trials = 100
    n_workers = 4
    calib = sim.calibrate(calib_pars=calib_pars, n_trials=n_trials, n_workers=n_workers)