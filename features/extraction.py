from os import listdir, getcwd
from os.path import isfile, join

from bs4 import BeautifulSoup
import features.feature_functions as ff

DEFAULT_TRAINING_PATH = join(getcwd(), 'classifier')

SECONDARY_TAGS = {'FORUM': 0, 'FORUM FORUM_MAIN': 1, 'FORUM FORUM_SINGLE_COMMENT': 2, 'FORUM FORUM_THREAD': 3,
                  'HIGH_QUALITY_CONTENT ARTICLE': 4, 'NO_CONTENT CONTACT_PAGE': 5, 'NO_CONTENT FORM': 6,
                  'NO_CONTENT IN_FRAME': 7, 'NO_CONTENT NO_CONTENT': 7, 'OTHER_MULTIMEDIA_CONTENT APPLICATION': 8,
                  'OTHER_MULTIMEDIA_CONTENT IMAGE_GALLERY': 9, 'OTHER_MULTIMEDIA_CONTENT ITEM_WITHOUT_TEXT_DESC': 10,
                  'OTHER_MULTIMEDIA_CONTENT ITEMS_LIST': 11, 'OTHER_MULTIMEDIA_CONTENT OTHERS': 12,
                  'OTHER_MULTIMEDIA_CONTENT QUIZ': 13, 'OTHER_MULTIMEDIA_CONTENT VIDEO': 14,
                  'OTHER_TEXT_CONTENT ITEM_WITH_TEXT_DESC': 15, 'OTHER_TEXT_CONTENT ITEMS_LIST_WITH_TEXT_DESC': 16,
                  'OTHER_TEXT_CONTENT QUIZ': 17, 'OTHER_TEXT_CONTENT TABLE_DATA': 18}

MAIN_TAGS = {'HIGH_QUALITY_CONTENT': 0, 'FORUM': 1, 'NO_CONTENT': 2, 'OTHER_TEXT_CONTENT': 3,
             'OTHER_MULTIMEDIA_CONTENT': 4, 'UNKNOWN': 5, 'ITEM_WITH_TEXT_DESC': 6}


def add_line_to_feature_file(soup, text, out, tag):
    # fire all feature extracting functions
    feature_list = ff.fire_all_feature_functions(soup, text)
    # append actual class at the end if we are creating a training file
    if tag is not None:
        # TODO: MAIN_TAGS OR SECONDARY_TAGS ?
        feature_list.append(str(MAIN_TAGS[tag]))
        # feature_list.append(str(SECONDARY_TAGS[tag]))
    # separate with comma
    out.write(','.join(feature_list))
    # newline for new file
    out.write('\n')


def iterate_over_dataset(out, train):
    # get list of files in data set
    path_to_dataset = join(getcwd(), 'data_set')
    only_files = [f for f in listdir(path_to_dataset) if isfile(join(path_to_dataset, f))]

    # for every file
    for filename in only_files:
        filepath = join(path_to_dataset, filename)
        print('===================================================')
        enc = None
        while True:
            try:
                with open(filepath, 'r', encoding=enc) as f:
                    # print current file
                    print('file:' + filename)
                    # if training read tag
                    tag = None
                    if train:
                        # TODO: MAIN_TAGS OR SECONDARY_TAGS ?
                        tag = f.readline().split(' ')[0].strip()
                        # tag = f.readline().strip()
                    # read the url line
                    url = f.readline().strip()
                    # parse the HTML
                    soup = BeautifulSoup(f, 'html.parser')
                    # standardize the website text content to lowercase
                    text = soup.get_text('\n').lower()
                    # DEBUG CONSOLE OUTPUT
                    ff.debug_out_to_console(soup, text)
                    # TEST CREATING FEATURE FILE
                    add_line_to_feature_file(soup, text, out, tag)
                    break
            except UnicodeDecodeError:
                enc = 'UTF-8'
                continue


def extract(train):
    # open proper feature file
    if train:
        with open(join(DEFAULT_TRAINING_PATH, 'features_train.txt'), "w") as out:
            iterate_over_dataset(out, True)
    else:
        with open(join(DEFAULT_TRAINING_PATH, 'features.txt'), "w") as out:
            iterate_over_dataset(out, False)


if __name__ == '__main__':
    extract()
