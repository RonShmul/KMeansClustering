from sklearn.cluster import KMeans
from PIL import Image
import matplotlib.pyplot as plt
import plotly.plotly as py

class Cluster:
    scatterPlot = None

    def __init__(self, data_frame, num_of_clusters, num_of_runs):
        self.df = data_frame
        self.clusters = num_of_clusters
        self.runs = num_of_runs

        # run the KMeans Algorithm
        k_means = KMeans(n_clusters=self.clusters, n_init=self.runs).fit(self.df)
        # add column for each country
        updated_df = k_means.predict(self.df)
        self.df["cluster"] = updated_df
        self.scatter()
        self.horopleth_map()

    def scatter(self):
        self.scatterPlot = plt.scatter(x=self.df["Social support"], y=self.df["Generosity"], c=self.df["cluster"])
        plt.colorbar(self.scatterPlot)
        plt.xlabel("Social support")
        plt.ylabel("Generosity")
        plt.title("K Means Clustering")
        plt.savefig("scatter.png")

    def horopleth_map(self):
        scl = [[0.0, 'rgb(242,240,247)'], [0.2, 'rgb(218,218,235)'], [0.4, 'rgb(188,189,220)'],
               [0.6, 'rgb(158,154,200)'], [0.8, 'rgb(117,107,177)'], [1.0, 'rgb(84,39,143)']]
        data = [dict(
            type='choropleth',
            colorscale=scl,
            autocolorscale=False,
            locations=self.df.axes[0].tolist(),
            z=self.df["cluster"],
            locationmode='country',
            text=self.df.axes[0].tolist(),
            marker=dict(
                line=dict(
                    color='rgb(255,255,255)',
                    width=2
                )),
            colorbar=dict(
                title="Millions USD")
        )]

        layout = dict(
            title='K Means Clustering Visualization',
            geo=dict(
                scope='Cluster group',
                projection=dict(type='Mercator'),
                showlakes=True,
                lakecolor='rgb(255, 255, 255)'),
        )
        py.sign_in("ronshmul", "BFWck7n9kO0cEty7zprn")
        fig = dict(data=data, layout=layout)
        py.plot(fig, validate=False, filename='horopleth.png', auto_open=False)
        py.image.save_as(fig, filename='horopleth.png')
