#!/usr/bin/env python3
# analysis_v2.py -- Pareto + weight-sweep + sensitivity analysis for Option A model
import json, math, sys, warnings
from dataclasses import dataclass
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
from numpy.linalg import lstsq

RNG = np.random.default_rng(2025)

# Baseline constants (same as v2)
alpha_0 = 1.0 / 137.035999084
c_0 = 299792458.0
hbar_0 = 1.054571817e-34
m_e_0 = 9.1093837015e-31
m_p_0 = 1.67262192369e-27
mu_0 = m_p_0 / m_e_0
alpha_s_0 = 0.1181
G_0 = 6.67430e-11
G_F_0 = 1.1663787e-5

# Ranges
ALPHA_RANGE = (alpha_0 * 0.85, alpha_0 * 1.15)
MU_RANGE = (mu_0 * 0.85, mu_0 * 1.15)
ALPHAS_RANGE = (alpha_s_0 * 0.8, alpha_s_0 * 1.2)
G_RANGE = (G_0 * 0.1, G_0 * 10.0)
GF_RANGE = (G_F_0 * 0.5, G_F_0 * 1.5)

@dataclass
class Params:
    alpha: float; mu: float; alpha_s: float; G: float; G_F: float

def bounded(x): return np.clip(x, 0.0, 1.0)

def hydrogen_binding_ev(alpha):
    E_J = -0.5 * (alpha**2) * m_e_0 * c_0**2
    return E_J / 1.602176634e-19

def atomic_coherence(params: Params)->float:
    E1 = abs(hydrogen_binding_ev(params.alpha))
    E1_0 = abs(hydrogen_binding_ev(alpha_0))
    sigma = 0.15
    score = math.exp(-((E1/E1_0 - 1.0)/sigma)**2)
    return float(bounded(score))

def triple_alpha_score(params: Params)->float:
    rel_alpha = (params.alpha - alpha_0)/alpha_0
    rel_alphas = (params.alpha_s - alpha_s_0)/alpha_s_0
    dev = math.sqrt((rel_alpha/0.02)**2 + (rel_alphas/0.05)**2)
    score = math.exp(-0.5 * dev**2)
    return float(bounded(score))

def deuteron_score(params: Params)->float:
    rel_alphas = (params.alpha_s - alpha_s_0)/alpha_s_0
    rel_mu = (params.mu - mu_0)/mu_0
    dev = math.sqrt((rel_alphas/0.06)**2 + (rel_mu/0.05)**2)
    score = math.exp(- (dev**2))
    return float(bounded(score))

def pp_fusion_score(params: Params)->float:
    proxy = params.alpha * math.sqrt(params.mu)
    proxy0 = alpha_0 * math.sqrt(mu_0)
    ratio = proxy/proxy0
    sigma = 0.10
    score = math.exp(-0.5 * (math.log(ratio)/sigma)**2)
    return float(bounded(score))

def bbn_score(params: Params)->float:
    rel_G = (params.G - G_0)/G_0
    rel_GF = (params.G_F - G_F_0)/G_F_0
    dev = math.sqrt((rel_G/0.2)**2 + (rel_GF/0.1)**2)
    score = math.exp(- (dev**2)/2.0)
    return float(bounded(score))

def coherence_score(params: Params)->float:
    atomic = atomic_coherence(params)
    relG = abs((params.G - G_0)/G_0)
    grav_score = math.exp(- (relG/0.25)**2)
    return float(bounded(0.6*atomic + 0.3*grav_score + 0.1*triple_alpha_score(params)))

def fertility_score(params: Params)->float:
    ta = triple_alpha_score(params)
    dd = deuteron_score(params)
    pp = pp_fusion_score(params)
    bb = bbn_score(params)
    return float(bounded(0.45*ta + 0.25*dd + 0.2*pp + 0.1*bb))

def combined_scalar(coh, fert, w_coh=0.8):
    return float(bounded(w_coh*coh + (1-w_coh)*fert))

# Monte Carlo sampling across the 5 constants
def sample_mc(N=5000):
    alphas = RNG.uniform(ALPHA_RANGE[0], ALPHA_RANGE[1], size=N)
    mus = RNG.uniform(MU_RANGE[0], MU_RANGE[1], size=N)
    alphas_s = RNG.uniform(ALPHAS_RANGE[0], ALPHAS_RANGE[1], size=N)
    Gs = RNG.uniform(G_RANGE[0], G_RANGE[1], size=N)
    GFs = RNG.uniform(GF_RANGE[0], GF_RANGE[1], size=N)
    rows = []
    for a, mu, as_, G, GF in zip(alphas, mus, alphas_s, Gs, GFs):
        p = Params(alpha=a, mu=mu, alpha_s=as_, G=G, G_F=GF)
        coh = coherence_score(p)
        fert = fertility_score(p)
        rows.append({'alpha':a,'mu':mu,'alpha_s':as_,'G':G,'G_F':GF,'coherence':coh,'fertility':fert})
    return pd.DataFrame(rows)

