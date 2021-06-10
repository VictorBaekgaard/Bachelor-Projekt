#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import covasim as cv
cv.options.set(dpi=200, show=False, close=True, verbose=0)
# Create default simulation

total_pop    = 5.806e6 # DK population size
pop_size     = 100e3 # Actual simulated population
pop_scale    = int(total_pop/pop_size)

trace_probs_1 = dict(h=1, s=0.5, w=0.5, c=0.3)
trace_probs_2 = dict(h=1, s=0.6, w=0.6, c=0.4)
trace_probs_3 = dict(h=1, s=0.7, w=0.7, c=0.5)


trace_probs = [trace_probs_1,trace_probs_2,trace_probs_3]
trace_time  = dict(h=0, s=1, w=1, c=2)
trace_time4  = dict(h=1, s=2, w=2, c=4)
trace_time5  = dict(h=2, s=4, w=4, c=6)


beta_days = ['2020-11-20', '2020-12-20', '2021-01-01']

h_beta_changes = [1.3, 2.0, 1.2]
s_beta_changes = [1.3, 0.05, 1.0]
w_beta_changes = [1.3, 0.25, 1.0] 
c_beta_changes = [1.3, 1.5, 1.0]

# Define the beta changes
h_beta = cv.change_beta(days=beta_days, changes=h_beta_changes, layers='h')
s_beta = cv.change_beta(days=beta_days, changes=s_beta_changes, layers='s')
w_beta = cv.change_beta(days=beta_days, changes=w_beta_changes, layers='w')
c_beta = cv.change_beta(days=beta_days, changes=c_beta_changes, layers='c')    


interventions1 = [
        h_beta,
        w_beta,
        s_beta,
        c_beta,
        cv.test_num(daily_tests='data'),
        cv.contact_tracing(start_day='2020-10-02', trace_probs=trace_probs[0], trace_time=trace_time),
        ]
interventions2 = [
        h_beta,
        w_beta,
        s_beta,
        c_beta,
        cv.test_num(daily_tests='data'),
        cv.contact_tracing(start_day='2020-10-02', trace_probs=trace_probs[1], trace_time=trace_time),
        ]
interventions3 = [
        h_beta,
        w_beta,
        s_beta,
        c_beta,
        cv.test_num(daily_tests='data'),
        cv.contact_tracing(start_day='2020-10-02', trace_probs=trace_probs[2], trace_time=trace_time),
        ]
interventions4 = [
        h_beta,
        w_beta,
        s_beta,
        c_beta,
        cv.test_num(daily_tests='data'),
        cv.contact_tracing(start_day='2020-10-02', trace_probs=trace_probs[1], trace_time=trace_time4),
        ]
interventions5 = [
        h_beta,
        w_beta,
        s_beta,
        c_beta,
        cv.test_num(daily_tests='data'),
        cv.contact_tracing(start_day='2020-10-02', trace_probs=trace_probs[1], trace_time=trace_time5),
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
)

n_runs = 5

sim1 = cv.Sim(pars = pars, interventions = interventions1, label = "Færre restriktioner, samme opsporing", datafile = "superdata.csv")
msim1 = cv.MultiSim(sim1)
msim1.run(n_runs=n_runs)
msim1.median()
#msim1.plot_result('cum_infections')  
sim2 = cv.Sim(pars = pars, interventions = interventions2, label = "Opsporing øget med 10%", datafile = "superdata.csv")
msim2 = cv.MultiSim(sim2)
msim2.run(n_runs=n_runs)
msim2.median()
#msim1.plot_result('cum_infections')  
sim3 = cv.Sim(pars = pars, interventions = interventions3, label = "Opsporing øget med 20%", datafile = "superdata.csv")
msim3 = cv.MultiSim(sim3)
msim3.run(n_runs=n_runs)
msim3.median()
#msim1.plot_result('cum_infections') 
sim4 = cv.Sim(pars = pars, interventions = interventions4, label = "Opsporing øget med 10%, 1-dags forsinkelse", datafile = "superdata.csv")
msim4 = cv.MultiSim(sim4)
msim4.run(n_runs=n_runs)
msim4.median()
#msim1.plot_result('cum_infections') 
sim5 = cv.Sim(pars = pars, interventions = interventions5, label = "Opsporing øget med 10%, 2-dages forsinkelse", datafile = "superdata.csv")
msim5 = cv.MultiSim(sim5)
msim5.run(n_runs=n_runs)
msim5.median()
#msim1.plot_result('cum_infections') 

merged = cv.MultiSim.merge([msim1,msim2,msim3,msim4,msim5], base=True)