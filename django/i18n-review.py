#!/usr/bin/python
# coding=utf-8

###
#
# A script for checking templates in a django project for any hardcoded strings
#
###

import re
import os
import sys


###
#
# Regexp patterns for jinja blocks and html tags
#
###
patterns = {
    'block_tag': re.compile('{%\s*(?P<id>\w+)\s*(?P<data>.*?)%}', re.M|re.S|re.U|re.I),
    'variable_tag': re.compile('{{\s*(?P<content>.+?)\s*}}'),
    'comment_tag': re.compile('{#.*?#}', re.S|re.M),
    'blocktrans_tag': re.compile('{%\s*blocktrans.*?endblocktrans\s*%}', re.S),
    'non_l10n_html_tag': re.compile('<(?P<name>(style|script)).*?</\s*(?P=name)\s*>', re.S|re.M),
    'l10n_html_attr': re.compile('<[^>]*(?:content|label)=(?P<m>["\']).+?(?P=m)[^>]*>'),
    'l10n_val': re.compile('<[^>]*?>\s*[^\s<][^<]*\s*<[^>]*?>', re.S|re.M),
}

###
#
# This is the list of template tags with informations on them
#
# * closing - does the tag has a closing tag
##
tags = {
  'load': {'closing': False},
  'block': {'closing': 'endblock'},
  'for': {'closing': 'endfor'},
  'ifequal': {'closing': 'endifequal'},
  'blocktrans': {'closing': 'endblocktrans'},
}


###
#
# Simple function to grab the file's content
#
###
def get_file(path):
    with open(path, 'r') as f:
        data = f.read()
    return data


###
#
# Load file into memory, strip everything and figure out if there
# are any hardcoded strings in attributes or as text nodes
#
###
def check_file(path=None):
    data = get_file(path)
    hdcoded = []
    (data, num) = patterns['comment_tag'].subn('', data)
    (data, num) = patterns['variable_tag'].subn('', data)
    (data, num) = patterns['blocktrans_tag'].subn('', data)
    (data, num) = patterns['block_tag'].subn('', data)
    (data, num) = patterns['non_l10n_html_tag'].subn('', data)
    matches = patterns['l10n_html_attr'].finditer(data)
    for match in matches:
        hdcoded.append(match.group(0))
    matches = patterns['l10n_val'].finditer(data)
    for match in matches:
        hdcoded.append(match.group(0))
    return hdcoded


###
#
# Walk through the directory and check every file with template ext
#
###
def check_dir(path=None, tmplext='.html'):
    hdcoded = {}
    for root, dirs, files in os.walk(path):
        for f in files:
            (p,ext) = os.path.splitext(f)
            if ext == tmplext:
                fpath = os.path.join(root, f)
                new_hdcoded = check_file(fpath)
                if new_hdcoded:
                    hdcoded[fpath] = new_hdcoded
    return hdcoded


if __name__ == "__main__":
    paths = sys.argv[1:]
    hdcoded = {}
    total = 0
    for i in paths:
        hdcoded.update(check_dir(i))
    for i in hdcoded:
        print('\n== File %s ==' % i)
        for n, elem in enumerate(hdcoded[i]):
            total += 1
            print('%s: %s' % (n+1, elem.replace('\n', '\\n').replace('\t', '\\t')))
    print('==============')
    print('Total: %i' % total)
