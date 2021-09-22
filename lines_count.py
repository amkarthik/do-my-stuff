#!/opt/helpers/.venv/bin/python

import os
import csv
import argparse
UNWANTED = ('.pyc', '.png', '.jpg', '.gif', '.db', '.pdf', '.mp3', '.ttf', '.eot', '.woff', '.cer','.otf','.jpeg','.gz','.txt','.key')
TO_CHECK = ('.py', '.xml', '.js')
# client_name = input("Enter the client name : ")
parser = argparse.ArgumentParser()
parser.add_argument('csv_file', type=str, nargs='?')
parser.add_argument('path', type=str)
parser.add_argument('location_to', type=str, nargs='?')
args = parser.parse_args()
path = os.path.abspath(args.path)
is_module_path = os.path.isfile(os.path.join(path,'__manifest__.py')) or os.path.isfile(os.path.join('__openerp__.py'))
csv_file_path = os.path.abspath(args.csv_file) if args.csv_file else False
save_file_path = os.path.abspath(args.location_to) if args.location_to else False

headers = ['name', 'technical_name', 'module_path', 'summary', 'author', 'no_of_lines', 'need_to_port', 'to_publish']

if not is_module_path:
    with open(csv_file_path, 'r') as module_file:
        data = csv.DictReader(module_file)
        module_list = []
        for line in data:
            module_name = line['Technical Name']
            for root, dirs, files in os.walk(path, topdown=False):
                for dir in dirs:
                    whole_path = os.path.join(root,dir)
                    if os.path.basename(whole_path) == module_name and 'community_modules_links' not in whole_path and 'sodexis_apps_store_links' not in whole_path:
                        module_path = whole_path
                        if os.path.isfile(os.path.join(module_path,'__manifest__.py')):
                            # print(module_path)
                            module_lines_count = 0
                            for mr, md, mf in os.walk(module_path, topdown=False):
                                for file in mf:
                                    if 'LICENSE' not in file and file != '__manifest__.py' and file != '__openerp__.py' and file.endswith(TO_CHECK):
                                        rf = os.path.join(mr, file)
                                        with open(rf, 'r', errors='replace') as f:
                                            for i in f.readlines():
                                                if i.strip():
                                                    module_lines_count += 1

                            temp_dict = {
                                'name': line['Module Name'],
                                'technical_name': module_name,
                                'module_path': module_path,
                                'summary':line['Summary'].strip() if line['Summary'].strip() else line['Description'].strip(),
                                'author': line['Author'],
                                'no_of_lines':module_lines_count,
                                'need_to_port':'',
                                'to_publish':'',
                            }
                            module_list.append(temp_dict)
        with open(os.path.join(save_file_path,'{0}_new.csv'.format(args.csv_file.split('.')[0])), 'w',newline='') as wf:
            writer = csv.DictWriter(wf, fieldnames=headers)
            writer.writeheader()
            for rows in module_list:
                writer.writerow(rows)
else:
    module_lines_count = 0
    for mr, md, mf in os.walk(path, topdown=False):
        for file in mf:
            if 'LICENSE' not in file and file.endswith(TO_CHECK):
                rf = os.path.join(mr, file)
                with open(rf, 'r', errors='replace') as f:
                    for i in f.readlines():
                        if i.strip():
                            module_lines_count += 1
    print(module_lines_count, os.path.basename(path), sep=' - ')

