import argparse
from datetime import datetime
import xmlrpc.client
import json
import os
import re
import sys
from xml.etree.ElementTree import Element,tostring


# globals:
url = None
db = None
username = None
password = None
models = None
common = None
uid = None


def slugify(name):
    return "".join(re.findall(r"[a-z0-9_]", name.lower().replace(" ", "_")))


# Lifted from
# https://stackoverflow.com/questions/28813876/how-do-i-get-pythons-elementtree-to-pretty-print-to-an-xml-file

def _pretty_print(current, parent=None, index=-1, depth=0):
    for i, node in enumerate(current):
        _pretty_print(node, current, i, depth + 1)
    if parent is not None:
        if index == 0:
            parent.text = '\n' + ('\t' * depth)
        else:
            parent[index - 1].tail = '\n' + ('\t' * depth)
        if index == len(parent) - 1:
            current.tail = '\n' + ('\t' * (depth - 1))

def export_data(model, out, name):
    droplist = ["id", "create_uid", "create_date", "write_uid", "write_date", "__last_update"]
    domain = []
    if name:
        domain = [("name", '=', name)]
    ids = models.execute_kw(db, uid, password, model, "search", [domain])
    if len(ids) == 0:
        print("No records found")
        sys.exit(1)
    else:
        out.write('<?xml version="1.0" encoding="utf-8" ?>\n')
        xml_top = Element('odoo')
        xml_top.set('noupdate', '1')
        records = models.execute_kw(db, uid, password, model, "read", [ids])
        for record in records:
            slug = slugify(record["name"])
            e = Element('record')
            e.set('id', slug)
            e.set('model', model)
            for field in droplist:
                if field in record:
                    record.pop(field)
            for field in record:
                if record[field] and record[field] is not False:
                    e2 = Element('field')
                    e2.set('name', field)
                    e2.text = str(record[field])
                    e.append(e2)
            xml_top.append(e)
        _pretty_print(xml_top)
        out.write(tostring(xml_top).decode(encoding='utf-8', errors='strict') + "\n")


def main():
    parser = argparse.ArgumentParser(description="Export Odoo data using XMLRPC")
    parser.add_argument(
        "--creds", required=False, help="Credentials file (default: ~/.odoo-xr.json)"
    )
    parser.add_argument("--out", required=True, help="Output file (CSV format)")
    parser.add_argument("--name", required=False, help="Filter on name")
    args = parser.parse_args()

    # Load the API password
    if args.creds:
        creds_file = args.creds
    else:
        creds_file = os.path.join(os.environ["HOME"], ".odoo-xr.json")
    creds = json.load(open(creds_file))

    global url, db, username, password
    url = creds["url"]
    db = creds["db"]
    username = creds["username"]
    password = creds["password"]

    global models, common, uid
    models = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(url))
    common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(url))
    uid = common.authenticate(db, username, password, {})

    out_file = args.out
    model = 'account.statement.import.sheet.mapping'

    with open(out_file, "w") as out:
        export_data(model, out, args.name)


main()
# vim: ai ts=4 sts=4 et sw=4 ft=python
