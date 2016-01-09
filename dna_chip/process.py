import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import fastcluster as fc
import scipy.cluster.hierarchy as sch
from scipy.cluster.hierarchy import dendrogram, set_link_color_palette

# Some settings
gene_of_interest = 'Lgr5'

plot_fulldata = False
plot_dendrogram = False
plot_clusters = False
plot_gene_of_interest_cluster = True
plot_anti_correlated_cluster = True

n_clusters = 20
expression_change_threshold = 0.1  # We pick the 5% of the genes which move the most
folded_change_threshold = 0.25
exp_names = ['WT_6h', 'KO_0h', 'KO_6h', 'WT_0h', 'WT_1h', 'WT_2h']      # Used to compute triplicates, file order
exp_sorted = ['WT_0h', 'WT_1h', 'WT_2h', 'WT_6h', 'KO_0h', 'KO_6h']     # Used to sort experiments in a meaningful way
filename = "marie.mc.group.limma.txt"

# Helper functions


def log_mean(log_values):
    exp_values = np.exp2(log_values)
    return np.log2(np.mean(exp_values))


def get_cluster_data(cluster_id, data):
    # Get a slice of the array corresponding to a given cluster
    # You can use a gene name (cluster that this gene belongs to), or a cluster number
    if isinstance(cluster_id, str):
        i_cluster = data[data['GeneName'] == cluster_id]['k_index'].values[0]
        return data[data['k_index'] == i_cluster]

    return data[data['k_index'] == cluster_id]


def fold_change_threshold(val):
    # - turn change into binary
    return max(min(int(val/folded_change_threshold), 1), -1)


def plot_cluster(_cluster_data, title=None):
    for _i in range(len(_cluster_data['GeneName'].values)):
        plt.plot(_cluster_data[exp_sorted].values[_i, :], label=_cluster_data['GeneName'].values[_i])
    plt.legend()
    plt.xticks(np.arange(len(exp_sorted)), exp_sorted, rotation=25)
    plt.grid(True)
    if title:
        plt.title(title)
    plt.show()


def cluster_correlation(cluster1, cluster2):
    first_cluster_val = cluster1[cluster_columns].median().values
    second_cluster_val = cluster2[cluster_columns].median().values
    return np.correlate(first_cluster_val, second_cluster_val)

# ----------------------------------------------------------
# Load the file into an array, can be indexed by names
raw_data = pd.read_table(filename)
print("File {} loaded. \nAvailable fields are : {}\n".format(filename, raw_data.columns))

# You can access the columns directly using the label, or using the name as a field
# ex : raw_data['GeneName'], or raw_data.GeneName

# Get a list of the actual measurement indexes :
experiments = raw_data.columns[1:19]
print("Selecting {} to work with. \n".format(experiments))

# Evaluate the sample evolution over time :
# - STD for every gene expression :
standard_dev = raw_data[experiments].std(1)
raw_data['STD'] = standard_dev
print("Standard deviation analysis : {}".format(raw_data['STD'].describe()))

# - threshold the genes we'll use : automatic threshold for now
threshold = raw_data['STD'].quantile(1 - expression_change_threshold)
clipped_data = raw_data[raw_data['STD'] > threshold]
clipped_data = clipped_data.dropna()  # We also get rid of all the rows with missing data

# - compute the triplicate means by 3 columns :
n_real_experiments = int(len(experiments)/3)

for i in range(n_real_experiments):
    col_start = 1+3*i
    col_end = col_start+3
    clipped_data[exp_names[i]] = clipped_data.iloc[:, col_start:col_end].apply(log_mean, axis=1)

# Plot those values over time for a start
if plot_fulldata:
    clipped_data[exp_sorted].T.plot()
    plt.show()

# ---------------------------------------------------------
# Compute a normalized change metric
# - compute relative change over time
clipped_data['FC_WT_1'] = clipped_data['WT_1h'] - clipped_data['WT_0h']
clipped_data['FC_WT_2'] = clipped_data['WT_2h'] - clipped_data['WT_1h']
clipped_data['FC_WT_6'] = clipped_data['WT_6h'] - clipped_data['WT_2h']

clipped_data['FC_KO_0'] = clipped_data['KO_0h'] - clipped_data['WT_0h']
clipped_data['FC_KO_6'] = clipped_data['KO_6h'] - clipped_data['KO_0h']

# - threshold change
clipped_data['FC_WT_1'] = clipped_data['FC_WT_1'].apply(fold_change_threshold)
clipped_data['FC_WT_2'] = clipped_data['FC_WT_2'].apply(fold_change_threshold)
clipped_data['FC_WT_6'] = clipped_data['FC_WT_6'].apply(fold_change_threshold)
clipped_data['FC_KO_0'] = clipped_data['FC_KO_0'].apply(fold_change_threshold)
clipped_data['FC_KO_6'] = clipped_data['FC_KO_6'].apply(fold_change_threshold)

# - accumulate change over time
clipped_data['FC_WT_2'] = clipped_data['FC_WT_1'] + clipped_data['FC_WT_2']
clipped_data['FC_WT_6'] = clipped_data['FC_WT_2'] + clipped_data['FC_WT_6']
clipped_data['FC_KO_6'] = clipped_data['FC_KO_0'] + clipped_data['FC_KO_6']

# ----------------------------------------------------------
# Try to cluster the data :
# - define clustering method and metric
method = 'complete'
metric = 'euclidean'  # metric: define here

cluster_columns = ['FC_WT_1', 'FC_WT_2', 'FC_WT_6', 'FC_KO_0', 'FC_KO_6']

# - run the hierarchical clustering, then crop to n clusters
cluster_total = fc.linkage(clipped_data[cluster_columns], method=method, metric=metric)
cluster_shortened = sch.fcluster(cluster_total, n_clusters, criterion='maxclust')

if plot_dendrogram:
    dendrogram(cluster_total, p=n_clusters)
    plt.show()

# - get back to Panda
clipped_data["k_index"] = pd.Series(cluster_shortened, index=clipped_data[exp_sorted].index)

# - Get some plots to check that we got something interesting
if plot_clusters:
    for cluster in range(n_clusters):
        subset = clipped_data[clipped_data['k_index'] == cluster + 1]
        plot_cluster(subset)

# ----------------------------------------------------------
# - Find Gene of interest companions
lookalikes = get_cluster_data(gene_of_interest, clipped_data)

if plot_gene_of_interest_cluster:
    plot_cluster(lookalikes, "Cluster corresponding to " + gene_of_interest)

# - Find anti-correlated cluster
worse_correlation = 0
anti_correlated_cluster = None

for index in clipped_data['k_index'].values:
    cluster_data = get_cluster_data(index, clipped_data)
    correlation = cluster_correlation(cluster_data, lookalikes)

    if correlation < worse_correlation:
        worse_correlation = correlation
        anti_correlated_cluster = cluster_data

if anti_correlated_cluster is not None and plot_anti_correlated_cluster:
    plot_cluster(anti_correlated_cluster, "Anti correlated cluster to " + gene_of_interest)
