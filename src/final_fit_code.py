import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import json as json


# a, b, c, d
# a=offset, b=scale, c=exp rate, d=delay
def prototype(x, a, b, c, d):
    return a + b * np.exp(c * x + d)


def fit_a_country(x, y, name):
    l_path = 'E:/Programming_stuff/Python/DM_clean/data/all_fits/'
    y_trim = np.delete(y, np.where(y == 0))
    x_trim = np.arange(y_trim.size)

    popt, pcov = curve_fit(prototype, x_trim, y_trim, maxfev=5000)
    data = {
        'a': popt[0],
        'b': popt[1],
        'c': popt[2],
        'd': popt[3]
    }

    with open(l_path + name + '.txt', 'w') as json_file:
        json.dump(data, json_file, indent=4, sort_keys=True)

    plt.figure()
    plt.plot(x, y, 'b-', linewidth=2, label='Original data')
    plt.plot(x_trim, y_trim, 'r-', linewidth=2, label='Trimmed data')
    plt.plot(x_trim, prototype(x_trim, *popt), 'g--', linewidth=2, label='Fit data')
    plt.legend()
    plt.title(name)
    plt.savefig(l_path + name + '.png')
    return data
    # plt.show()


def main():
    path = 'E:/Programming_stuff/Python/DM_clean/data/'
    df = pd.read_csv(path + 'grouped.csv', index_col='Country')
    df = df.drop(['Lat', 'Long'], axis=1)

    # list of all countries which should not be fitted
    countries_to_skip_lst = []
    countries_to_skip_file = open(path + "final_list_of_countries_to_skip.txt", 'r')
    for line in countries_to_skip_file:
        countries_to_skip_lst.append(line.rstrip('\n'))

    # load full table
    full_table = pd.read_csv(path + 'full_table.csv', index_col='Country')
    full_table['a'] = ''
    full_table['b'] = ''
    full_table['c'] = ''
    full_table['d'] = ''
    for country in countries_to_skip_lst:
        if country in full_table.index:
            full_table.drop(index=country, inplace=True)

    for index, row in df.iterrows():
        if index in countries_to_skip_lst:
            continue
        x = np.arange(row.size)
        y = row.values
        try:
            data = fit_a_country(x, y, index)
            full_table.loc[index, 'a'] = data['a']
            full_table.loc[index, 'b'] = data['b']
            full_table.loc[index, 'c'] = data['c']
            full_table.loc[index, 'd'] = data['d']

        except RuntimeError as e:
            print(e)
            print('Error while fitting country: ', index)
            print('Continuing other countries.')

        full_table.to_csv(path + 'full_table.csv', index=True)


if __name__ == '__main__':
    main()

