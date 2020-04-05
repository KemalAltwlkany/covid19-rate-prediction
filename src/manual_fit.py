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
    l_path = 'E:/Programming_stuff/Python/DM_clean/data/repeated_fits/'
    y_trim = np.delete(y, np.where(y == 0))
    x_trim = np.arange(y_trim.size)

    popt, pcov = curve_fit(prototype, x_trim, y_trim, maxfev=5000, ftol=1e-5, xtol=1e-5)
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
    # plt.show()


if __name__ == '__main__':
    country_name = 'Zambia' # ovdje staviti ime da se fituje samo ta drzava
    path = 'E:/Programming_stuff/Python/DM_clean/data/'
    df = pd.read_csv(path + 'grouped.csv', index_col='Country')
    df = df.drop(['Lat', 'Long'], axis=1)
    y = df.loc[country_name, :].values
    x = np.arange(y.size)
    try:
        fit_a_country(x, y, country_name)
    except RuntimeError as e:
        print(e)
        print('Error while fitting country: ', country_name)
        print('Continuing other countries.')



