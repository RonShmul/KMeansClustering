import pandas as pd
import numpy as np
#import matplotlib as plt
import matplotlib.pyplot as plt
from scipy.stats import mode
from PIL import Image
import plotly.plotly as py
from sklearn.cluster import KMeans


class Cluster:
    df = pd.DataFrame({})
    kMean=pd.DataFrame({})
    scatterPlot=None

    def __init__(self, data_frame, num_of_clusters, num_of_runs):
        self.df = data_frame
        self.num_of_clusters = num_of_clusters
        self.num_of_runs = num_of_clusters

        # run the KMeans Algorithm
        kmeans = KMeans(num_of_clusters, num_of_runs).fit(self.df)
        # add column for each country
        updated_df = kmeans.predict(self.df)
        self.df["cluster"] = updated_df
        self.scatter()
        self.horopleth_map()

    def scatter(self):
        self.scatterPlot = plt.scatter(x = self.df["Social support"], y = self.df["Generosity"], c = self.df["cluster"])
        plt.title("K-Means Clustering")
        plt.xlabel("Social support")
        plt.ylabel("Generosity")
        plt.savefig("scatter.png")
        plt.colorbar(self.df)

    def horopleth_map(self):




  '''  def printMap(self):
        py.sign_in("sarfatyl","AAk5mt9UQlWdoE7aOiZ7")
        scl = [[0.0, 'rgb(242,240,247)'], [0.2, 'rgb(218,218,235)'], [0.4, 'rgb(188,189,220)'], \
               [0.6, 'rgb(158,154,200)'], [0.8, 'rgb(117,107,177)'], [1.0, 'rgb(84,39,143)']]

        data = [dict(
            type='choropleth',
            colorscale=scl,
            autocolorscale=False,
            locations=self.df['country'],
            z=self.df['cluster'].astype(float),
            locationmode='Country Name',
            text=self.df['country'],
            marker=dict(
                line=dict(
                    color='rgb(255,255,255)',
                    width=2
                )),
            colorbar=dict(
                title="Cluster")
        )]

        layout = dict(
            title='K-Means Clustering Visualization',
            geo=dict(
                scope='cluster group',
                projection=dict(type='Mercator'),
                showlakes=True,
                lakecolor='rgb(255, 255, 255)'),
        )

        fig = dict(data=data, layout=layout)
        py.iplot(fig, filename='d3-cloropleth-map')
        py.image.save_as(fig, filename="mapPLT.png")
        temp=Image.open("mapPLT.png")
        temp = temp.convert('RGB').convert('P', palette=Image.ADAPTIVE)
        temp.save('mapPLT.gif') '''