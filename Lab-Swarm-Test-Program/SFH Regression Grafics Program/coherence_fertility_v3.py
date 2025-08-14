#!/usr/bin/env python3
# coherence_fertility_v3.py -- upgraded proxies (v3)
# Notes: proxies improved with explicit parameter dependencies and clearer scaling.
import json, math, warnings, sys
from dataclasses import dataclass
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from scipy.stats import spearmanr
from numpy.linalg import lstsq
RNG = np.random.default_rng(3031)

# Baselines
alpha_0 = 1.0 / 137.035999084
m_e_0 = 9.1093837015e-31
m_p_0 = 1.67262192369e-27
mu_0 = m_p_0 / m_e_0
alpha_s_0 = 0.1181
G_0 = 6.67430e-11
G_F_0 = 1.1663787e-5
c_0 = 299792458.0

@dataclass
class Params:
    alpha: float; mu: float; alpha_s: float; G: float; G_F: float

def bounded(x): return np.clip(x,0.0,1.0)

# Atomic: Bohr binding energy and Bohr radius effects
def atomic_score(params: Params):
    E1 = 0.5 * params.alpha**2 * m_e_0 * c_0**2 # J, positive proxy for binding magnitude
    E1_0 = 0.5 * alpha_0**2 * m_e_0 * c_0**2
    # Use combined metric of binding strength and Bohr radius (a0 ~ 1/(alpha m_e))
    a0 = 1.0/(params.alpha * m_e_0)
    a0_0 = 1.0/(alpha_0 * m_e_0)
    # normalize logs
    e_ratio = E1/E1_0
    a_ratio = a0/a0_0
    # prefer small deviations in both; gaussian penalties
    sE = math.exp(-((math.log(e_ratio)/0.15)**2)/2.0)
    sA = math.exp(-((math.log(a_ratio)/0.20)**2)/2.0)
    return float(bounded(0.6*sE + 0.4*sA))

# Triple-alpha: Hoyle state sensitivity proxy. We implement a scaling where shift in resonance energy
# depends on alpha and alpha_s; use modest linearized sensitivity coefficients motivated by literature.
def triple_alpha_score(params: Params):
    # sensitivity coefficients (approx): dE/E per fractional change in parameter
    s_alpha = 2.0   # relative sensitivity to alpha (placeholder scale)
    s_alphas = 1.0  # sensitivity to alpha_s
    # fractional deviations
    da = (params.alpha - alpha_0)/alpha_0
    das = (params.alpha_s - alpha_s_0)/alpha_s_0
    # resonance energy fractional shift
    frac_shift = s_alpha*da + s_alphas*das
    # yield drops rapidly if shift exceeds few percent; use Gaussian window sigma~0.02
    score = math.exp(-0.5*(frac_shift/0.02)**2)
    return float(bounded(score))

# Deuteron binding: approximate linear sensitivity to alpha_s and mu (quark mass proxy)
def deuteron_score(params: Params):
    # assume deuteron binding E_d ~ E_d0 * (1 + k1*delta(alpha_s) + k2*delta(mu))
    k1 = 1.5
    k2 = 2.0
    da_s = (params.alpha_s - alpha_s_0)/alpha_s_0
    dmu = (params.mu - mu_0)/mu_0
    frac = k1*da_s + k2*dmu
    score = math.exp(-0.5*(frac/0.05)**2)  # sigma ~5%
    return float(bounded(score))

# pp fusion: use Gamow-like exponential sensitivity: tunneling exponent ~ (pi * Z1*Z2*alpha * sqrt(mu_red/E))
# We approximate effect by alpha*sqrt(mu) ratio mapping.
def pp_score(params: Params):
    proxy = params.alpha * math.sqrt(params.mu)
    proxy0 = alpha_0 * math.sqrt(mu_0)
    # map via log-Gaussian with sigma~0.08 (strong sensitivity)
    score = math.exp(-0.5*(math.log(proxy/proxy0)/0.08)**2)
    return float(bounded(score))

# BBN proxy: sensitivity to G and G_F (affect expansion rate and weak rates). Use simple combined dev metric.
def bbn_score(params: Params):
    devG = (params.G - G_0)/G_0
    devGF = (params.G_F - G_F_0)/G_F_0
    dev = math.sqrt((devG/0.15)**2 + (devGF/0.08)**2)
    score = math.exp(-0.5*(dev**2))
    return float(bounded(score))

# Gravitational coherence: large G changes change stellar masses/lifetimes. Penalty beyond ~50%.
def grav_coh(params: Params):
    rel = (params.G - G_0)/G_0
    score = math.exp(- (rel/0.5)**2)
    return float(bounded(score))

# Composite scores
def coherence(params: Params):
    atom = atomic_score(params)
    grav = grav_coh(params)
    ta = triple_alpha_score(params)
    return float(bounded(0.65*atom + 0.25*grav + 0.10*ta))

def fertility(params: Params):
    ta = triple_alpha_score(params)
    dd = deuteron_score(params)
    pp = pp_score(params)
    bb = bbn_score(params)
    return float(bounded(0.50*ta + 0.20*dd + 0.20*pp + 0.10*bb))

