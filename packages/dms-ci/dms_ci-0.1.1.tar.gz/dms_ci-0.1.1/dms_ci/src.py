import pandas as pd
import numpy as np
import os
import statsmodels.api as sm
import plotly.express as px

N_TRIAL_PER_DATASET = 10000
SIZE_SAMPLE = [500, 1000, 2000, 3000, 5000, 10000, 20000, 50000]
DATAPATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
FIGPATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'figs'))

def bootstrap(sample, n=1000):
    """
    Bootstrap the sample
    """
    n, r = sample.shape
    res = np.zeros((n, r))
    for i in range(n):
        res[i] = sample[np.random.randint(0, n, n)].sum(axis=0)
    return res

def predict_confidence_interval_bootstrap(sample, bootstrap_iterations=1000):
    bs = bootstrap(sample, n=bootstrap_iterations)
    lower_bound, upper_bound = np.percentile(bs, [2.5, 97.5], axis=0)/bs.shape[0]
    return lower_bound, upper_bound
    
    
def process_data(data):
    data = data.to_numpy(dtype=np.byte).astype(float)
    data[data == 0] = 0
    data[data < 0] = 128
    data[data < 64] = 0
    data[data > 0] = 1
    return data

def predict_confidence_interval_binomial_distribution(observed_freq, size_sample):
    """
    Predict the confidence interval using the binomial distribution
    """
    lower_bound = observed_freq - 1.96*np.sqrt(observed_freq*(1-observed_freq)/size_sample)
    upper_bound = observed_freq + 1.96*np.sqrt(observed_freq*(1-observed_freq)/size_sample)
    return lower_bound, upper_bound
    
    
def wilson(p, n, z = 1.96, bias_correction=0):
    
    p = np.array(p) + bias_correction
    denominator = 1 + z**2/n
    centre_adjusted_probability = p + z*z / (2*n)
    adjusted_standard_deviation = np.sqrt((p*(1 - p) + z*z / (4*n)) / n)
    
    lower_bound = (centre_adjusted_probability -  z*adjusted_standard_deviation) / denominator
    upper_bound = (centre_adjusted_probability + z*adjusted_standard_deviation) / denominator
    return (lower_bound, upper_bound)

def clopper_pearson(*args):
    return sm.stats.proportion_confint(*args, method='beta', alpha=0.05)

def agresti_coull(*args):
    return sm.stats.proportion_confint(*args, method='agresti_coull', alpha=0.05)


def predict_confidence_interval_poisson(observed_freq, size_sample, alpha=0.05):
    cov = size_sample
    mut = observed_freq*size_sample
    return 0.5*scipy.stats.chi2.ppf(alpha/2, df=2*mut)/cov, 0.5*scipy.stats.chi2.ppf(1-alpha/2, df=2*(mut+1))/cov

def failure_to_success(arr):
    return [100 - m for m in arr]

