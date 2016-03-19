# coding=utf-8
import hashlib
import os
import fnmatch
from operator import itemgetter

from Timer import Timer

def list_files(directory, pattern='*'):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename

def hashfile(filename, hasher_func, blocksize=65536):
    hasher = hasher_func()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(blocksize), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def hashpath(root_path, hasher=hashlib.md5):
    result = []
    for pf in list_files(root_path):
        # ignore directories
        if os.path.isfile(pf):
            filecode = hashfile(pf, hasher)
            result.append((filecode, pf))
    return result


def write_result_to_file(result, file_path):
    with open(file_path, "w") as f:
        for tup in result:
            f.write("%s\n" % str(tup))


def read_result_from_file(file_path):
    result = []
    with open(file_path, "r") as f:
        for line in f:
            result.append(eval(line))
    return result

def find_duplicates(list_of_tuples):
    result = dict()
    list_of_tuples = sorted(list_of_tuples)
    for i, _ in enumerate(list_of_tuples[:-1]):
        (firsthash, firstname) = list_of_tuples[i]
        (secondhash, secondname) = list_of_tuples[i+1]
        if firsthash == secondhash:
            if not result.has_key(firsthash):
                result[firsthash] = set()
            container = result[firsthash]
            container.add(firstname)
            container.add(secondname)
    return result

signs_of_copy = ["(2)", " (2)"]
def find_delete_candidates(result):

    candidates = []
    others = dict()

    for key in result:
        file_set = result[key]
        if len(file_set) is not 2:
            others[key] = file_set
            continue

        file_names = list(file_set)
        first = file_names[0]
        second = file_names[1]
        # remove file extension
        first = first[:first.index('.')]
        second = second[:second.index('.')]
        if first.strip(second) in signs_of_copy:
            candidates.append(file_names[0])
        elif second.strip(first) in signs_of_copy:
            candidates.append(file_names[1])
        else:
            others[key] = file_set


    return (candidates, others)


def find_rename_candidates(result):

    candidates = []
    others = dict()

    for key in result:
        file_set = result[key]
        if len(file_set) is not 2:
            others[key] = file_set
            continue

        file_names = list(file_set)
        first = file_names[0]
        second = file_names[1]
        if len(first) != len(second):
            others[key] = file_set
            continue

        if first.replace('(1)', '') == second.replace('(2)', ''):
            candidates.append((first, second))
        elif second.replace('(1)', '') == first.replace('(2)', ''):
            candidates.append((second, first))
        else:
            others[key] = file_set

    return (candidates, others)


if __name__ == "__main__":
    # root_path = u"Z:\Dropbox (Dropbox Team)\תמונות גיבוי"
    root_path = ur'C:\\Users\nir\Desktop\test'
    # files_list_path = r"c:\temp\hashed_files_list.txt"
    timer = Timer()

    with timer:
        result = hashpath(root_path, hasher=hashlib.md5)

    # write_result_to_file(result, files_list_path)
    # result = read_result_from_file(files_list_path)

    result = find_duplicates(result)
    (candidates, others) = find_delete_candidates(result)

    # for name in candidates:
    #     print name
    # for key in others:
    #     print key
    #     for name in others[key]:
    #         print '\t' + name

    for filename in candidates:
        print 'delete ' + filename
        # os.remove(filename)

    (candidates, others) = find_rename_candidates(others)
    for (first, second) in candidates:
        print 'rename ' + first + ' ' + first.replace('(1)', '')
        # os.rename(first, first.replace('(1)', ''))
        print 'delete ' + second
        # os.remove(second)

    # for pair in candidates:
    #     print pair[0], pair[1]
    # for key in others:
    #     print key
    #     for name in others[key]:
    #         print '\t' + name

    for key in others:
        print key
        for name in others[key]:
            print '\t' + name

    print timer.duration_in_seconds()
