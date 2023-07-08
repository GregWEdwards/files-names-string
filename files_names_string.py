import os
import re
import typing

#This script will run to create a string of every file name in a specified directory.
#The string is customizable to exclude certain file types from the list and/or exclude
# file extensions from the names of the files

GENERIC_EXTENSION_RE = re.compile('(.*)(\.[a-zA-Z0-9]{3,})$')

def input_YN(question: str) -> bool:
    """Takes a prompting question that should end in 'Y/N\n' and prompts the executor
    with the question. The input is then checked for either a 'Y' or 'N' string value
    and will repeat the question until a valid response is input.

    Keyword arguments:
    question -> what to ask the user; should end in 'Y/N\n'.
    """
    flag = False
    while not flag:
        response = input(question)
        if response == 'Y':
            return True
        elif response == 'N':
            return False
        else:
            print('The response must be either \'Y\' or \'N\'.')

def scan_for_file_types(path: str) -> typing.Optional[str]:
    """Iterates through each file in the directory at the specified path and collects
    each unique file extension, including subdirectories. Returns a formatted string
    displaying each file type or None if the directory is empty.
    
    Keyword arguments:
    path -> absolute path to the directory to search
    """
    builder = set()
    with os.scandir(path) as entries:
        for entry in entries:
            if os.path.isdir(path + '/' + entry.name):
                builder.add('Directories')
            else:
                match = GENERIC_EXTENSION_RE.search(entry.name)
                builder.add(match.group(2))
    if len(builder) == 0:
        return None
    return 'The following file types were detected in this folder:\n\t' + '\n\t'.join(builder)

path = input('Type the absolute path of the folder, then press Enter.\n')
file_types = scan_for_file_types(path)
if file_types:
    print('\n' + file_types)
else:
    print('There are no files in this directory')
    exit()

exclude_YN = input_YN('\nDo you want to exclude any file types? Y/N\n')
exclude_extensions = [] #will stay empty if exclude_YN is False
exclude_directories = False
if exclude_YN:
    flag = False
    while not flag:
        new_extension = input('Type the extension of one of the file types that you want to exclude, starting with \'.\'. If you want to exclude directories, type \'Directory\'. If you\'re done, type "Done". Then, press Enter.\n')
        if new_extension == 'Done':
            flag = True
        elif new_extension == 'Directory':
            exclude_directories = True
        elif new_extension not in file_types:
            print('That file extension was not found in the list of known file extensions.')
        else:
            exclude_extensions.append(new_extension)
    if len(exclude_extensions) == 0 and exclude_directories:
        print('Only excluding directories\n')
    else:
        print('Excluding files with the following file extensions: ' + ' '.join(exclude_extensions))
        if exclude_directories:
            print('Also excluding directories\n')
        else:
            print('Not excluding directories\n')

extension_print_YN = input_YN('Do you want the string to be printed without the file extensions? Y/N\n')
extension_re = re.compile('|'.join(exclude_extensions)) if len(exclude_extensions) > 0 else None
builder = ''

with os.scandir(path) as entries:
    for entry in entries:
        if exclude_directories and os.path.isdir(path + '/' + entry.name):
            continue
        if extension_re and extension_re.search(entry.name):
            continue
        if extension_print_YN:
            match = GENERIC_EXTENSION_RE.search(entry.name)
            if match:
                builder += match.group(1)
            else:
                builder += entry.name
        else:
            builder += entry.name
        builder += '\n'

print('\n' + builder)

