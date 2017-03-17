import numpy as np
import pandas as pd


class Statistics:
    def __init__(self, name=''):
        self.data = pd.read_csv(name, delimiter=';')
        # dropping rows containing NaN values
        self.data = self.data[pd.notnull(self.data['Paid'])]
        self.params = ['mean', 'max', 'min', 'median', 'mode']

    def calculate_type(self, group, type_name='All'):
        ans = {}
        header = list(group)
        header.remove('Type')

        types = []
        for i in self.params:
            types.append(type_name + ' (' + i + ')')
        ans['Type'] = types

        for c in header:
            params = []
            params.append(float(group[c].mean()))
            params.append(float(group[c].max()))
            params.append(float(group[c].min()))
            params.append(float(group[c].median()))
            # taking min mode of all possible options
            try:
                params.append(float(min(list(group[c].mode()))))
            except (ValueError, TypeError):
                params.append(float(min(list(group[c]))))
            ans[c] = params

        return ans

    def calculate(self):
        result = self.calculate_type(self.data)

        for i in self.data['Type'].unique():
            temp = self.calculate_type(self.data[self.data['Type'] == i], i)
            for j in result:
                result[j] += temp[j]

        statistics = pd.DataFrame(result, columns=list(result))
        return statistics

    def most_popular_post(self):
        self.data['Popularity'] = self.data['Total Interactions'].div(self.data['Lifetime Post Total Reach'], axis=0)
        result = self.data[self.data['Popularity'] == self.data['Popularity'].max()]
        return result

temp = Statistics('dataset_Facebook.csv')
stat = temp.calculate()
#print(stat)
stat.to_csv('Result.csv', sep=';')
most_popular = temp.most_popular_post()
most_popular.to_csv('Popular.csv', sep=';')
#print (most_popular)
