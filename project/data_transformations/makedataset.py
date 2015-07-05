'''

Converts the BRFSS 2011 and 2012 data provided in the VizRisk competition into Mirador format

@copyright: Fathom Information Design 2014
'''

import sys, os, csv, codecs, shutil, math
import collections
from xml.dom.minidom import parseString
from sets import Set

def write_xml_line(line, xml_file, xml_strings):
    ascii_line = ''.join(char for char in line if ord(char) < 128)
    if len(ascii_line) < len(line):
        print "  Warning: non-ASCII character found in line: '" + line.encode('ascii', 'ignore') + "'"
    xml_file.write(ascii_line + '\n')
    xml_strings.append(ascii_line + '\n')

def is_number(str):
    try:
        float(str)
        return True
    except ValueError:
        return False

def set_var_type(name, lbounds, ubounds, values, var_types, var_ranges):
    categorical = True
    catlock = False
    empty_values = False
    for i in range(0, len(lbounds)):
        lbound = lbounds[i]
        ubound = ubounds[i]
        value = values[i]
        if lbound == "BLANK" or lbound == "HIDDEN": continue
        if i == 0 and value and not ubound:
            catlock = True
        if not value:
            empty_values = True
        if not catlock and is_number(lbound) and is_number(ubound): categorical = False

    if categorical:
        categories = collections.OrderedDict()
        for i in range(0, len(lbounds)):
            lbound = lbounds[i]
            ubound = ubounds[i]
            value = values[i]
            if lbound == "BLANK" or lbound == "HIDDEN": continue
            if value and (not empty_values or i > 0):
                categories[lbound] = value
            else:
                categories[lbound] = lbound
        if categories:
            range_str = ""
            for cod in categories:
                if range_str: range_str = range_str + ";"
                range_str = range_str + cod + ":" + categories[cod]
            var_types[name] = 'category'
            var_ranges[name] = range_str
#             print "Variable",name,"is categorical",range_str
    else:
        min_value = 1E9
        max_value = 0
        special_values = collections.OrderedDict()
        for i in range(0, len(lbounds)):
            lbound = lbounds[i]
            ubound = ubounds[i]
            value = values[i]
            if lbound == "BLANK" or lbound == "HIDDEN": continue
            if lbound and ubound and is_number(lbound) and is_number(ubound):
                min_value = min(min_value, float(lbound))
                max_value = max(max_value, float(ubound))
            elif lbound and value:
                special_values[lbound] = value
        if min_value < max_value:
            range_str = str(int(math.floor(min_value))) + "," + str(int(math.ceil(max_value)))
            for cod in special_values:
                range_str = range_str + ";" + cod + ":" + special_values[cod]
            var_ranges[name] = range_str

def load_metadata(data_file, var_file, code_file, var_names, var_titles, var_types, var_ranges, var_groups, weight_vars):
    print "Loading metadata..."
    reader = csv.reader(open(data_file, "r"), dialect="excel")
    var_names.extend(reader.next())
    for name in var_names:
        var_titles[name] = name
        var_types[name] = 'int'
        var_ranges[name] = '0,100000'

    reader = csv.reader(open(var_file, "rU"), dialect="excel")
    reader.next()
    for row in reader:
        grp_name = row[1].replace("&", "and")
        tbl_name = row[2].replace("&", "and")
        tbl_index = int(row[3])
        var_index = int(row[4])
        var_name = row[5]
        var_title = row[6]

        if var_name in var_names:
            if grp_name == "Weighting" or grp_name == "Land and Cell Raking":
                weight_vars.append(var_name)
#                 print var_name, var_title
            if grp_name in var_groups:
                group = var_groups[grp_name]
            else:
                group = collections.OrderedDict()
                var_groups[grp_name] = group

            if tbl_name in group:
                table = group[tbl_name]
            else:
                table = []
                group[tbl_name] = table

            table.append(var_name)
            var_titles[var_name] = var_title

    reader = csv.reader(open(code_file, "rU"), dialect="excel")
    reader.next()
    name0 = ""
    lbounds = []
    ubounds = []
    values = []
    for row in reader:
        name = row[5]
        lbound = row[8]
        ubound = row[9]
        value = (''.join(char for char in row[10] if ord(char) < 128)).replace(";", "")

        if name in var_names:
            if name0 != name and lbounds:
                set_var_type(name0, lbounds, ubounds, values, var_types, var_ranges)
                lbounds = []
                ubounds = []
                values = []

            lbounds.append(lbound)
            ubounds.append(ubound)
            values.append(value)
            name0 = name

    if name0 and lbounds:
        set_var_type(name0, lbounds, ubounds, values, var_types, var_ranges)

    print "Done"

