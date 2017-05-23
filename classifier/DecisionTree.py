import pickle

from sklearn import tree

from features.extraction import MAIN_TAGS as TAGS


class DecisionTree:
    def __init__(self):
        self.classifier = tree.DecisionTreeClassifier()

    def train(self, X, Y):
        self.classifier.fit(X, Y)

    def validate(self, X, Y):
        results = self.classifier.predict(X)
        correct = 0
        for index in range(len(results)):
            if results[index] == Y[index]:
                correct += 1
        print('======================================================')
        print('Overall accuracy: ' + str(float(correct) / float(len(results))))
        print('======================================================')
        for tag in TAGS:
            # get all entries from tree results that belong to current class
            group = [idx for idx, item in enumerate(results) if item == TAGS[tag]]
            # count how many entries of this group exists in correct data
            count_of_class = Y.count(TAGS[tag])
            # count how many correct entries there are in tree result
            correct = 0
            for idx in group:
                if results[idx] == Y[idx]:
                    correct += 1
            # display group accuracy
            if len(group) == 0 and count_of_class == 0:
                print(str(tag) + ' accuracy: 1.0 (none)')
            else:
                print(str(tag) + ' accuracy: ' + str(float(correct) / float(count_of_class)))

        return results

    def classify(self, X):
        return self.classifier.predict(X)

    def save(self, path):
        pickle.dump(self.classifier, open(path, 'wb'))

    def load(self, path):
        self.classifier = pickle.load(open(path, 'rb'))