# sampling
def sample_mc(N=8000):
    a = RNG.uniform(alpha_0*0.8, alpha_0*1.2, size=N)
    mu = RNG.uniform(mu_0*0.85, mu_0*1.15, size=N)
    alphas = RNG.uniform(alpha_s_0*0.8, alpha_s_0*1.2, size=N)
    Gs = RNG.uniform(G_0*0.2, G_0*5.0, size=N)
    GFs = RNG.uniform(G_F_0*0.6, G_F_0*1.4, size=N)
    rows = []
    for ai, mui, asi, Gi, GFi in zip(a, mu, alphas, Gs, GFs):
        p = Params(alpha=ai, mu=mui, alpha_s=asi, G=Gi, G_F=GFi)
        c = coherence(p); f = fertility(p)
        rows.append({'alpha':ai,'mu':mui,'alpha_s':asi,'G':Gi,'G_F':GFi,'coherence':c,'fertility':f})
    df = pd.DataFrame(rows)
    return df

# Pareto frontier
def pareto(df):
    pts = df[['coherence','fertility']].values
    n = len(pts)
    is_p = np.ones(n, dtype=bool)
    for i in range(n):
        if not is_p[i]: continue
        dom = np.all(pts >= pts[i], axis=1) & np.any(pts > pts[i], axis=1)
        is_p[dom] = False
    return df[is_p].sort_values('coherence',ascending=False).reset_index(drop=True)

# weight sweep, PRCC (same as before)
def prcc(df, target, params_cols):
    ranked = df[params_cols + [target]].rank(method='average').to_numpy()
    X = ranked[:, :-1]; y = ranked[:, -1]
    pr = {}
    for i, col in enumerate(params_cols):
        others = [j for j in range(X.shape[1]) if j != i]
        if others:
            A = np.column_stack([np.ones(X.shape[0]), X[:, others]])
            beta, *_ = lstsq(A, X[:, i], rcond=None)
            rx = X[:, i] - A.dot(beta)
            B = np.column_stack([np.ones(X.shape[0]), X[:, others]])
            beta_y, *_ = lstsq(B, y, rcond=None)
            ry = y - B.dot(beta_y)
        else:
            rx = X[:, i] - X[:, i].mean(); ry = y - y.mean()
        pr[col] = float(np.corrcoef(rx, ry)[0,1])
    return pr

def weight_sweep(df, weights=np.linspace(0,1,41)):
    rows = []
    for w in weights:
        combined = w*df['coherence'] + (1-w)*df['fertility']
        idx = combined.idxmax()
        row = df.loc[idx].to_dict()
        row.update({'w_coh':float(w),'combined':float(combined[idx])})
        rows.append(row)
    return pd.DataFrame(rows)

def find_w_min_for_coh_threshold(df, threshold=0.8):
    # Find minimal w such that the combined-optimum's coherence >= threshold
    ws = np.linspace(0,1,101)
    for w in ws:
        combined = w*df['coherence'] + (1-w)*df['fertility']
        idx = combined.idxmax()
        if df.loc[idx,'coherence'] >= threshold:
            return float(w), df.loc[idx].to_dict()
    return None, None

def main():
    df = sample_mc(8000)
    df.to_csv('samples_v3.csv', index=False)
    p = pareto(df); p.to_csv('pareto_v3.csv', index=False)
    plt.figure(figsize=(7,6)); plt.scatter(df['coherence'], df['fertility'], s=6, alpha=0.25); plt.scatter(p['coherence'], p['fertility'], color='red', s=18); plt.xlabel('Coherence'); plt.ylabel('Fertility'); plt.title('Pareto v3'); plt.tight_layout(); plt.savefig('pareto_v3.png'); plt.close()
    ws = weight_sweep(df); ws.to_csv('weight_sweep_v3.csv', index=False)
    plt.figure(figsize=(8,6)); plt.plot(ws['w_coh'], ws['coherence'], label='coherence'); plt.plot(ws['w_coh'], ws['fertility'], label='fertility'); plt.plot(ws['w_coh'], ws['combined'], label='combined'); plt.legend(); plt.title('Weight sweep v3'); plt.tight_layout(); plt.savefig('weight_sweep_v3.png'); plt.close()
    sens = {'prcc_coh':prcc(df,'coherence',['alpha','mu','alpha_s','G','G_F']),'prcc_fert':prcc(df,'fertility',['alpha','mu','alpha_s','G','G_F'])}
    with open('sensitivity_v3.json','w') as f: json.dump(sens,f,indent=2)
    # find w min for coherence threshold 0.8
    wmin, row = find_w_min_for_coh_threshold(df, threshold=0.8)
    result = {'wmin_for_coh0.8':wmin,'row_at_wmin':row}
    with open('wmin_result_v3.json','w') as f: json.dump(result,f,indent=2)
    print('v3 done: files saved: samples_v3.csv, pareto_v3.png, weight_sweep_v3.png, weight_sweep_v3.csv, sensitivity_v3.json, wmin_result_v3.json')
    print(json.dumps(result, indent=2))
if __name__=='__main__':
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        main()
