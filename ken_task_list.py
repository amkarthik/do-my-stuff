#!/opt/helpers/.venv/bin/python

import os
import xmlrpc.client as xmlrpclib
import argparse

try:
    import pyperclip
    auto_copy = True
except ImportError:
    auto_copy = False
    print("pyperclip not found. Install it using `pip install pyperclip` to have auto copy feature\n")


KENCOVE_PROJECT_ID = 117

parser = argparse.ArgumentParser()
parser.add_argument('milestone', type=str, help='Enter the milestone: ')
parser.add_argument('-n', '--no_id', action='store_true', help="Skip task ID in final list")

args = parser.parse_args()
milestone = args.milestone
skip_id = args.no_id

from dotenv import load_dotenv
load_dotenv(dotenv_path="/opt/helpers/.env")


server = os.environ.get('ODOO_SERVER') or 'https://odoo.sodexis.com'
db = os.environ.get('ODOO_DB') or 'SOD_Master_V12'
user = os.environ.get('ODOO_USER') or 'your_odoo_user_name'
pwd = os.environ.get('ODOO_PWD') or 'your_odoo_password'

common = xmlrpclib.ServerProxy('%s/xmlrpc/2/common' % server)
uid = common.authenticate(db, user, pwd, {})
api = xmlrpclib.ServerProxy('%s/xmlrpc/2/object' % server)

model = 'project.task'
field_list = ['name', 'x_studio_specs']
domain = [['project_id', '=', KENCOVE_PROJECT_ID], ['milestones_id.name', '=', milestone],'|', ['parent_id','=', False], ['parent_id.milestones_id.name', '!=', milestone]]

details =  api.execute_kw(db, uid, pwd, model, 'search_read', [domain], {'fields': field_list})

formatted_name = []
for detail in details:
    name = ""
    if skip_id:
        name += "- {1}".format(detail['id'], detail['name'])
    else:
        name += "[ID: {0}] {1}".format(detail['id'], detail['name'])
    if detail.get('x_studio_specs'):
        name += " ({0})".format(detail['x_studio_specs'])
    formatted_name.append(name)

final = "\n".join(formatted_name)

if auto_copy:
    pyperclip.copy(final)
print(final)
