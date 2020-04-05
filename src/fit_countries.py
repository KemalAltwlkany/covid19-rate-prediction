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
    l_path = 'E:/Programming_stuff/Python/DM_clean/data/fits/'
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
    #plt.show()


# Ovo sam pokrenuo jednom, i dobio 165 uspjesnih fitova. Medjutim, od tih 165, neki ne valjaju.
# Treba ih dodati na spisak, i izbjegavati. Razlozi su premalo podataka.
# To je prvi filter.
def main():
    path = 'E:/Programming_stuff/Python/DM_clean/data/'
    df = pd.read_csv(path + 'grouped.csv', index_col='Country')
    df = df.drop(['Lat', 'Long'], axis=1)
    successful_fit = open(path + 'successful_fit.txt', 'w')
    failed_fit = open(path + 'failed_fit.txt', 'w')

    # countries which should be skipped and removed.
    bad_fits = open(path + 'bad_fits.txt', 'r')
    countries_to_skip = []
    for line in bad_fits:
        countries_to_skip.append(line.rstrip('\n'))

    # countries which should be done with special parameters
    # because the fits were poor
    poor_fits = open(path + "repeat_fit.txt", 'r')
    for line in poor_fits:
        countries_to_skip.append(line.rstrip('\n'))
        
    for index, row in df.iterrows():
        if index in countries_to_skip:
            continue
        x = np.arange(row.size)
        y = row.values
        if index == 'Malawi':
            continue
        try:
            fit_a_country(x, y, index)
            successful_fit.write(index + '\n')
        except RuntimeError as e:
            print(e)
            print('Error while fitting country: ', index)
            print('Continuing other countries.')
            failed_fit.write(index + '\n')


if __name__ == '__main__':
    main()
