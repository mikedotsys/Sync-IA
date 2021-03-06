import os
from glob import glob
import csv
import urllib.request
import re
import time
from random import randint


def main():
    # declare empty file names list
    col_file_names = []

    # Get list from collection URL as csv and convert to list
    ia_url = 'https://archive.org/advancedsearch.php?q=apple_ii_library_4am&fl%5B%5D=identifier&sort%5B%5D=&sort%5B' \
             '%5D=&sort%5B%5D=&rows=5000&page=1&callback=callback&save=yes&output=csv '
    response = urllib.request.urlopen(ia_url)
    lines = [l.decode('utf-8') for l in response.readlines()]
    col_lines = csv.reader(lines)
    collection_list = list(col_lines)
    collection_list.sort()

    # fix names
    for i in collection_list:
        fix_name = re.sub("(?<!:)[\[\]']", "", str(i))
        fix_name = re.sub(".+[, ]", "", fix_name)
        col_file_names.append(fix_name)
        col_file_names.sort()

    # Get list of files from local file system and convert to list
    local_files = [os.path.splitext(val)[0] for val in glob("D:/Sync IA/apple_ii_library_4am/*.zip")]
    formatted_file_names = list(map(lambda b: b.replace("D:/Sync IA/apple_ii_library_4am\\", ""), local_files))
    local_list = [s.split(',') for s in formatted_file_names]
    local_list.sort()

    # Compare list from collection and list from local file system and download
    for i in col_file_names:
        m = 0

        for l in local_list:

            if i == l[0]:
                m = 1
                break

        if m != 1:

            if (i != 'identifier') and (i != 'apple_ii_library_am'):
                download_url = 'https://archive.org/compress/' + i
                file_on_disk = i + '.zip'
                print('downloading file -> ' + file_on_disk)
                print(download_url)
                time.sleep(5.0)
                urllib.request.urlretrieve(download_url, file_on_disk)


if __name__ == "__main__":
    main()
