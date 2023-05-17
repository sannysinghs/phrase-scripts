import subprocess
import glob
import repository
import phrase_app_gen as script
import translated_tags as phrase_tags
import duplicated_key_finder as utils

# phrase_cmd = 'python3 scripts/phrase_app/phrase_pull_adr.py -t {tag} -p {module} -f {file_name}'

def find_path(source, input_data): 
    result_paths = []
    unique_path = []
    for item in input_data:
        tag_to_path = {'tag' : item['tag'], 'module': item['module'], 'string': item['string']}
        pattern = '{}/**/{}/src/main/res/values/{}.xml'.format(source, item['module'], item['string'])
        if (glob.glob(pattern, recursive=False)): 
            string_file_paths = glob.glob(pattern, recursive=False)
                
        else: 
            without_foler = '{}/**{}/src/main/res/values/{}.xml'.format(source, item['module'], item['string'])
            string_file_paths = glob.glob(without_foler, recursive=False)

        p = ''
        for path in string_file_paths: 
            p = path
        
        tag_to_path['path'] = p
        result_paths.append(tag_to_path)
    return result_paths

def find_folder(paths):
    folder = {}
    for p in paths: 
        folder.add(p.rsplit('/', 1)[0])
    return folder

def find_string_with_dash_and_underscore(input_string): 
    index = input_string.find("-")
    if index >= 0:
        end_index = input_string.find("_", index + 1)
        if end_index >= 0:
            return '{}'.format(input_string[0:index]) 
    return 'strings'
    


def breakdown_tags_to_module_and_filename(data): 
    reuslts = []
    for tag in data: 
        mod_to_file = {'tag' : tag }
        index = tag.find("-")
        if index >= 0:
            end_index = tag.find("_", index + 1)
            mod_to_file['module'] = tag[0:end_index] 
            if end_index >= 0:
                mod_to_file['string'] = tag[end_index+1:] 
                reuslts.append(mod_to_file)
                continue
        
        mod_to_file['module'] = tag
        mod_to_file['string'] = 'strings'
        reuslts.append(mod_to_file)
            
    return reuslts

def process_locale(local_id, paths): 
    localised_paths = []
    for p in paths: 
        p['path'] = p['path'].replace("/values/", "/values-{}/".format(local_id))
        localised_paths.append(p)
    return localised_paths    

def list_duplicated_keys(paths): 
    folder = []
    for p in paths:
        directory = p['path'].rsplit('/', 1)[0]
        if directory: 
            folder.append(directory)

    result = []
    for f in folder: 
        keys = utils.find_duplicate_keys(f)
        if keys: 
            result.extend(keys)
            
    return set(result)

def backfill_unknown_modules(data): 
    result = []
    for p in data: 
        filtered = list(filter(lambda x: x['tag'] == p['tag'], phrase_tags.non_standard_tag_to_module))
        if filtered: 
            p['module'] = filtered[0]['module']
        result.append(p)
    return result    

def filter_empty_path(paths):
    return list(filter(lambda x: len(x['path']) > 0, paths))

def main():
    source = '/Users/sanny.segue/Documents/pax/pax-android'
    
    mod_to_files = breakdown_tags_to_module_and_filename(phrase_tags.data) # tag, module, string
    mod_to_files = backfill_unknown_modules(mod_to_files)

    paths = find_path(source, mod_to_files) # tag, path, string, module
    paths = process_locale('ja', paths)
    paths = filter_empty_path(paths)
    
    # for i in list_duplicated_keys(paths): 
    #     print(i)
    
    script.generate_phrase_app_yml(paths)

if __name__ == '__main__':
    main()