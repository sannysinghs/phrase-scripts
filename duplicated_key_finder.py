import os
import xml.etree.ElementTree as ET


def find_duplicate_keys(folder_path):
    keys = {}
    duplicate_keys = []

    # Iterate over files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.xml'):
            file_path = os.path.join(folder_path, file_name)
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Extract keys from each XML file
            for element in root.findall('.//string'):
                key = element.get('name')
                if key in keys:
                    if key not in duplicate_keys:
                        duplicate_keys.append(key)
                else:
                    keys[key] = True

    return duplicate_keys


# # Provide the path to the folder containing the XML files
# folder_path = '/path/to/xml/files/folder'
# duplicates = find_duplicate_keys(folder_path)

# if duplicates:
#     print('Duplicated Keys:')
#     for key in duplicates:
#         print(key)
# else:
#     print('No duplicated keys found.')
