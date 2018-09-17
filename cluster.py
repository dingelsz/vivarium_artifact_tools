import pandas as pd
import numpy as np

from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.cluster import AgglomerativeClustering, DBSCAN, KMeans

import matplotlib.pyplot as plt
# %matplotlib inline

folder = '/Volumes/IHME/projects/artifact_tool/'
table_name = 'table.csv'
plot_name = 'cluster'

# Load the table and clean the data
table = pd.read_csv(folder + table_name)
countries = table.columns.tolist()[1:]
table.columns = ["Features"] + countries
countries = table.columns.tolist()[1:]
features = table.Features.tolist()
table.index = table.Features
table = table.drop(columns=['Features'])

# Since our populations vary so much take the log of each feature that
# uses population
table.loc['population'] = np.log(table.loc['population'])
table.loc['population under 5'] = np.log(table.loc['population under 5'])

# Standardize the data
data = table.transpose().values[0:]
data = preprocessing.scale(data)

# Reduce the number of dimensions with TSNE.
n_comp = 2
perplexity = 8
tsne = TSNE(n_components=n_comp, perplexity=perplexity)
data_cluster = tsne.fit_transform(X=data)

# Standardize the output of the reduced data
data_cluster = preprocessing.scale(data_cluster)

# Cluser using an agglormerative method
n_clusters = 7
model = AgglomerativeClustering(n_clusters=n_clusters)
model.fit(data_cluster)
clusters = model.labels_

# Save images of the clustering
plt.figure(1)
x_component = 0
y_component = 1
plt.scatter(data_cluster[:,x_component], data_cluster[:,y_component], c=clusters)
for i in range(len(countries)):
    plt.annotate('  '+str(i), (data_cluster[:,x_component][i], data_cluster[:,y_component][i]), va='center')
plt.savefig(folder + plot_name + '.png', bbox_inches='tight', dpi=200)

plt.figure(2)
cluster_table = pd.DataFrame( list(zip(clusters, countries)), columns = ['cluster', 'country'] ).sort_values(by=['cluster'])
cluster_table = cluster_table.reset_index().drop(columns = ['index'])
plt.pcolor([[c] for c in cluster_table.cluster.values])
for index, (cluster, country) in cluster_table.iterrows():
    plt.annotate('  '+str(cluster_table.country.loc[index]) + ' (' +str(countries.index(country)) + ')', (1, index + 0.5), va='center')
plt.savefig(folder + plot_name + '_table.png', bbox_inches='tight', dpi=200)
