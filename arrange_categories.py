import csv
from os import listdir, getcwd, makedirs, rename
from os.path import isfile, join, exists
from collections import defaultdict

if __name__ == '__main__':
    category1tofiles = defaultdict(list)
    category2tofiles = defaultdict(list)
    
    onlyfiles = [f for f in listdir(getcwd() + '\\train\\') if isfile(join(getcwd() + '\\train\\', f))]
    # for every file
    for filename  in onlyfiles:
        filepath = join(getcwd() + '\\train\\', filename)
        # read file info
        dirpath = ''

        with open(filepath, 'r', encoding="utf8") as f:
            reader = csv.reader(f, delimiter=' ')
            # get first line
            category = next(reader)
            # add file to category -> files mapping
            category1tofiles[category[0]].append(filename)
            category2tofiles[category[1]].append(filename)
            # construst proper file location
            sequence = (getcwd(), '\\train\\', category[0], '\\',category[1])
            dirpath = ''.join(sequence)
        # after reading put file in proper directory
        if not exists(dirpath):
            makedirs(dirpath)
        rename(filepath, dirpath + '\\' + filename)