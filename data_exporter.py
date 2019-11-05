"""
Script to export recorded data in JSON format.

November 2019
Markus Konrad <markus.konrad@wzb.eu>
"""


import sys

from otreeutils import scripts


if len(sys.argv) != 2:
    print('Call script like this: python %s <output.json>' % sys.argv[0])
    exit(1)

output_file = sys.argv[1]

apps = ['iat']

print('loading data for apps: %s...' % str(apps))

combined = scripts.get_hierarchical_data_for_apps(apps)

print('writing data to file', output_file)

scripts.save_data_as_json_file(combined, output_file, indent=2)

print('done.')
