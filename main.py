"""
Author: Eliza Black

Credits: 
University of Oregon CIS 210 Project 7 Outline
https://www.geeksforgeeks.org/python-find-most-frequent-element-in-a-list/

Description: Organizing and visualizing data in csv file regarding Titanic passengers
"""


import csv
import statistics
import matplotlib.pyplot as plt


def load_data(file_name: str, types: dict) -> dict:
    """
    opens and reads the file named file_name, creates a dictionary to contain the
    data as described in the following steps, and returns it.

    :param file_name: csv file name
    :param types: types of the file columns
    :return: dict_from_lists: dictionary containing the data
    """

    keys = types.items()
    keys = list(keys)

    val_types = types.values()
    val_types = list(val_types)

    with open(file_name, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_file)

        list_of_rows = list(csv_reader)

        # Creating list of lists containing column data (each sub list is a column of data)
        columns = []
        for number in range(len(list_of_rows[0])):
            col_list = []
            for row_list in list_of_rows:
                row_val = row_list[number]

                col_list.append(row_val)

            map(val_types[number], col_list)

            columns.append(col_list)

        # Creating dictionary with kys variable as dict keys and columns list as the values
        # Format example of key, value pair: ('PassengerId', <class 'int'>): [1, 2, 3, 4....]
        dict_from_lists = {k: [k[1](v) for v in vals] for k, vals in zip(keys, columns)}

        return dict_from_lists


def summarize(data: dict):
    """
    Takes the dictionary returned by load_data as the data parameter and summarizes each dictionary
    value, printing the results, right-aligning the numerical results for better readability.
    For int and float values, calculates the min, max, mean, standard deviation, and mode
    For non-numerical data (e.g., strings), output the number of unique values

    :param data: dictionary returned by load_data
    :return: None
    """

    for key, values in data.items():
        print("Statistics for " + str(key[0]) + ":")

        # For dictionary values that contain integers and floats, performs mean, mode, etc calculations:
        if isinstance(values[1], int or float):

            min_val = round(float(min(values)), 1)
            max_val = round(float(max(values)), 1)
            mean_val = round(float(statistics.mean(values)), 1)
            stdev_val = round(float(statistics.stdev(values)), 1)
            mode_val = round(float(statistics.mode(values)), 1)

            # String formatting: right aligning printed results
            min_str = "min:"
            max_str = "max:"
            mean_str = "mean:"
            stdev_str = "stdev:"
            mode_str = "mode:"

            print(f"{min_str:>8}", f"{min_val:>6}")
            print(f"{max_str:>8}",f"{max_val:>6}")
            print(f"{mean_str:>8}", f"{mean_val:>6}")
            print(f"{stdev_str:>8}", f"{stdev_val:>6}")
            print(f"{mode_str:>8}", f"{mode_val:>6}")

        # For dictionary values that contain strings, performs the following:
        elif isinstance(values[1], str):

            # Finding most common value and number of unique values
            counter = 0
            num = values[0]
            unique_vals_cnt = 0
            unique_vals_list = []

            # finding most common value
            for i in values:
                curr_frequency = values.count(i)
                if curr_frequency > counter:
                    counter = curr_frequency
                    num = i

                # finding num of unique values
                if i not in unique_vals_list:
                    unique_vals_cnt += 1
                    unique_vals_list.append(i)

            most_freq = num
            print("Number of unique values: ", unique_vals_cnt)
            print("      Most common value:", most_freq)


def pearson_corr(x: list, y: list) -> float:
    """
    Takes two lists of numerical values (ints or floats) and returns the Pearson correlation coefficient r.
    r results in a value in the range (-1, 1).

    :param x: list of numerical values (ints or floats)
    :param y: list of numerical values (ints or floats)
    :return: corr_rounded: rounded Pearson correlation coefficient r
    """
    # CREDIT: this function is from Python Programming in Context, 3rd Edition

    # Makes sure x and y have the same length. Raises an exception otherwise.
    if len(x) != len(y):
        print("x and y need to be same length")

    x_bar = statistics.mean(x)
    y_bar = statistics.mean(y)
    x_std = statistics.stdev(x)
    y_std = statistics.stdev(y)
    num = 0.0
    for i in range(len(x)):
        num = num + (x[i] - x_bar) * (y[i] - y_bar)
    corr = num / ((len(x) - 1) * x_std * y_std)
    corr_rounded = round(corr, 2)

    return corr_rounded


