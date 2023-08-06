import sys, numpy as np
sys.path.append('../src/')
import networkinference.utils as nu
import networkinference as ni

print('\nRGG')
A = nu.FakeData.random_geometric()

print('\nsumstats')
ni.core.sumstats(A)

print('\nsumstats with arguments')
ni.core.sumstats(A, decimals=6)

print('\nplot spectrum')
ni.core.plot_spectrum(A)

print('\nplot spectrum with arguments')
ni.core.plot_spectrum(A, giant=False, weight=None, xlim_scat_buffer=0.1, ylim_scat_buffer=0.1, \
            xticks_scat=8, yticks_scat=8, xticks_hist=3, binwidth=None, binrange=None, figsize=(16, 7), \
            title_hist='Hi', title_scat='Sc', title_y='Ei', sns_style='dark')

print('\nspectrum')
x = ni.core.spectrum(A, giant=True, weight=None)

print('\nspectral clustering')
clusters = ni.core.spectral_clustering(5, A, seed=None)

print('\nconductance')
print(ni.core.conductance(clusters, A, weight=None))

print('\nER')
A = nu.FakeData.erdos_renyi()
ni.core.sumstats(A)
ni.core.plot_spectrum(A)

print('\nnhbr mean')
Z = nu.nhbr_mean(np.random.rand(500), A, distance=2)

print('\nadjrownorm')
A_norm = nu.adjrownorm(A)

print('\nLIM')
Y, X = nu.FakeData.linear_in_means(nu.FakeData.erdos_renyi(), theta=np.array([0,0,0,0]))

print('\nIPW')
Y, ind1, ind0, pscores1, pscores0, A = nu.FakeData.ipw()

print('\nOLS')
Y, X, A = nu.FakeData.ols()

print('\nTSLS')
Y, X, W, A = nu.FakeData.tsls(network='RGG')

print('\nIPW with arguments')
Y, ind1, ind0, pscores1, pscores0, A = nu.FakeData.ipw(n=300, network='ER', avg_deg=10, p = 0.5, seed=0)

print('\nOLS with arguments')
Y, X, A = nu.FakeData.ols(n=300, network='ER', avg_deg=10, seed=0)

print('\nTSLS with arguments')
Y, X, W, A = nu.FakeData.tsls(n=300, network='ER', avg_deg=10, seed=0)