def load_data(data_file, var_names, var_types, data):
    print "Loading data..."
    reader = csv.reader(open(data_file, "r"), dialect="excel")
    reader.next()
    for row0 in reader:
        row1 = []
        index = 0
        for val0 in row0:
            if val0 == '':
                val1 = missing_str
            else:
                name = var_names[index]
                try:
                    fval = float(val0)
                    if var_types[name] == 'int' and not fval.is_integer():
                        var_types[name] = 'float'
                    val1 = val0
                except ValueError:
                    val1 = missing_str
            row1.append(val1)
            index = index + 1

        data.append(row1)
    print "Done"

def save_dictionary(dict_file, var_names, var_titles, var_types, var_ranges, weight_vars):
    use_weights = "_LLCPWT" in weight_vars
    print "Saving dictionary..."
    dfile = open(dict_file, "w")
    for var in var_names:
        weight_str = ""
        if use_weights:
            weight_str = '\t'
            if var in weight_vars:
                weight_str = weight_str + "sample weight"
            else:
                weight_str = weight_str + "_LLCPWT"

        line = var_titles[var] + '\t' + var_types[var] + '\t' + var_ranges[var] + weight_str +'\n'
        dfile.write(line)
    dfile.close()
    print "Done."

def save_groups(filename, var_groups):
    print "Saving groups..."
    # Writing file in utf-8 because the input html files from
    # NHANES website sometimes have characters output the ASCII range.
    xml_file = codecs.open(filename, 'w', 'utf-8')
    xml_strings = []
    write_xml_line('<?xml version="1.0"?>', xml_file, xml_strings)
    write_xml_line('<data>', xml_file, xml_strings)
    for gname in var_groups:
        if gname in ["State", "Weighting", "Land and Cell Raking"]: continue
        write_xml_line(' <group name="' + gname + '">', xml_file, xml_strings)
        group = var_groups[gname]
        for tname in group:
            write_xml_line('  <table name="' + tname + '">', xml_file, xml_strings)
            table = group[tname]
            for var in table:
                write_xml_line('   <variable name="' + var + '"/>', xml_file, xml_strings)
            write_xml_line('  </table>', xml_file, xml_strings)
        write_xml_line(' </group>', xml_file, xml_strings)
    write_xml_line('</data>', xml_file, xml_strings)
    xml_file.close()

    # XML validation.
    try:
        doc = parseString(''.join(xml_strings))
        doc.toxml()
        print "Done."
    except:
        sys.stderr.write("XML validation error:\n")
        raise

def save_data(data_file, var_names, data):
    print "Saving data..."
    writer = csv.writer(open(data_file, "w"), dialect="excel-tab")
    writer.writerow(var_names)
    for row in data:
        writer.writerow(row)
    print "Done."

##########################################################################################

survey_year = sys.argv[1]

source_folder = "../source_data/vizrisk/"
missing_str = "\\N"
output_folder = "mirador/" + survey_year

var_names = []
weight_vars = []
var_titles = {}
var_types = {}
var_ranges = {}
var_groups = collections.OrderedDict()
data = []

data_file = source_folder + "BRFS" + survey_year + ".csv"
var_file = source_folder + "varlist-" + survey_year + ".csv"
code_file = source_folder + "codebook-" + survey_year + ".csv"

load_metadata(data_file, var_file, code_file, var_names, var_titles, var_types, var_ranges, var_groups, weight_vars);
load_data(data_file, var_names, var_types, data);

save_dictionary(output_folder + "/dictionary.tsv", var_names, var_titles, var_types, var_ranges, weight_vars)
save_groups(output_folder + "/groups.xml", var_groups)
save_data(output_folder + "/data.tsv", var_names, data);
