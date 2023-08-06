##### Parse command line arguments #####

import sys
if len(sys.argv) == 1:
   method = 'IPW'  # defaults
   network = 'ER' 
elif len(sys.argv) == 3:
    method = str(sys.argv[1])
    if method not in ['OLS', 'TSLS', 'IPW']: 
        raise ValueError('First command line argument must be OLS, TSLS, or IPW.')
    network = str(sys.argv[2])
    if network not in ['RGG', 'ER']:
        raise ValueError('Second command line argument must be RGG or ER.')
else:
    raise ValueError('Script takes either 0 or 2 command line arguments.')

##### Main #####

import numpy as np, sys
sys.path.append('../src/')
import networkinference as ni
import networkinference.utils as nu

n = 500 # number of nodes
seed = 0

if method == 'IPW':
    Y, ind1, ind0, pscores1, pscores0, A = nu.FakeData.ipw(n, network=network, seed=seed)
    netinf = ni.IPW(Y, ind1, ind0, pscores1, pscores0, A)
    theta = np.array([2])
    dimension = 0 # dimension of the estimand on which we will conduct inference
elif method == 'OLS':
    Y, X, A = nu.FakeData.ols(n, network=network, seed=seed)
    netinf = ni.OLS(Y, X, A)
    theta = np.array([1,1])
    dimension = 1
else:
    Y, X, W, A = nu.FakeData.tsls(n, network=network, seed=seed)
    netinf = ni.TSLS(Y, X, W, A)
    theta = np.array([1,0.5,3,1])
    dimension = 1

print(f'Method: {method}. Network: {network}.')

print('\nEstimate')
print(netinf.estimate)

print('\nSummands stdev')
print(netinf.summands.std(axis=0))

if method != 'IPW':
    print('\nScores stdev')
    print(netinf.scores.std(axis=0))

    print('\ninvhessian')
    print(netinf.invhessian)

    print('\nResids stdev')
    print(netinf.resid.std(axis=0))

print('\nnetwork_se table')
netinf.network_se()

print('\nnetwork_se table with arguments')
netinf.network_se(b=1, decimals=4, verbose=False, PD_alert=True)

print('\nvar_hac')
print(netinf.network_se_vcov)

print('\nse_hac')
print(netinf.network_se_result)

print('\ndrobust_test')
netinf.drobust_test(theta[dimension], dimension=dimension, seed=seed)

print('\ndrobust_test with arguments')
netinf.drobust_test(theta[dimension], dimension=dimension, alpha=0.05, beta=0.01, R=800, L=900, seed=None, verbose=False)

print('\ntest_drobust')
print(netinf.drobust_test_result)

print('\ndrobust_ci table')
netinf.drobust_ci(theta[dimension]-2, theta[dimension]+2, dimension=dimension, seed=seed)

print('\ndrobust_ci table with arguments')
netinf.drobust_ci(theta[dimension]-2, theta[dimension]+2, dimension=dimension, grid_size=151, coverage=0.95, \
            beta=0.01, R=800, L=900, seed=None, decimals=1, verbose=False)

print('\nci_drobust')
print(netinf.drobust_ci_result)

print('\nget_clusters')
netinf.get_clusters(10, seed=seed)

print('\nget_clusters with arguments')
netinf.get_clusters(5, clusters=netinf.clusters, seed=None, weight=None, verbose=True)

print('\nclusters')
print(netinf.clusters)

print('\nconductance')
print(netinf.conductance)

print('\ntrobust_ci table')
netinf.trobust_ci()

print('\ntrobust_ci table with arguments')
netinf.trobust_ci(dimension=None, num_clusters=5, coverage=0.95, decimals=3, verbose=False)

print('\ntrobust_ci_result')
print(netinf.trobust_ci_result)

print('\narand_test')
netinf.arand_test(theta[dimension], dimension=dimension)

print('\narand_test with arguments')
netinf.arand_test(theta[dimension], dimension=dimension, num_clusters=5, seed=None, verbose=False)

print('\npval_arand')
print(netinf.arand_test_result)

print('\ntstat_arand')
print(netinf.arand_test_stat)

print('\narand_ci table')
netinf.arand_ci(theta[dimension]-2, theta[dimension]+2, dimension=dimension)

print('\narand_ci table with arguments')
netinf.arand_ci(theta[dimension]-2, theta[dimension]+2, dimension=None, grid_size=151, coverage=0.95, \
            num_clusters=5, decimals=1, seed=None, verbose=False)

print('\nci_arand')
print(netinf.arand_ci_result)

print('\ncluster_se table')
netinf.cluster_se()

print('\ncluster_se table with arguments')
netinf.cluster_se(num_clusters=30, decimals=1, verbose=False)

print('\nvar_cluster')
print(netinf.cluster_se_vcov)

print('\nse_cluster')
print(netinf.cluster_se_result)