def compare_methods():
    
    n_trials_per_dataset = N_TRIAL_PER_DATASET
    bootstrap_iterations = 10
    methods = ['bootstrap', 'binomial', 'wilson', 'clopper_pearson', 'agresti_coull', 'poisson']
    size_samples = SIZE_SAMPLE

    failures_df = pd.DataFrame()
    size_df = pd.DataFrame()

    for size_sample in size_samples:
        failures = {m:[] for m in methods}
        size_ci = {m:[] for m in methods}
        sub_rate_vector = []
        failures_vector =  {m:[] for m in methods}
        
        for f in os.listdir(DATAPATH):
            
            # read dataset
            data = process_data(pd.read_orc(os.path.join(DATAPATH, f)))
            true_mutation_rate = data.sum(axis=0)/data.shape[0]

            fail = {m:[] for m in methods}
            size = {m:[] for m in methods}
            
            for _ in range(n_trials_per_dataset):
                
                # generate a new sample
                sample = data[np.random.randint(0, data.shape[0], size=size_sample)]
                observed_freq = sample.sum(axis=0)/size_sample
                sub_rate_vector.append(true_mutation_rate)
                
                # count failures bootstrap
               # lb_bs, ub_bs = predict_confidence_interval_bootstrap(sample, bootstrap_iterations=bootstrap_iterations)
               # fail['bootstrap'].append(100*np.logical_or(ub_bs < true_mutation_rate, lb_bs > true_mutation_rate).sum()/data.shape[1])
              #  size['bootstrap'].append(np.mean(ub_bs - lb_bs))
              #  failures_vector['bootstrap'].append(np.logical_or(ub_bs < true_mutation_rate, lb_bs > true_mutation_rate))
                
                # count failures binomial
                lb_bin, ub_bin = predict_confidence_interval_binomial_distribution(observed_freq, size_sample)
                fail['binomial'].append(100*np.logical_or(ub_bin < true_mutation_rate, lb_bin > true_mutation_rate).sum()/data.shape[1])
                size['binomial'].append(np.mean(ub_bin - lb_bin))
                failures_vector['binomial'].append(np.logical_or(ub_bin < true_mutation_rate, lb_bin > true_mutation_rate))
                
                # count Wilson failures
                lb_wilson, ub_wilson = wilson(observed_freq, size_sample)
                fail['wilson'].append(100*np.logical_or(ub_wilson < true_mutation_rate, lb_wilson > true_mutation_rate).sum()/data.shape[1])
                size['wilson'].append(np.mean(ub_wilson - lb_wilson))
                failures_vector['wilson'].append(np.logical_or(ub_wilson < true_mutation_rate, lb_wilson > true_mutation_rate))
                
                # count Clopper-Pearson failures
                lb_cp, ub_cp = clopper_pearson(observed_freq*size_sample, size_sample)
                fail['clopper_pearson'].append(100*np.logical_or(ub_cp < true_mutation_rate, lb_cp > true_mutation_rate).sum()/data.shape[1])
                size['clopper_pearson'].append(np.mean(ub_cp - lb_cp))
                failures_vector['clopper_pearson'].append(np.logical_or(ub_cp < true_mutation_rate, lb_cp > true_mutation_rate))
                
                # count Agresti-Coull failures
                lb_ac, ub_ac = agresti_coull(observed_freq*size_sample, size_sample)
                fail['agresti_coull'].append(100*np.logical_or(ub_ac < true_mutation_rate, lb_ac > true_mutation_rate).sum()/data.shape[1])
                size['agresti_coull'].append(np.mean(ub_ac - lb_ac))
                failures_vector['agresti_coull'].append(np.logical_or(ub_ac < true_mutation_rate, lb_ac > true_mutation_rate))
                
                # count Poisson failures
                lb_poisson, ub_poisson = predict_confidence_interval_poisson(observed_freq, size_sample)
                fail['poisson'].append(100*np.logical_or(ub_poisson < true_mutation_rate, lb_poisson > true_mutation_rate).sum()/data.shape[1])
                size['poisson'].append(np.mean(ub_poisson - lb_poisson))
                failures_vector['poisson'].append(np.logical_or(ub_poisson < true_mutation_rate, lb_poisson > true_mutation_rate))

            for m in methods:
                failures[m].append(fail[m])
                size_ci[m].append(size[m])
            #    print(f'{n_dataset}: {m}: {np.mean(failures[m][-1])}% failure rate')
            #print('----------------------------------------------------------')
        
        df = pd.DataFrame(
            {
                'Bootstrap': failure_to_success(np.array(failures['binomial']).flatten()), 
                #'Binomial': np.array(failures['binomial']).flatten(), 
                'Wilson': failure_to_success(np.array(failures['wilson']).flatten()),
                'Clopper-Pearson': failure_to_success(np.array(failures['clopper_pearson']).flatten()),
                'Agresti-Coull': failure_to_success(np.array(failures['agresti_coull']).flatten()),
                'Poisson': failure_to_success(np.array(failures['poisson']).flatten()),
                'size_sample': size_sample,
            })

        failures_df = pd.concat([failures_df, df], axis=0)

        df = pd.DataFrame(
            {
                'Bootstrap': np.array(size_ci['binomial']).flatten(), 
                #'Binomial': np.array(size_ci['binomial']).flatten(), 
                'Wilson': np.array(size_ci['wilson']).flatten(),
                'Clopper-Pearson': np.array(size_ci['clopper_pearson']).flatten(),
                'Agresti-Coull': np.array(size_ci['agresti_coull']).flatten(),
                'Poisson': np.array(size_ci['poisson']).flatten(),
                'size_sample': size_sample        
            })
        size_df = pd.concat([size_df, df], axis=0)
        
    fig = px.box(failures_df, y=[c for c in df.columns if c != 'size_sample'], color='size_sample', title='Success rate of the confidence interval methods. # of runs: {}. L = 170.'.format(3*n_trials_per_dataset * len(os.listdir(DATAPATH))))
    fig.update_yaxes(title_text="Success rate (%)")
    fig.update_xaxes(title_text="Method")    
    fig.update_traces(boxpoints=False) 
    #   add a horizontal line at y=5 all the way across the figure legend y=5 
    fig.add_shape(type="line", x0=0, y0=95, x1=1, y1=95, line=dict(color="Green", width=2, dash="dash"), xref="paper", yref="y")
    # label that line "95%"
    fig.add_annotation(x=-0.03, y=95, text="95%", showarrow=False, xref="paper", yref="y")
    fig.show()
    
    # a = fig.to_html()
    # with open(os.path.join(FIGPATH, 'compare_models.html'), 'w') as f:
    #     f.write(a)
        
    a = fig.to_image(format='png')
    with open(os.path.join(FIGPATH, 'compare_models.png'), 'wb') as f:
        f.write(a)
    # save to file
    
        
    # fig = px.box(size_df, y=[c for c in df.columns if c != 'size_sample'], color='size_sample', title='Size of the confidence interval methods. n_bootstrap = {}, n_iter = {} iterations *{} datasets'.format(bootstrap_iterations, n_trials_per_dataset, len(os.listdir('../../bv'))))
    # fig.update_yaxes(title_text="Size of the CI")
    # fig.update_xaxes(title_text="Method")
    # fig.show()

    # # save to file
    # util.save_plotly_fig(ipynbname.path(), '[B] Size of the confidence interval methods', fig)

    