# Pareto frontier (non-dominated)
def pareto_frontier(df):
    # keep points that are not dominated (higher is better for both)
    pts = df[['coherence','fertility']].values
    is_pareto = np.ones(len(pts), dtype=bool)
    for i, p in enumerate(pts):
        if not is_pareto[i]: continue
        # any point that is >= p in both and > in one will dominate p (we want non-dominated)
        dominated = np.all(pts >= p, axis=1) & np.any(pts > p, axis=1)
        is_pareto[dominated] = False
    pareto_df = df[is_pareto].copy()
    # sort by coherence descending
    pareto_df = pareto_df.sort_values(by='coherence', ascending=False).reset_index(drop=True)
    return pareto_df

# PRCC via rank-transform + linear residual correlation
def prcc(df, target_col, param_cols):
    # rank-transform
    ranked = df[param_cols + [target_col]].rank(method='average').to_numpy()
    X = ranked[:, :-1]
    y = ranked[:, -1]
    prccs = {}
    for i, col in enumerate(param_cols):
        # regress X[:, i] on other X's to get residuals r_x
        others_idx = [j for j in range(X.shape[1]) if j != i]
        if len(others_idx) > 0:
            A = np.column_stack([np.ones(X.shape[0]), X[:, others_idx]])
            beta, *_ = lstsq(A, X[:, i], rcond=None)
            r_x = X[:, i] - A.dot(beta)
            # regress y on other Xs to get residual r_y
            B = np.column_stack([np.ones(X.shape[0]), X[:, others_idx]])
            beta_y, *_ = lstsq(B, y, rcond=None)
            r_y = y - B.dot(beta_y)
        else:
            r_x = X[:, i] - X[:, i].mean()
            r_y = y - y.mean()
        # compute correlation
        corr = np.corrcoef(r_x, r_y)[0,1]
        prccs[col] = float(corr)
    return prccs

def weight_sweep(df, weights=np.linspace(0.0,1.0,21)):
    results = []
    for w in weights:
        combined = w*df['coherence'] + (1-w)*df['fertility']
        idx = combined.idxmax()
        row = df.loc[idx]
        results.append({'w_coh':float(w),'alpha':float(row['alpha']),'mu':float(row['mu']),'alpha_s':float(row['alpha_s']),
                        'G':float(row['G']),'G_F':float(row['G_F']),'coherence':float(row['coherence']),'fertility':float(row['fertility']),
                        'combined':float(combined[idx])})
    return pd.DataFrame(results)

def main():
    N = 6000  # Monte Carlo samples
    df = sample_mc(N=N)
    df.to_csv('samples_mc_v2.csv', index=False)
    # Pareto frontier
    pareto = pareto_frontier(df)
    pareto.to_csv('pareto_points_v2.csv', index=False)
    # Plot pareto
    plt.figure(figsize=(7,6))
    plt.scatter(df['coherence'], df['fertility'], s=6, alpha=0.25, label='samples')
    plt.scatter(pareto['coherence'], pareto['fertility'], color='red', s=20, label='Pareto frontier')
    plt.scatter([alpha_0*0+1], [0], alpha=0) # dummy to fix legend spacing
    plt.scatter([np.nan],[np.nan], label='Our Universe', marker='*') # placeholder
    plt.xlabel('Coherence'); plt.ylabel('Fertility'); plt.title('Pareto: Coherence vs Fertility (v2 proxies)')
    plt.legend()
    plt.tight_layout(); plt.savefig('pareto_v2.png'); plt.close()
    # Weight sweep
    ws = weight_sweep(df)
    ws.to_csv('weight_sweep_v2.csv', index=False)
    plt.figure(figsize=(8,6))
    plt.plot(ws['w_coh'], ws['coherence'], label='coherence at optimum')
    plt.plot(ws['w_coh'], ws['fertility'], label='fertility at optimum')
    plt.plot(ws['w_coh'], ws['combined'], label='combined score')
    plt.xlabel('w_coh'); plt.ylabel('value'); plt.title('Weight sweep: optimum values vs w_coh')
    plt.legend(); plt.tight_layout(); plt.savefig('weight_sweep_v2.png'); plt.close()
    # Sensitivity: Spearman and PRCC
    params = ['alpha','mu','alpha_s','G','G_F']
    spearman = {}
    prccs_coh = prcc(df, 'coherence', params)
    prccs_fert = prcc(df, 'fertility', params)
    for p in params:
        rho_c, pval_c = spearmanr(df[p], df['coherence'])
        rho_f, pval_f = spearmanr(df[p], df['fertility'])
        spearman[p] = {'coherence_rho':float(rho_c),'coherence_p':float(pval_c),'fertility_rho':float(rho_f),'fertility_p':float(pval_f)}
    sens = {'spearman':spearman, 'prcc_coherence':prccs_coh, 'prcc_fertility':prccs_fert}
    with open('sensitivity_report_v2.json','w') as f:
        json.dump(sens, f, indent=2)
    print('Wrote samples and reports. Summary of top sensitivities (PRCC magnitude):')
    # display sorted PRCCs
    def top_prcc(pr):
        return sorted(pr.items(), key=lambda x: abs(x[1]), reverse=True)
    print('Coherence PRCC (abs desc):', top_prcc(prccs_coh))
    print('Fertility PRCC (abs desc):', top_prcc(prccs_fert))
    # Also print weight-sweep table head
    print('\\nWeight sweep (first 5 rows):')
    print(ws.head().to_string(index=False))
if __name__=='__main__':
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        main()
