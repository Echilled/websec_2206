import Watcher_Cleanup
import matplotlib.pyplot as plt
import numpy as np


def main():
    # x axis values
    # creating the dataset
    data = Watcher_Cleanup.index_change_history()
    Watcher_Cleanup.DRIVER.quit()
    courses = list(data.keys())
    values = list(data.values())

    fig = plt.figure(figsize=(10, 5))

    # creating the bar plot
    plt.bar(courses, values, color='maroon',
            width=0.4)

    plt.xlabel("URLs checked")
    plt.ylabel("No. of times it's content changed")
    plt.title("Number of times each URL changed")
    plt.show()


if __name__ == '__main__':
    main()