def how_to_pick_N():
    P = np.arange(0, 0.11, 0.01)
    df = pd.DataFrame(columns=SIZE_SAMPLE, index = P)
    for n in SIZE_SAMPLE:
        for p in P:
            df.loc[p, n] = wilson(p, n, bias_correction=1E-3)[1] - wilson(p, n, bias_correction=1E-3)[0]
    
    fig = px.line(df, x=P, y=SIZE_SAMPLE, title='How to pick N?', labels={'x': 'Mutation rate', 'y': 'Size of the CI'})

    fig.update_layout(
        title = 'Select N to get a CI of a given size',
        xaxis_title = 'Mutation rate',
        yaxis_title = 'Size of the CI',
        legend_title = 'N := number of reads',
    )
    
    fig.update_xaxes(title_text="Mutation rate")
    
    # a = fig.to_html()
    # with open(os.path.join(FIGPATH, 'how_to_pick_N.html'), 'w') as f:
    #     f.write(a)    
        
    a = fig.to_image(format="png", engine="kaleido")
    with open(os.path.join(FIGPATH, 'how_to_pick_N.png'), 'wb') as f:
        f.write(a)
        

def plot_mr_distribution():
    mr = []
    for f in os.listdir(DATAPATH):
        data = process_data(pd.read_orc(os.path.join(DATAPATH, f)))
        mr += (data.sum(axis=0)/data.shape[0]).tolist()
        
    fig = px.histogram(pd.DataFrame({'mr': mr}), x='mr', nbins=100, title='Distribution of the mutation rate in the dataset')
    
    fig.update_layout(
        title = 'Distribution of the mutation rate in the dataset',
        xaxis_title = 'Mutation rate',
        yaxis_title = 'Count',
    )
    
    
    # a = fig.to_html()
    # with open(os.path.join(FIGPATH, 'mr_distribution.html'), 'w') as f:
    #     f.write(a)
        
    a = fig.to_image(format="png", engine="kaleido")
    with open(os.path.join(FIGPATH, 'mr_distribution.png'), 'wb') as f:
        f.write(a)
        

def generate_plots():
    plot_mr_distribution()
    compare_methods()
    how_to_pick_N()
    
if __name__ == '__main__':
    generate_plots()