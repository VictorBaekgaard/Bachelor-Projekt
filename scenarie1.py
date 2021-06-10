#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Run the calibrated model:

import covasim as cv
cv.options.set(dpi=200, show=False, close=True, verbose=0.1)
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
        cv.contact_tracing(start_day='2020-10-02', trace_probs=trace_probs, trace_time=trace_time),
        ]
    
pars = dict(
    pop_size       = pop_size,
    pop_scale      = pop_scale,
    pop_infected   = 6436, #active cases in Denmark by 1/10/2020 (source: https://www.worldometers.info/coronavirus/country/denmark/)
    beta           = 0.019395953846461377,
    asymp_factor   = 1.2613389491583862,
    rel_death_prob = 0.8419695397963538,
    pop_type       = 'hybrid',
    start_day      = '2020-10-01',
    end_day        = '2021-03-25',
    location       = 'Denmark',
    rescale        = True,
    rand_seed      = 1,
    interventions  = interventions,
)

sim = cv.Sim(pars=pars, label = "Efter kalibrering", datafile='superdata.csv')
baseSim = cv.Sim(pars=pars, beta=0.016, asymp_factor=1, rel_death_prob = 1, label = "Før kalibrering", datafile = "superdata.csv")

multi = cv.MultiSim([sim, baseSim])
multi.run()
multi.plot(to_plot=['cum_diagnoses','cum_deaths','new_diagnoses'], fig_args=dict(figsize=(15,15)))



multirun = cv.MultiSim(sim)
multirun.run(n_runs=5)
multirun.median()

multirun.plot_result('r_eff')
