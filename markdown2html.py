#!/usr/bin/python3
"""
Markdown script with python.
"""
import sys
import os.path
import re
import hashlib

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: ./markdown2html.py README.md README.html',
              file=sys.stderr)
        exit(1)

    if not os.path.isfile(sys.argv[1]):
        print('Missing {}'.format(sys.argv[1]), file=sys.stderr)
        exit(1)

    with open(sys.argv[1]) as read:
        with open(sys.argv[2], 'w') as html:
            unorderedStart, orderedStart, paragraph = False, False, False
            # bold syntax
            for line in read:
                line = line.replace('**', '<b>', 1)
                line = line.replace('**', '</b>', 1)
                line = line.replace('__', '<em>', 1)
                line = line.replace('__', '</em>', 1)

                # md5
                md5 = re.findall(r'\[\[.+?\]\]', line)
                md5_inside = re.findall(r'\[\[(.+?)\]\]', line)
                if md5:
                    line = line.replace(md5[0], hashlib.md5(
                        md5_inside[0].encode()).hexdigest())

                # remove the letter C
                removeLetter_c = re.findall(r'\(\(.+?\)\)', line)
                removeMore_c = re.findall(r'\(\((.+?)\)\)', line)
                if removeLetter_c:
                    removeMore_c = ''.join(
                        c for c in removeMore_c[0] if c not in 'Cc')
                    line = line.replace(removeLetter_c[0], removeMore_c)

                length = len(line)
                headings = line.lstrip('#')
                heading_nums = length - len(headings)
                unordered = line.lstrip('-')
                unordered_nums = length - len(unordered)
                ordered = line.lstrip('*')
                ordered_nums = length - len(ordered)
                
                # headings, lists
                if 1 <= heading_nums <= 6:
                    line = '<h{}>'.format(
                        heading_nums) + headings.strip() + '</h{}>\n'.format(
                        heading_nums)

                if unordered_nums:
                    if not unorderedStart:
                        html.write('<ul>\n')
                        unorderedStart = True
                    line = '<li>' + unordered.strip() + '</li>\n'
                if unorderedStart and not unordered_nums:
                    html.write('</ul>\n')
                    unorderedStart = False

                if ordered_nums:
                    if not orderedStart:
                        html.write('<ol>\n')
                        orderedStart = True
                    line = '<li>' + ordered.strip() + '</li>\n'
                if orderedStart and not ordered_nums:
                    html.write('</ol>\n')
                    orderedStart = False

                if not (heading_nums or unorderedStart or orderedStart):
                    if not paragraph and length > 1:
                        html.write('<p>\n')
                        paragraph = True
                    elif length > 1:
                        html.write('<br/>\n')
                    elif paragraph:
                        html.write('</p>\n')
                        paragraph = False

                if length > 1:
                    html.write(line)

            if unorderedStart:
                html.write('</ul>\n')
            if orderedStart:
                html.write('</ol>\n')
            if paragraph:
                html.write('</p>\n')
    exit (0)