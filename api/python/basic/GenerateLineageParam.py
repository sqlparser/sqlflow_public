import zipfile
import sys
import os


def toZip(start_dir):
    if start_dir.endswith(os.sep):
        start_dir = start_dir[:-1]
    start_dir = start_dir
    file_news = start_dir + '.zip'

    z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)
    for dir_path, dir_names, file_names in os.walk(start_dir):
        f_path = dir_path.replace(start_dir, '')
        f_path = f_path and f_path + os.sep or ''
        for filename in file_names:
            z.write(os.path.join(dir_path, filename), f_path + filename)
    z.close()
    return file_news


def buildSqltextParam(userId, token, delimiter, export_include_table, showConstantTable,
                      treatArgumentsInCountFunctionAsDirectDataflow, dbvendor, sqltext):
    data = {'dbvendor': dbvendor, 'token': token, 'userId': userId}
    if delimiter != '':
        data['delimiter'] = delimiter
    if export_include_table != '':
        data['export_include_table'] = export_include_table
    if showConstantTable != '':
        data['showConstantTable'] = showConstantTable
    if treatArgumentsInCountFunctionAsDirectDataflow != '':
        data['treatArgumentsInCountFunctionAsDirectDataflow'] = treatArgumentsInCountFunctionAsDirectDataflow
    if sqltext != '':
        data['sqltext'] = sqltext
    return data


def buildSqlfileParam(userId, token, delimiter, export_include_table, showConstantTable,
                      treatArgumentsInCountFunctionAsDirectDataflow, dbvendor, sqlfile):
    files = ''
    if sqlfile != '':
        if os.path.isdir(sqlfile):
            print('The SQL file cannot be a directory.')
            sys.exit(0)
        files = {'sqlfile': open(sqlfile, 'rb')}

    data = {'dbvendor': dbvendor, 'token': token, 'userId': userId}
    if delimiter != '':
        data['delimiter'] = delimiter
    if export_include_table != '':
        data['export_include_table'] = export_include_table
    if showConstantTable != '':
        data['showConstantTable'] = showConstantTable
    if treatArgumentsInCountFunctionAsDirectDataflow != '':
        data['treatArgumentsInCountFunctionAsDirectDataflow'] = treatArgumentsInCountFunctionAsDirectDataflow
    return data, files

