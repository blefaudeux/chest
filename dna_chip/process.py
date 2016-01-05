import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import fastcluster as fc
import scipy.cluster.hierarchy as sch
from scipy.cluster.hierarchy import dendrogram, set_link_color_palette


def log_mean(log_values):
    exp_values = np.exp2(log_values)
    return np.log2(np.mean(exp_values))


def fold_change(values):
    pass

# Some settings
plot_fulldata = False
plot_dendrogram = False
plot_clusters = True
n_clusters = 50
expression_change_threshold = 0.05  # We pick the 5% of the genes which move the most
folded_change_threshold =  0.25
exp_names = ['WT_6h', 'KO_0h', 'KO_6h', 'WT_0h', 'WT_1h', 'WT_2h']      # Used to compute triplicates
exp_sorted = ['WT_0h', 'WT_1h', 'WT_2h', 'WT_6h', 'KO_0h', 'KO_6h']     # Used to sort experiments in a meaningful way
filename = "marie.mc.group.limma.txt"

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


def fold_change_threshold(val):
    # - turn change into binary
    return max(min(int(val*4), 1), -1)

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

cluster_collumns = ['FC_WT_1', 'FC_WT_2', 'FC_WT_6', 'FC_KO_0', 'FC_KO_6']

# - run the hierarchical clustering
clust_total = fc.linkage(clipped_data[cluster_collumns], method=method, metric=metric)

# - crop dendrogram to n clusters, all of them are available if needed
short_clust = sch.fcluster(clust_total, n_clusters, criterion='maxclust')

if plot_dendrogram:
    dendrogram(clust_total, p=n_clusters)
    plt.show()

# - get back to Panda
clipped_data["k_index"] = pd.Series(short_clust, index=clipped_data[exp_sorted].index)

# - Get some plots to check that we got something interesting
if plot_clusters:
    for cluster in range(n_clusters):
        subset = clipped_data[clipped_data['k_index'] == cluster + 1]

        for i in range(len(subset['GeneName'].values)):
            plt.plot(subset[exp_sorted].values[i, :], label=subset['GeneName'].values[i])
        plt.legend()
        plt.xticks(np.arange(len(exp_sorted)), exp_sorted, rotation=25)
        plt.show()
