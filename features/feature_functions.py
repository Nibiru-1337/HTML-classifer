import re

from inspect import isfunction
from urllib import parse


def fire_all_feature_functions(soup, text):
    feature_list = []
    # fire all functions from this script which start with 'feature'
    # they extract features and put output to feature list
    for obj in globals().values():
        if isfunction(obj) and obj.__module__ == __name__ and obj.__name__.startswith('_feature'):
            #print(obj)
            feature_list.append(str(obj(soup, text)))
    return feature_list

def debug_out_to_console(soup, text):
    # get number of "kontakt" occurances in text
    print('kontakt count:' + str(_feature_count_kontakt(soup, text)))
    # check if it contains phone number
    print('Has phone #:' + str(_feature_phone_number(soup, text)))
    # check if it has an <a> tag with href starting with "mailto:"
    print('<a> with href \'mailto:\':' + str(_feature_send_mail_anchor(soup, text)))
    # check if it has opening hours format
    print('opening hours:' + str(_feature_opening_hours(soup, text)))
    # check if it has area code format
    print('area code:' + str(_feature_area_code(soup, text)))
    # check if street address occurs
    print('street address:' + str(_feature_street_adress(soup, text)))
    # check if we have a reference to google maps api
    print('google maps:' + str(_feature_google_maps_ref(soup, text)))
    # check if title has html status code format
    print('error status code in title:' + str(_feature_error_status_code_in_title(soup, text)))
    # check if we have form tag
    print('has form tag:' + str(_feature_has_form_tag(soup, text)))
    # check if it has an iframe with visible content
    print('has iframe with content:' + str(_feature_iframe_with_content_not_fb(soup, text)))
    # check how many p tags
    print('num of p tags:' + str(_feature_count_paragraphs(soup, text)))
    # check how many table tags
    print('num of table tags:' + str(_feature_count_table(soup, text)))
    # check how many radio buttons
    print('num of radio buttons:' + str(_feature_count_radio_buttons(soup, text)))
    # check how many image tags
    print('num of img tags:' + str(_feature_count_image(soup, text)))
#=====================================FEATURE FUNCTIONS(name starts with feature)======================================#
def _feature_phone_number(soup, text):
    # regular exp matching (some?) phone number formats
    pattern = re.compile(r'''
    ((?:[^\w]|\s) # starts with not a word or whitespace
    \d{3}       # area code is 3 digits (e.g. '111')
    [ -]?       # optional separator (0 or 1 time)
    \d{3}       # trunk is 3 digits (e.g. '222')
    [ -]?       # optional separator (0 or 1 time)
    \d{3}       # rest of number is 3 digits (e.g. '333')
    (?:[^\w]|\s)) # starts with not a word or whitespace
    ''', re.VERBOSE)
    # if something matches phone regex return 1
    if pattern.search(text):
        # print(pattern.findall(text))
        return 1
    # else also check if any phone number keywords occur
    else:
        keywords = ['+48', '+44', 'telefon', '☎', '☏']
        return occurs_keywords(keywords, text)

def _feature_send_mail_anchor(soup, text):
    atags = soup.findAll('a', {'href': True})
    for a in atags:
        # print("<a> href values: " + str(a['href']))
        if a['href'].startswith('mailto:'):
            return 1
    return 0

def _feature_opening_hours(soup, text):
    # regular exp matching (some?) opening hours formats
    pattern = re.compile(r'''
    (?:[^\w]|\s)# starts with not a word or whitespace
    (\d{1,2}    # hour of day 1 or 2 digits (e.g. '12' or '9')
    (?:[:.]     # mandatory separator : or .
    \d{2})?     # mandatory minute of day (e.g. '30')
    \s?         # optional whitespace
    [-–]        # FUCKING PIECE OF SHIT UTF-8 ENCODING, - AND – IS NOT THE FUCKING SAME!
    \s?         # optional whitespace
    \d{1,2}     # hour of day 1 or 2 digits (e.g. '12')
    [:.]        # mandatory separator : or .
    \d{2})      # mandatory minute of day (e.g. '30')
    (?:[^\w]|\s)# ends with not a word or whitespace
    ''', re.VERBOSE | re.IGNORECASE)
    # if something matches regex return 1
    if pattern.search(text):
        # print(pattern.findall(text))
        return 1
    else:
        return 0

