import csv
import numpy as numpy
import matplotlib.pyplot as plt

# header
# time,TP9,AF7,AF8,TP10,AUX,accelX,accelY,accelZ,gyroX,gyroY,gyroZ
times = []
tp9 = []
af7 = []
af8 = []
tp10 = []


def get_data(filename):
    with open(filename, 'r') as csvfile:
        csvFileReader = csv.reader(csvfile)
        next(csvFileReader)
        for row in csvFileReader:
            times.append(float(row[0]))
            tp9.append(float(row[1]))
            af7.append(float(row[2]))
            af8.append(float(row[3]))
            tp10.append(float(row[4]))


def graph():
    # plt.plot(times, tp9)
    plt.plot(times, af7)
    # plt.plot(times, af8)
    # plt.plot(times, tp10)
    plt.show()


if __name__ == "__main__":
    get_data("./recordings/1553041309127_recording.csv")
    graph()
    print("done")
