from os import listdir, getcwd
from os.path import isfile, join

from bs4 import BeautifulSoup
import features.feature_functions as ff

DEFAULT_TRAINING_PATH = join(getcwd(), 'classifier')
TAGS = {'FORUM': 0, 'FORUM FORUM_MAIN': 1, 'FORUM FORUM_SINGLE_COMMENT': 2, 'FORUM FORUM_THREAD': 3,
        'HIGH_QUALITY_CONTENT ARTICLE': 4, 'NO_CONTENT CONTACT_PAGE': 5, 'NO_CONTENT FORM': 6, 'NO_CONTENT IN_FRAME': 7,
        'NO_CONTENT NO_CONTENT': 7, 'OTHER_MULTIMEDIA_CONTENT APPLICATION': 8,
        'OTHER_MULTIMEDIA_CONTENT IMAGE_GALLERY': 9, 'OTHER_MULTIMEDIA_CONTENT ITEM_WITHOUT_TEXT_DESC': 10,
        'OTHER_MULTIMEDIA_CONTENT ITEMS_LIST': 11, 'OTHER_MULTIMEDIA_CONTENT OTHERS': 12,
        'OTHER_MULTIMEDIA_CONTENT QUIZ': 13, 'OTHER_MULTIMEDIA_CONTENT VIDEO': 14,
        'OTHER_TEXT_CONTENT ITEM_WITH_TEXT_DESC': 15, 'OTHER_TEXT_CONTENT ITEMS_LIST_WITH_TEXT_DESC': 16,
        'OTHER_TEXT_CONTENT QUIZ': 17, 'OTHER_TEXT_CONTENT TABLE_DATA': 18}


def create_feature_file(soup, text, tag=None):
    # check if we are creating a training file or not
    if tag is not None:
        file = join(DEFAULT_TRAINING_PATH, 'features_train.txt')
    else:
        file = join(DEFAULT_TRAINING_PATH, 'features.txt')

    # open file in appending mode
    with open(file, 'a') as out:
        # fire all feature extracting functions
        feature_list = ff.fire_all_feature_functions(soup, text)
        # append actual class at the end if we are creating a training file
        if tag is not None:
            feature_list.append(str(TAGS[tag]))
        # separate with comma
        out.write(','.join(feature_list))
        # newline for new file
        out.write('\n')

def extract():
    # get list of files in data set
    path_to_dataset = join(getcwd(), 'data_set')
    only_files = [f for f in listdir(path_to_dataset) if isfile(join(path_to_dataset, f))]

    # for every file
    for filename in only_files:
        filepath = join(path_to_dataset, filename)
        print('===================================================')
        with open(filepath, 'r', encoding="utf8") as f:
            # print current file
            print('file:' + filename)
            # read two first lines
            tag = f.readline().strip()
            url = f.readline()
            # parse the HTML
            soup = BeautifulSoup(f, 'html.parser')
            # check if file is proper HTML
            if soup.head is None or soup.body is None:
                print('This shit ain\'t even HTML!')
                continue
            # standardize the website text content to lowercase
            text = soup.get_text('\n').lower()

            # DEBUG CONSOLE OUTPUT
            ff.debug_out_to_console(soup, text)

            # TEST CREATING FEATURE FILE
            create_feature_file(soup, text, tag)


if __name__ == '__main__':
    extract()