import features.extraction as x
import classifier.classifier as classifier

def print_menu():
    print('=========================================')
    print('Menu:')
    print('(default paths: classifier/features_train.txt, classifier/tree.pck)')
    print('xtrain - extract features from files in data_set folder for training and validating')
    print('x - extract features from files in data_set folder for classifying')
    print('t - train tree from features file')
    print('v - validate accuracy of classifier')
    print('c - classify from features files')
    print('q  - quit')

if __name__ == '__main__':

    print('=========================================')
    print('Welcome to HTML-classifier (^_^)')

    while True:
        print_menu()
        command = input('>> ')

        if command.startswith('q'):
            break
        elif command.startswith('xtrain'):
            x.extract(True)
        elif command.startswith('x'):
            x.extract(False)
        elif command.startswith('t'):
            classifier.train()
        elif command.startswith('v'):
            classifier.validate()
        elif command.startswith('c'):
            classifier.classify()
