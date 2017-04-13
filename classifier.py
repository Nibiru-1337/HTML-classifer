import csv
from DecisionTree import DecisionTree

def read_training_data(path):
    X = []
    Y = []
    with open(path, 'r') as ds:
        reader = csv.reader(ds, delimiter=',')
        for row in reader:
            process_row_training(row)
            X.append(row[:-1])
            Y.append(row[-1])
    return X, Y

def process_row_training(row):
    for idx in range(len(row)):
        row[idx] = int(row[idx])


if __name__ == '__main__':
    # train the tree
    training_data = read_training_data('features_train.txt')
    tree = DecisionTree()
    tree.train(training_data[0], training_data[1])
    tree.save('tree.pck')

    # validate accuracy
    training_data = read_training_data('features_train.txt')
    tree = DecisionTree()
    tree.load('tree.pck')
    results = tree.validate(training_data[0], training_data[1])
    with open('results.txt', 'w') as outfile:
        for item in results:
            outfile.write("%s\n" % item)