def survivor_vis(data: dict, col1: tuple, col2: tuple) -> plt.Figure:
    """
    Visualize survival in the Titanic dataset as a scatterplot

    :param data: dict created in load_data
    :param col1: tuple that contains keyvalues that indicate the data column to be visualized
    :param col2: tuple that contains keyvalues that indicate the data column to be visualized
    :return: matplotlib figure
    """
    # col1 and col2 are first part/index of the keys from data dict

    # data[key] is the value, or list of data, pertaining to the col1 or col2 key
    for key in data.keys():
        key_name = key[0]

        # Finding the data columns for given col1 and col2 names
        if key_name == col1[0]:
            data_col_1 = data[key]

            # variable for axis name
            axis_1 = key_name

        elif key_name == col2[0]:
            data_col_2 = data[key]

            # variable for axis name
            axis_2 = key_name

        if key_name == 'Survived':
            col_survival = data[key]

    # Zipping together col1, col2, and their survival into one list of tuples
    survival_col_1_zipped = zip(col_survival, data_col_1)
    survival_col_2_zipped = zip(col_survival, data_col_2)
    zipped_list_1 = list(survival_col_1_zipped)
    zipped_list_2 = list(survival_col_2_zipped)

    # Splitting up zipped_list_1 between died and survived (0 or 1)
    died_1 = []
    survived_1 = []

    for item in zipped_list_1:
        if item[0] == 0:
            died_1.append(item[1])
        elif item[0] == 1:
            survived_1.append(item[1])

    # Splitting up zipped_list_2 between died and survived (0 or 1)
    died_2 = []
    survived_2 = []

    for item in zipped_list_2:
        if item[0] == 0:
            died_2.append(item[1])
        elif item[0] == 1:
            survived_2.append(item[1])

    fig = plt.Figure()
    plt.title("Survival of Titanic Passengers")

    # axis labels
    plt.xlabel(axis_1)
    plt.ylabel(axis_2)

    # create a plt.scatter for each of the sets of values (survived and died)
    plt.scatter(survived_1, survived_2, color="g")
    plt.scatter(died_1, died_2, marker="x", color="r")

    # legend in upper right corner
    plt.legend(["Survived", "Died"])

    plt.savefig(f'scatter-{axis_1}-{axis_2}.png')

    plt.show(block=True)

    return fig


# main() not my work; given in project instructions
def main():
    """
    Main program driver for Project 7.
    """
    # 7.1 Load the dataset
    TITANIC_TYPES = {'PassengerId': int, 'Survived': int, 'Pclass': int,
                     'Sex': str, 'Age': float, 'SibSp': int, 'Parch': int,
                     'Fare': float, 'Embarked': str, 'FamilySize': int,
                     'age_group': str}
    data = load_data('Titanic-clean.csv', TITANIC_TYPES)

    # 7.2 Print informative summaries
    print("\nPart 7.2")
    summarize(data)

    print("\nPart 7.3")
    # 7.3 Compute correlations between age and survival
    corr_age_survived = pearson_corr(data[('Age', float)],
                                     data[('Survived', int)])
    print(f'Correlation between age and survival is {corr_age_survived:3.2f}')

    # 7.3 Correlation between fare and survival
    corr_fare_survived = pearson_corr(data[('Fare', float)],
                                      data[('Survived', int)])
    print(f'Correlation between fare and survival is {corr_fare_survived:3.2f}')

    # 7.3 Correlation between family size and survival
    corr_fare_survived = pearson_corr(data[('FamilySize', int)],
                                      data[('Survived', int)])
    print(f'Correlation between family size and survival is'
          f' {corr_fare_survived:3.2f}')

    # 7.4 Visualize results
    fig = survivor_vis(data, ('Age', float), ('Fare', float))
    fig = survivor_vis(data, ('Age', float), ('Pclass', int))
    fig = survivor_vis(data, ('Age', float), ('Parch', int))


if __name__ == "__main__":
    main()
