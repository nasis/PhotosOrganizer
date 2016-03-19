# coding=utf-8
import hashlib
import os
import fnmatch

from Timer import Timer

def list_files(directory, pattern='*'):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename

def hashfile(filename, hasher_func=hashlib.md5, blocksize=65536):
    hasher = hasher_func()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(blocksize), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def hashpath(root_path, hasher_func):
    result = []
    for pf in list_files(root_path):
        # ignore directories
        if os.path.isfile(pf):
            filecode = hashfile(pf, hasher_func)
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
            set_container = result[firsthash]
            set_container.add(firstname)
            set_container.add(secondname)
    return result

signs_of_copy = ["(2)", " (2)"]
def find_delete_candidates(result):

    candidates = []
    others = dict()

    for key in result:
        file_names = sorted(list(result[key]), reverse=True)

        found = False
        for i in xrange(1, len(file_names)):
            # The list is reverse sorted
            shorter = file_names[i-1]
            longer = file_names[i]

            # remove file extension
            if longer.find('.') < 0 or shorter.find('.') < 0:
                continue

            # str.strip() didn't work well on all cases
            prefix = shorter[:shorter.rindex('.')]
            if longer.startswith(prefix) and longer[len(prefix):longer.rindex('.')] in signs_of_copy:
                found = True
                candidates.append(longer)

        if not found or len(file_names) is not 2:
            others[key] = file_names

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


def find_folder_duplicates(file_duplicates, hashed_paths):

    # candidates = []
    others = dict()

    ignore_list = [".picasa.ini"]

    # pre-processing, match each path with all the files it contains
    folderhash = dict()
    for (hashvalue, filepath) in hashed_paths:
        filename = os.path.basename(filepath)
        if filename in ignore_list:
            continue
        basepath = os.path.dirname(filepath)
        if not basepath in folderhash:
            folderhash[basepath] = set()
        folderhash[basepath].add(hashvalue)

    hash2path_list = []
    for basepath in folderhash:
        hasher = hashlib.md5()
        for hashvalue in folderhash[basepath]:
            hasher.update(hashvalue)
        hash2path_list.append((hasher.hexdigest(), basepath))
    # identical folders
    folder_duplicates = find_duplicates(hash2path_list)

    partial_folder_duplicates = set()
    for key in file_duplicates:
        filenames = file_duplicates[key]
        for i in xrange(1, len(filenames)):
            folder_a = os.path.dirname(filenames[i-1])
            folder_b = os.path.dirname(filenames[i])
            if folder_a == folder_b:
                continue
            files_a = folderhash[folder_a]
            files_b = folderhash[folder_b]
            inter = files_a.intersection(files_b)
            symmdiff = files_a.symmetric_difference(files_b)
            if len(symmdiff) > 0 and float(len(inter)) / max(len(files_a), len(files_b)) > 0.9:
                partial_folder_duplicates.add((folder_a, folder_b))
            # if a single file in this duplicate set is not matched list all of it
            else:
                if not key in others:
                    others[key] = set()
                others[key].add(filenames[i-1])
                others[key].add(filenames[i])

    return (folder_duplicates, partial_folder_duplicates, others)


if __name__ == "__main__":

    do_hashfiles = True
    is_debug = True
    hasher = hashlib.md5

    root_path = ur"Z:\Dropbox (Dropbox Team)\תמונות גיבוי"
    files_list_path = r"c:\temp\hashed_files_list_phase2.txt"
    # root_path = ur'C:\\Users\nir\Desktop\test'
    # files_list_path = r"c:\temp\hashed_files_list2.txt"

    timer = Timer()
    if do_hashfiles:
        with timer:
            hashed_path = hashpath(root_path, hasher_func=hasher)
        write_result_to_file(hashed_path, files_list_path)
    else:
        hashed_path = read_result_from_file(files_list_path)

    duplicates = find_duplicates(hashed_path)
    (delete_candidates, others) = find_delete_candidates(duplicates)

    for filename in delete_candidates:
        print 'delete ' + filename
        if not is_debug:
            try:
                os.remove(filename)
            except Exception, e:
                print e

    (rename_candidates, others) = find_rename_candidates(others)
    for (first, second) in rename_candidates:
        print 'rename ' + first + ' ' + first.replace('(1)', '')
        print 'delete ' + second
        if not is_debug:
            try:
                os.rename(first, first.replace('(1)', ''))
                os.remove(second)
            except Exception, e:
                print e

    (folder_duplicates, partial_folder_duplicates, others) = find_folder_duplicates(others, hashed_path)
    print "Folder " + str(len(folder_duplicates))
    for key in folder_duplicates:
        print "Folder " + key
        for name in folder_duplicates[key]:
            print '\t' + name

    print "Partial Folder " + str(len(partial_folder_duplicates))
    for (first, second) in partial_folder_duplicates:
        print "Partial Folder"
        print '\t' + first
        print '\t' + second

    print "Others " + str(len(others))
    for key in others:
        print key
        for name in others[key]:
            print '\t' + name

    print timer.duration_in_seconds()
