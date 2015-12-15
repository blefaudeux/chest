import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import fastcluster as fc
import scipy.cluster.hierarchy as sch
from scipy.cluster.hierarchy import dendrogram, set_link_color_palette

def log_mean(logval):
    expval = np.exp2(logval)
    return np.log2(np.mean(expval))

# ----------------------------------------------------------
# Load the file into an array, can be indexed by names
filename = "marie.mc.group.limma.txt"
raw_data = pd.read_table(filename)

# Available indexes :
print("File {} loaded. \n Available fields are : {}\n".format(filename, raw_data.columns))

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
threshold = raw_data['STD'].quantile(0.95)  # WE pick the 5% of the genes which move the most
clipped_data = raw_data[raw_data['STD'] > threshold]
clipped_data = clipped_data.dropna()  # We also get rid of all the rows with missing data

# - compute the triplicat means by 3 columns :
avg_experiments = []
n_real_experiments = int(len(experiments)/3)

for col in range(n_real_experiments):
    new_name = "Aggregate_" + experiments[3 * col].split('_')[1]
    new_name += "__" + experiments[3 * col + 1].split('_')[1]
    new_name += "__" + experiments[3 * col + 2].split('_')[1]
    avg_experiments.append(new_name)

    col_start = 1+3*col
    col_end = col_start+3

    clipped_data[new_name] = clipped_data.iloc[:, col_start:col_end].apply(log_mean, axis=1)

# Plot those values over time for a start
# clipped_data[avg_experiments].T.plot()
# plt.show()

# ----------------------------------------------------------
# Try to cluster the data :
n_clusters = 20

# - define clustering method and metric
method = 'complete'
metric = 'euclidean'  # metric: define here

# - run the hierarchical clustering
clust_total = fc.linkage(clipped_data[avg_experiments], method=method, metric=metric)

# - crop dendrogram to n clusters, all of them are available if needed
short_clust = sch.fcluster(clust_total, n_clusters, criterion='maxclust')
dendrogram(clust_total)
plt.show()

# - get back to Panda
clipped_data["k_index"] = pd.Series(short_clust, index=clipped_data[avg_experiments].index)

# - Get some plots to check that we got something interesting
groups = clipped_data.groupby('k_index')
groups[avg_experiments].plot()
plt.show()