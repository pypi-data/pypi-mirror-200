import numpy as np
from sklearn.neighbors import NearestNeighbors, KDTree
from scipy.special import digamma, gamma
from scipy.stats import multivariate_normal as mv
from numpy.random import choice
import sympy

#%%
def NMI(tpl, measure = 'divergence', k=50, info='nats', epsilon='adapt', reverse='True'):
    
    """
    Estimation of (multivariate) Kullback-Leibler divergence 
    estimation via nearest neighbor ratios. The algorithm was proposen 
    in Noshad, M. et al. (2017). Direct estimation of information divergence
    using nearest neighbor ratios. In 2017 IEEE International Symposium
    on Information Theory (ISIT 2017)", pages 903 – 907, Aachen, Germany.
    Institute of Electrical and Electronics Engineers ( IEEE ).
    """

    
    X = np.array(tpl[0])
    Y = np.array(tpl[1])

    # f-Divergence D(p|q)=Kullb.-Leibler Div. KLD(q|p) when f=-log
    # to compute KLD(p|q) use reverse==True
    if reverse:
        Z = X.copy()
        X = Y.copy()
        Y = Z
    
    if X.ndim == 1:
        X = X.reshape(-1,1)
    if Y.ndim == 1:
        Y = Y.reshape(-1,1)        
    
    if measure== 'divergence':
        p = X
        q = Y
    
    else:
        #shuffle data such that dependencies disappear
        Y_per = Y.copy()
        np.random.shuffle(Y_per)
        p = np.hstack((X,Y))
        q = np.hstack((X,Y_per))
    
   
    n = len(p)
    m = len(q)


    # flexible number of neighbors according to sample size 
    # suggested in paper: big-O(sqrt(m)) 
    if k == 'adapt':
        k = 3*int(np.sqrt(m))
    
    both = np.concatenate((q,p))
    # shuffle data such that neighbors of both distributions are considered
    # in case of doublets
    permut = choice(n+m,n+m,replace = False)
    both[permut]
    label = np.concatenate((np.ones(m), np.zeros(n)))
    label = label[permut]

    nbrs = NearestNeighbors(n_neighbors=k).fit(both)
    indices = nbrs.kneighbors(q, return_distance=False)

    # count Y-neighbors of (Y_i)s
    M = np.sum(label[indices], axis=1)
    N = k - M
    
    ratio = N/(M + 1)
    if epsilon=='adapt':
        epsilon = 1/(m*p.shape[1])
    
    # here, we use max(ratio) instead of max(f(ratio)) as max(-log(0))=inf
    ratio = np.max((ratio, epsilon*np.ones(len(ratio))), axis=0)
    
    if info=='nats':
        res = np.mean(-np.log(ratio))
    else:
        res = np.mean(-np.log2(ratio))
    
    return max(res,0.)


#%%

def BannMI(tpl, measure = 'MI', k = 15, info='nats', prior='empiric'):
    
    """
    Bayesian nearest neighbor ratio estimation for mutual information
    and Kullback-Leibler divergences, as proposed in
    Schmidt et al., 2023, soon to come...
    In particular, we recommend BannMI for dependency analysis 
    of phosphoproteomic data (protein-protein-interactions)
    The algorithm was inspired by NMI (see function)
    """
    
    X = np.array(tpl[0])
    Y = np.array(tpl[1])
    
    if X.ndim == 1:
        X = X.reshape(-1,1)
    if Y.ndim == 1:
        Y = Y.reshape(-1,1)

    if measure=='divergence':
        p = X
        q = Y
    
    else:
        #shuffle data such that dependencies disappear
        Y_per = Y.copy()
        np.random.shuffle(Y_per)
        p = np.hstack((X,Y))
        q = np.hstack((X,Y_per))
    
    n = p.shape[0]
    n2 = 2*n


    both = np.concatenate((p, q))
    # shuffle data such that neighbors are mixed in case of identical values
    permut = choice(n2,n2,replace = False)
    both[permut]
   
    
    label = np.concatenate((np.zeros(n), np.ones(n)))
    label[permut]
    nbrs = NearestNeighbors(n_neighbors=k).fit(both)
    indices = nbrs.kneighbors(p, return_distance=False)

    q_neighbors = np.sum(label[indices], axis=1)
    c = k - q_neighbors

    # case: distributions are identical (t_var==0)
    t_var = np.nanvar((c/k))
    if not t_var:
        return 0.
    
    if prior=='empiric':
        t_mu = np.nanmean((c/k))
        # hyperparameters
        b = np.array((t_mu-t_mu**2-t_var)*(1-t_mu)/t_var)
        a = np.array(b*t_mu/(1-t_mu))
        
        # case for < 1 prior beta is convex
        b[b<1]=1
        a[a<1]=1        
        
    else:
        b = prior
        a = prior

    a_new = a + c
    b_new = b + k - c

    theta = (a_new)/(a_new + b_new) 
    ratio = theta/(1-theta)
    
    if info == 'bits':
        res = np.mean(np.log2(ratio))
    else:
        res = np.mean(np.log(ratio))    
    
    return max(res, 0.)


