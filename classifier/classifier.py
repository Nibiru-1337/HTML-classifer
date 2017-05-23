import csv
from os.path import join
from os import getcwd

from classifier.DecisionTree import DecisionTree

DEFAULT_TRAINING_PATH = join(getcwd(), 'classifier', 'features_train.txt')
DEFAULT_CLASSIFY_PATH = join(getcwd(), 'classifier', 'features.txt')
DEFAULT_TREE_PATH = join(getcwd(), 'classifier', 'tree.pck')
DEFAULT_RESULTS_PATH = join(getcwd(), 'classifier', 'results.txt')


def read_training_data(path):
    X = []
    Y = []
    with open(path, 'r') as ds:
        reader = csv.reader(ds, delimiter=',')
        for row in reader:
            process_row(row)
            X.append(row[:-1])
            Y.append(row[-1])
    return X, Y

def process_row(row):
    for idx in range(len(row)):
        row[idx] = int(row[idx])

def read_data(path):
    X = []
    with open(path, 'r') as ds:
        reader = csv.reader(ds, delimiter=',')
        for row in reader:
            process_row(row)
            X.append(row)
    return X

def train(train_file=DEFAULT_TRAINING_PATH):
    # train the tree
    training_data = read_training_data(train_file)
    tree = DecisionTree()
    tree.train(training_data[0], training_data[1])
    tree.save(DEFAULT_TREE_PATH)

def validate(train_file=DEFAULT_TRAINING_PATH):
    # validate accuracy
    training_data = read_training_data(train_file)
    tree = DecisionTree()
    tree.load(DEFAULT_TREE_PATH)
    results = tree.validate(training_data[0], training_data[1])
    with open(DEFAULT_RESULTS_PATH, 'w') as outfile:
        for item in results:
            outfile.write("%s\n" % item)

def classify(features_file=DEFAULT_CLASSIFY_PATH):
    data = read_data(features_file)
    if len(data) == 0:
        print('Error !\n Extract features first!')
        return
    tree = DecisionTree()
    tree.load(DEFAULT_TREE_PATH)
    results = tree.classify(data)
    with open(DEFAULT_RESULTS_PATH, 'w') as outfile:
        for item in results:
            outfile.write("%s\n" % item)

if __name__ == '__main__':
    # train the tree
    train()
    # validate accuracy
    validate()