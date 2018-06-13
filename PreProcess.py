import numpy as np
from sklearn.preprocessing import LabelEncoder


class PreProcess:

    def __init__(self, data_frame):
        self.df = data_frame
        self.fill_na()      # todo: call to the functions in the gui
        self.standardization()
        self.group_by_country()

    # fill na values in the data frame
    def fill_na(self):
        for column in self.df.columns[1:]:
            if column != 'country' and column != 'year':
                self.df[column].fillna(self.df[column].mean(), inplace=True)

    # normalize the values
    def standardization(self):
        for column in self.df.columns[1:]:
            avg = self.df[column].mean()
            std = np.std(self.df[column])
            self.df[column] = (self.df[column] - avg) / std

    # group by country
    def group_by_country(self):
        self.df = self.df.groupby("country").mean()
        del self.df["year"]

    # transform all nominal values to numeric todo: not sure we need it!!!!
    def transform(self):
        le = LabelEncoder()
        self.df['country'] = le.fit_transform(self.df['country'])