#%%
    
def WMI(tpl, measure = 'divergence', k = 5, info='nats', epsilon=False):
    
    """
    Erstimation of (multivariate) differential Kullback-Leibler Divergence
    via nearest neighbor distances as proposed in 
    Wang, Q. et al. (2009). Divergence Estimation for Multidimensional
    Densities Via k-Nearest-Neighbor Distances. IEEE Transactions of
    Information Theory, 55(5), 2392–2405.
    here, epsilon parameter is introduced to adjust for distance 0.
    if measure is not 'divergence', WMI computes mutual information between 
    tpl[0] and tpl[1]
    
    """
    
    X = np.array(tpl[0])
    Y = np.array(tpl[1])
    
    if X.ndim == 1:
        X = X.reshape(-1,1)
    if Y.ndim == 1:
        Y = Y.reshape(-1,1)

    if measure == 'divergence':
        p = X
        q = Y
    
    else: 
        Y_per = Y.copy()
        np.random.shuffle(Y_per)
        p = np.hstack((X,Y))
        q = np.hstack((X,Y_per))
        
    n = p.shape[0]
    d = p.shape[1] 

        
    Xnbrs = NearestNeighbors(n_neighbors= k + 1).fit(p)
    Ynbrs = NearestNeighbors(n_neighbors= k).fit(q)
    Xdistances, indices = Xnbrs.kneighbors(p, return_distance=True)
    Ydistances, indices = Ynbrs.kneighbors(p, return_distance=True)
    xdist = Xdistances[:,k]
    ydist = Ydistances[:,k-1]
    
    if epsilon:
        xdist[xdist==0]=epsilon
        ydist[ydist==0]=epsilon
            
    px = k/(xdist**d*(n-1))
    py = k/(ydist**d*n)
    
    if info == 'bits':
        res = np.mean(np.log2(px/py))
    else: 
        res = np.mean(np.log(px/py))
           
    return max(res, 0.)

#%%

def KSG(tpl, k = 2):

    """
    function sklearn.feature_selection.mutual_info_regression 
    https://github.com/scikit-learn/scikit-learn/blob/main/doc/modules/feature_selection.rst
    adjusted for multivariate variables. Algorithm was proposed in
    Kraskov, A. et al. (2004). Estimating mutual information. Phys. Rev. E,
69, 066138.
    """

    x = tpl[0]
    y = tpl[1]
    n_samples = x.shape[0]

    if x.ndim == 1:
        x = x.reshape((-1, 1))
    if y.ndim == 1: 
        y = y.reshape((-1, 1))
    xy = np.hstack((x, y))
    permut = choice(n_samples,n_samples,replace = False)
    xy[permut]

    # Here we rely on NearestNeighbors to select the fastest algorithm.
    nn = NearestNeighbors(metric="chebyshev", n_neighbors=k)

    nn.fit(xy)
    radius = nn.kneighbors()[0]
    radius = np.nextafter(radius[:, -1], 0)

    # KDTree is explicitly fit to allow for the querying of number of
    # neighbors within a specified radius
    kd = KDTree(x, metric="chebyshev")
    nx = kd.query_radius(x, radius, count_only=True, return_distance=False)
    nx = np.array(nx) - 1.0

    kd = KDTree(y, metric="chebyshev")
    ny = kd.query_radius(y, radius, count_only=True, return_distance=False)
    ny = np.array(ny) - 1.0

    mi = (digamma(n_samples) + digamma(k)
        - np.mean(digamma(nx + 1))
        - np.mean(digamma(ny + 1))
    )

    return max(0, mi)




