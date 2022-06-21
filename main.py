# method to extract the data from the csv file
import csv
import math
import os
import matplotlib.pyplot as plt


diameter = 0.8 * 10 ** -2
radius = diameter / 2
area = math.pi * radius ** 2
lenght = 44 * 10 ** -2
print(area)


def extract_data(file_name):
    data = []
    with open(file_name, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            for i in range(len(row)):
                try:
                    row[i] = float(row[i].replace(',', '.'))
                except ValueError:
                    pass
            data.append(row)
    return data


# plot the data
def plot_data(data, file_name):
    # extract the data
    x = []
    y = []
    for row in data:
        if file_name == 'C15.csv':
            x.append((float(row[1]) + 2.49496) / lenght)
            y.append(10 ** -6 * (float(row[2]) - 1231.54285) / area)
        else:
            x.append(float(row[1]) / lenght)
            y.append(10 ** -6 * float(row[2]) / area)
    # plot the data
    plt.plot(x, y, label=file_name)
    plt.xlabel('Déformation (SA)')
    plt.ylabel('Contrainte (MPa)')
    leg = plt.legend(loc='lower right', ncol=3, mode="expand", shadow=True, fancybox=True)
    leg.get_frame().set_alpha(0.5)
    # change the color of the line


def plot_raw_data(data, file_name):
    # extract the data
    x = []
    y = []
    for row in data:
        x.append(float(row[1]))
        y.append(float(row[2]))
    # plot the data
    plt.plot(x, y, label=file_name)
    plt.xlabel('extension (mm)')
    plt.ylabel('Charge (N)')
    leg = plt.legend(loc='lower right', ncol=3, mode="expand", shadow=True, fancybox=True)
    leg.get_frame().set_alpha(0.5)
    # change the color of the line


# plot a single curve
def plot_single_curve(data, file_name, save=False):
    # extract the data
    x = []
    y = []
    for row in data:
        x.append(float(row[1]) / lenght)
        y.append(10 ** -6 * float(row[2]) / area)
    # plot the data
    plt.plot(x, y, label=file_name)
    plt.xlabel('Déformation (SA)')
    plt.ylabel('Contrainte (MPa)')
    Rm = find_max(data)
    plt.axhline(10 ** -6 * Rm / area, color='red')
    plt.title(str(file_name).split('.csv')[0])
    plt.text(0.25, 10 ** -6 * Rm / area + 10 ** -6 * 0.05e8, f'Rm = {round(10 ** -6 * Rm / area, 2)} MPa', rotation=360)
    # Re = find_Re(data)
    # plt.axhline(10 ** -6 * Re / area, color='red')
    # plt.text(0.25, 10 ** -6 * Re / area - 10 ** -6 * 0.25e8, f'Re = {round(10 ** -6 * Re / area, 2)} MPa', rotation=360)

    if save:
        plt.savefig(str(file_name).split('.csv')[0] + '.png')
    plt.show()


def plot_single_curve_raw(data, file_name, save=False):
    # extract the data
    x = []
    y = []
    for row in data:
        x.append(float(row[1]))
        y.append(float(row[2]))
    # plot the data
    plt.plot(x, y, label=file_name)
    plt.xlabel('extension (mm)')
    plt.ylabel('Charge (N)')
    Fm = find_max(data)
    plt.axhline(Fm, color='red')
    plt.title(str(file_name).split('.csv')[0])
    plt.text(0.25, Fm + 300, f'Fm = {Fm} N', rotation=360)
    if save:
        plt.savefig(str(file_name).split('.csv')[0] + '_brute.png')
    plt.show()


def plot_all_single_curves(folder):
    files = get_files(folder)
    for file in files:
        plot_single_curve(extract_data(file)[3:], file)


def plot_all_single_curves_raw(folder):
    files = get_files(folder)
    for file in files:
        plot_single_curve_raw(extract_data(file)[3:], file)


# calculate the median of a list
def median(lst, a, b):
    lst = lst[a:b]
    sortedLst = sorted(lst)
    lstLen = len(lst)
    index = (lstLen - 1) // 2
    return sortedLst[index]


def find_Re(data):
    C = []
    # extract the data
    x = []
    y = []
    tolerance = 0.7
    for row in data:
        x.append(float(row[1]))
        y.append(float(row[2]))
    f = 1
    for i in range(int((len(data) - 100) / f)):
        C.append(
            (
                    median(x, i * f, (i + 1) * f) - median(x, (i + 1) * f, (i + 2) * f)
            )
            /
            (
                    median(y, i * f, (i + 1) * f) - median(y, (i + 1) * f, (i + 2) * f)
            )
        )
    # O = 500  # inox
    O = 200  # all
    # O = 660 # C35 eau revenu

    for i in range(O, len(C)):
        if C[i + 1] / C[i] < 1 - tolerance:
            return y[i]


def get_files(folder):
    files = []
    for file in os.listdir(folder):
        if file.endswith(".csv"):
            files.append(file)
    return files


def plot_all_data(folder, save=False):
    files = get_files(folder)
    for file in files:
        plot_data(extract_data(file)[3:], file)
    # save the image
    if save:
        plt.savefig('courbes.png')
    plt.show()


def plot_all_row_data(folder, save=False):
    files = get_files(folder)
    for file in files:
        plot_raw_data(extract_data(file)[3:], file)
    if save:
        plt.savefig('courbes_brutes.png')
    plt.show()


def courbes():
    plot_all_data('.', save=True)
    # plot_all_row_data(".")
    return None


# method to find the max and min of the data
def find_max(data):
    max_value = 0
    for row in data:
        if row[2] > max_value:
            max_value = row[2]
    return max_value


# file = 'C15_T'+'.csv'
# print(find_Re(extract_data(file)[3:])/area * 10**-6)
# plot_single_curve(extract_data(file)[3:], file, save=True)
# plt.show()
plot_all_single_curves('.')
# plot_all_row_data('.')
courbes()
