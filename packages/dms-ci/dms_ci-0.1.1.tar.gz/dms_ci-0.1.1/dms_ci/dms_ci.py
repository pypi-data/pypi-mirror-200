from .src import wilson

def dms_ci(p, n, z = 1.96, sub_error=1E-3):
    """Provides confidence intervals for DMS-MaPseq data.

    Parameters
    ----------

    N : array_like
        Number of reads for each position.

    n : array_like
        Number of mutations for each position.

    alpha : float, optional
        Significance level of the confidence interval. Default is 0.05.
        
    sub_error: float, optional
        Probability of having a substitution error in the sequencing. Used to unbias the CI. Default is 1E-3. Read the README for more details.

    Returns
    -------

    low : array_like
        Lower confidence interval.

    high : array_like
        Upper confidence interval.

    Notes
    -----

    The confidence intervals are calculated using the Wilson score interval with a bias correction. 
    """
    
    return wilson(p, n, z, sub_error)
    