#%%

def entropy(X, k=1, info = 'nats'): 
    
    """
    nearest neighbor estimation of differential entropy as proposed in
    Kozachenko, L. and Leonenko, N. (1987). Sample Estimate of the Entropy
    of a Random Vector. Problems of Information Transmission, 23(2),
    95–101.
    """
    
    X = np.array(X)
    gam = sympy.EulerGamma.evalf()

    
    if X.ndim == 1:
        X = X.reshape(-1,1)
        
     
    n = X.shape[0]
    d = X.shape[1] 

        
    Xnbrs = NearestNeighbors(n_neighbors= k + 1).fit(X)
    Xdistances, indices = Xnbrs.kneighbors(X, return_distance=True)
    xdist = Xdistances[:,k]
    v = np.exp(np.array([gam], dtype = float))[0]
    px = (k*gamma(d/2+1))/(xdist**d*(n-1)*v*np.pi**(d/2))
    
    if info == 'bits':
        res = np.mean(np.log2(px))
    else:
        res = np.mean(np.log(px))
           
    return max(-res, 0.)
    

#%%

def KLD_gaussian(tpl=False, mu0=False, mu1=False, 
                 cov0=False, cov1=False, samples=True, density_estimate=False):
    
    """
    compute Kullback Leibler Divergence on Gaussians
    either estimate Gaussian parameters based on samples 
    or input parameters
    in the latter case, result is analytical
    """
    
    if samples:
        X = tpl[0]
        Y = tpl[1]
        if X.ndim == 1:
            k=1
        else:
            k = X.shape[1]
        mu0 = np.mean(X, axis=0)
        mu1 = np.mean(Y, axis=0)
        cov0 = np.cov(X, rowvar=False)
        cov1 = np.cov(Y, rowvar=False)


    if density_estimate:
        px = mv.pdf(X, mean=mu0, cov=cov0)
        py = mv.pdf(X, mean=mu1, cov=cov1)
        
        return np.nanmean(np.log(px/py))

    
    if np.isscalar(mu0) or len(mu0)==1:
        x = 0.5*((cov0/cov1)**2+(mu1-mu0)**2/cov1**2-1+2*np.log(cov1/cov0))
        if not np.isscalar(x):
            x = x[0]
        return x

    else:
        k = len(mu0)
        part1 = np.trace(np.linalg.inv(cov1) @ cov0)
        
        part2 = (mu1 - mu0).reshape((-1, k)) @ np.linalg.inv(cov1) @ (mu1 - mu0) - k
        
        if np.isnan(np.linalg.det(cov1)/np.linalg.det(cov0)):
            return np.nan
            
        else: 
            part3 = np.log(np.linalg.det(cov1)/np.linalg.det(cov0))
       
        return max((0.5*(part1 + part2 + part3)[0]), 0)
    

def KLD_gamma(tpl=False, a0=False, a1=False, b0=False, b1=False, samples=True):
    
    """
    compute Kullback Leibler Divergence on Gamma distributions.
    parameters are a=alpha (shape), b=beta (rate)
    either estimate parameters based on samples 
    or input parameters
    in the latter case, result is analytical
    """
    
    if samples:
        X = tpl[0]
        Y = tpl[1]
        
        mu = np.mean(X), np.mean(Y)
        var = np.var(X), np.var(Y)
        
        a0 = mu[0]**2/var[0]
        a1 = mu[1]**2/var[1]
        b0 = mu[0]/var[0]
        b1 = mu[1]/var[1]
    
    part1 = (a0-a1)*digamma(a0) - np.log(gamma(a0)) + np.log(gamma(a1))
    part2 = a1*(np.log(b0)-np.log(b1)) + a0*((b1-b0)/b0)
    res = part1 + part2
    return max(res,0)
    
