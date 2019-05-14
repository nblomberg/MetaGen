import os
import ast


def meta_loader(absolute_path):
    """
    Finds all files in the chosen input folder and subfolders under it and saves filename and file location into
    meta_dict dictionary where file location is the KEY.

    :param absolute_path: Absolute path to input  (String)
    :return meta_dict: Metadata stored in a dictionary. PATH to a file is the KEY and it includes HEADERS and FILENAME
    """

    meta_dict = {}
    for root, dirs, files in os.walk(absolute_path):
        for f in files:
            meta_dict[os.path.join(root, f)] = {'filename': f}

    return meta_dict


def load_headers(meta_dict, regex, name_ext):
    """
    Loads headers with name_ext (e.g '.csv') from the file and saves them, filename and file location into a meta_dict
    dictionary where file location is the KEY.

    :param meta_dict:
    :param regex: data splitting between these. e.g ','  (String)
    :param name_ext: target file extension. e.g '.csv'  (String)
    :param absolute_path: Absolute path to input  (String)
    :return meta_dict: Metadata stored in a dictionary. PATH to a file is the KEY and it includes HEADERS and FILENAME
    """

    for path in meta_dict:
        if path.endswith(name_ext):
            file_obj = open(path, 'r')
            headers = file_obj.readline().rstrip().split(regex)
            meta_dict[path].update({'headers': headers})
            file_obj.close()
    return meta_dict


def load_types(meta_dict, regex, name_ext):
    """

    :param meta_dict:
    :param regex: data splitting between these. e.g ','  (String)
    :param name_ext: target file extension. e.g '.csv'  (String)
    :return meta_dict: Metadata stored in a dictionary. PATH to a file is the KEY and it includes HEADERS and FILENAME
    """

    for path in meta_dict:
        if path.endswith(name_ext):
            types = []
            file_obj = open(path, 'r')
            next(file_obj)   # Skipping headers
            first_line = file_obj.readline().rstrip().split(regex)
            for member in first_line:
                try:
                    try:
                        types.append(type(ast.literal_eval(member)).__name__)
                    except SyntaxError:
                        types.append("String")
                except ValueError:
                    types.append("Unknown")
                    # Prompt Logger
            meta_dict[path].update({'types': types})
            file_obj.close()
    return meta_dict


def meta_save(meta_dict, absolute_path, name="\\Meta_data.csv", append=False):
    """
    Saves data stored in meta_dict into a default csv file.

    :param meta_dict:
    :param absolute_path: Absolute path to output. MUST BE DIFFERENT THAN INPUT!  (String)
    :param name:
    :param append:
    """

    path = absolute_path + name
    if append:
        file_obj = open(path, 'a')
    else:
        file_obj = open(path, 'w')
    file_obj.write("Metadata list\n")
    file_obj.write('Listed files: %d' % len(meta_dict.keys()))
    file_obj.write('\n')
    for path in meta_dict:
        file_obj.write('\n')
        file_obj.write('Path;Name;Headers;\n')
        try:
            file_obj.write('%s;%s;%s\n' % (path, meta_dict[path].get('filename'), (';'.join(meta_dict[path].get('headers')))))
            file_obj.write(';;%s\n' % (';'.join(meta_dict[path].get('types'))))
        except TypeError:
            file_obj.write('%s;%s;None\n' % (path, meta_dict[path].get('filename')))
    file_obj.close()
    print("Metadata saved into %s", path)
    return

def make_header_list(meta_dir, selected_files, output_name):
    """
    Makes a header list from selected files. This way other programs can import necessary headers easily.

    :param meta_dict: Metadata stored in a dictionary. PATH to a file is the KEY and it includes HEADERS and FILENAME
    :param selected_files: folder names for selected files e.g '\\C:\\Data\\selected' (String)
    :output_name: Output file name (String)
    :return:
    """

    return