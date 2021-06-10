#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint

def model(y, t, N, lambda_I, gamma):
    S, I, R = y
    dSdt = -lambda_I * S * I / N
    dIdt = lambda_I * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

N = 1000
lambda_I = 0.3
gamma = 1./14

I0 = 1
R0  = 0
S0 = 1000 - I0 - R0
y0 = S0, I0, R0

t = np.linspace(0,100,100)

ret = odeint(model, y0, t, args=(N, lambda_I, gamma))
S, I, R = ret.T

y = ret.T

fig = plt.figure()
ax = fig.add_subplot(111,  axisbelow=True)
ax.plot(t, S/1000, 'b', alpha=0.5, lw=2, label='Modtagelig')
ax.plot(t, I/1000, 'r', alpha=0.5, lw=2, label='Inficeret')
ax.plot(t, R/1000, 'g', alpha=0.5, lw=2, label='Rask med immunitet')
ax.set_xlabel('Tid (dage)')
ax.set_ylabel('Antal (1000\'er)')
ax.set_ylim(0,1.2)
ax.yaxis.set_tick_params(length=0)
ax.xaxis.set_tick_params(length=0)
ax.grid(b=True, which='major', c='w', lw=2, ls='-')
legend = ax.legend()
legend.get_frame().set_alpha(0.5)

plt.savefig("SIR_plot.png")
plt.show()