# xr-export-statement-sheet-mapping

This is a simple script that uses XML-RPC to export a Statement Sheet definition, created using the Odoo user interface to the `account_statement_import_txt_xlsx` OCA module.

## Usage

* copy `.odoo-xr.json.template` to a file `.odoo-xr.json` in your home directory, or store it elsewhere and refer to the file using the `--creds` command line option. Update it to include your username and API key (or password, if you are so inclined).
* Start the script from the command line, for example:

```
python3 xr-export-statement-sheet-mapping.py --creds .odoo-xr.json --out statement-import-template-knab.xml --name 'KNAB CSV import'

```

* Leave out the `--name` parameter to export all Statement Sheet definitions in one go
* Optionally, add a `__manifest__.py` file and bring the file under git revision control. For an example, see https://github.com/driehuis/account_statement_import_txt_xlsx_bank_knab.
