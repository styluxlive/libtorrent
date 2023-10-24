#!/usr/bin/env python3
from __future__ import print_function

f = open('../include/libtorrent/settings_pack.hpp')

out = open('settings.rst', 'w+')
all_names = set()


def print_field(str, width):
    return f"{str}{' ' * (width - len(str))}"


def render_section(names, description, type, default_values):
    max_type_len = max(len(type), len('type'))
    max_name_len = max(len(max(names, key=len)), len('name'))
    max_val_len = max(len(max(default_values, key=len)), len('default'))

    # add link targets for the rest of the manual to reference
    for n in names:
        print('.. _%s:\n' % n, file=out)
        for w in n.split('_'):
            all_names.add(w)

    if len(names) > 0:
        print('.. raw:: html\n', file=out)
        for n in names:
            print('\t<a name="%s"></a>' % n, file=out)
        print('', file=out)

    separator = '+-' + ('-' * max_name_len) + '-+-' + ('-' * max_type_len) + '-+-' + ('-' * max_val_len) + '-+'

    # build a table for the settings, their type and default value
    print(separator, file=out)
    print(
        f"| {print_field('name', max_name_len)} | {print_field('type', max_type_len)} | {print_field('default', max_val_len)} |",
        file=out,
    )
    print(separator.replace('-', '='), file=out)
    for i in range(len(names)):
        print(
            f'| {print_field(names[i], max_name_len)} | {print_field(type, max_type_len)} | {print_field(default_values[i], max_val_len)} |',
            file=out,
        )
        print(separator, file=out)
    print(file=out)
    print(description, file=out)


mode = ''

# parse out default values for settings
f2 = open('../src/settings_pack.cpp')
def_map = {}
for line in f2:
    line = line.strip()
    if not line.startswith('SET(') \
        and not line.startswith('SET_NOPREV(') \
            and not line.startswith('DEPRECATED_SET('):
        continue

    line = line.split('(')[1].split(',')
    if line[1].strip()[0] == '"':
        default = ','.join(line[1:]).strip()[1:].split('"')[0].strip()
    else:
        default = line[1].strip()
    def_map[line[0]] = default
    print(f'{line[0]} = {default}')

description = ''
names = []

for line in f:
    if 'enum string_types' in line:
        mode = 'string'
    if 'enum bool_types' in line:
        mode = 'bool'
    if 'enum int_types' in line:
        mode = 'int'
    if '#if TORRENT_ABI_VERSION == 1' in line:
        mode += 'skip'
    if '#if TORRENT_ABI_VERSION <= 2' in line:
        mode += 'skip'
    if '#endif' in line:
        mode = mode[:-4]

    if mode == '':
        continue
    if mode[-4:] == 'skip':
        continue

    line = line.lstrip()

    if line == '' and len(names) > 0:
        if description == '':
            for n in names:
                print(f'WARNING: no description for "{n}"')
        elif description.strip() != 'hidden':
            default_values = [def_map[n] for n in names]
            render_section(names, description, mode, default_values)
        description = ''
        names = []

    if line.startswith('};'):
        mode = ''
        continue

    if line.startswith('//'):
        description += line[3:] if line[2] == ' ' else line[2:]
        continue

    line = line.strip()
    if line.endswith(','):
        line = line[:-1]  # strip trailing comma
        if '=' in line:
            line = line.split('=')[0].strip()
        if line.endswith('_internal'):
            continue

        names.append(line)

with open('hunspell/settings.dic', 'w+') as dictionary:
    for w in all_names:
        dictionary.write(w + '\n')
out.close()
f.close()