def _feature_area_code(soup, text):
    # regular exp matching (some?) opening area code formats
    pattern = re.compile(r'''
        ((?:[^\w]|\s)   # starts with not a word or whitespace
        \d{2}           # two digits
        \s?[-–]\s?      # separator (REMEMBER FUCKING UTF-8 DASH!)
        \d{3}           # three digits
        (?:[^\w]|\s))   # ends with not a word or whitespace
        ''', re.VERBOSE | re.IGNORECASE)
    # if something matches regex return 1
    if pattern.search(text):
        # print(pattern.findall(text))
        return 1
    else:
        return 0

def _feature_street_adress(soup, text):
    keywords = ['ulica', 'ul.', 'aleja']
    return occurs_keywords(keywords, text)

def _feature_google_maps_ref(soup, text):
    for link in soup.find_all('a'):
        href = str(link.get('href'))
        # print(href)
        if 'maps.googleapis.com' in href or 'maps.google.com' in href:
            return 1
    return 0

def _feature_error_status_code_in_title(soup, text):
    # check if title has content
    if soup.title is None or len(soup.title.contents) == 0:
        return 0
    title = str(soup.title.contents[0])
    # print(title)
    # regular exp matching (some?) html error status code formats
    pattern = re.compile(r'''
            ((?:[^\w]|\s|^) # starts with not a word, whitespace, or is start of string
            [45]            # starts with 4 or 5 (client error or server error)
            \d{2}           # two digits
            (?:[^\w]|\s|$)) # ends with not a word, whitespace, or is end of string
            ''', re.VERBOSE | re.IGNORECASE)
    # if something matches regex return 1
    if pattern.search(title):
        # (pattern.findall(title))
        return 1
    else:
        return 0

def _feature_iframe_with_content_not_fb(soup, text):
    iframes = soup.findAll('iframe', {'src': True})
    for iframe in iframes:
        # print("<iframe> src values: " + str(iframe['src']))
        parsed_uri = parse.urlparse(iframe['src'])
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        # print(domain)
        if (iframe['src'].startswith('http://www.') \
                    or iframe['src'].startswith('https://www.')) \
                and 'facebook' not in domain:
            # check if it has style tag with visibility set to hidden
            if iframe.has_attr('style'):
                # print("<iframe> style values: " + str(iframe['style']))
                if iframe['style'].startswith('visibility: hidden'):
                    return 0
                else:
                    return 1
            else:
                return 1
    return 0

def _feature_has_form_tag(soup, text):
    return has_tag('form', soup)

def _feature_count_kontakt(soup, text):
    return count_keyword('kontakt', text)

def _feature_count_paragraphs(soup, text):
    return count_tag('p', soup)

def _feature_count_table(soup, text):
    return count_tag('table', soup)

def _feature_count_radio_buttons(soup, text):
    return len(soup.find_all('input', {'type': 'radio'}))

def _feature_count_image(soup, text):
    return len(soup.find_all('img'))

def _feature_count_lists(soup, text):
    return len(soup.find_all('ul')) + len(soup.find_all('ol'))

#============================================HELPER FUNCTIONS==========================================================#
def occurs_keywords(keywords, text):
    for word in keywords:
        if word in text:
            return 1
    return 0

def count_keyword(keyword, text):
    return text.count(keyword)

def has_tag(tag, soup):
    if soup.find(tag) is None:
        return 0
    else:
        return 1

def count_tag(tag, soup):
    return len(soup.find_all(tag))