import features.extraction as x
import classifier.classifier as classifier

def print_menu():
    print('=========================================')
    print('Menu:')
    print('(default paths: classifier/features_train.txt, classifier/tree.pck)')
    print('x - extract features from files in data_set folder')
    print('t [path to txt] - train tree from features file')
    print('v [path to txt] [path to tree] - validate accuracy of classifier')
    print('c [path to txt] - classify from features files')
    print('q  - quit')

if __name__ == '__main__':

    print('=========================================')
    print('Welcome to HTML-classifier (^_^)')

    while True:
        print_menu()
        command = input('>> ')

        if command.startswith('q'):
            break
        elif command.startswith('x'):
            x.extract()
        elif command.startswith('t'):
            classifier.train()
        elif command.startswith('v'):
            classifier.validate()
        elif command.startswith('c'):
            pass
