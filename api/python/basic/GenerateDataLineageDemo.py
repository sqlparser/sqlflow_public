#!/usr/bin/python
# -*- coding: UTF-8 -*-
import zipfile

import requests
import time
import json
import sys
import os


def toSqlflow(userId, token, server, port, jobName, dbvendor, sqlfiles):
	url = '/gspLive_backend/sqlflow/job/submitUserJob'

	if port != '':
		url = server + ':' + port + url
	else:
		url = server + url

	if os.path.isdir(sqlfiles):
		sqlfiles = toZip(sqlfiles)
	files = {'sqlfiles': open(sqlfiles, 'rb')}
	data = {'dbvendor': dbvendor, 'jobName': jobName, 'token': token, 'userId': userId}
	datastr = json.dumps(data)

	print('start submit job to sqlflow.')

	try:
		response = requests.post(url, data=eval(datastr), files=files)
	except Exception:
		print('submit job to sqlflow failed.')
		sys.exit(0)

	result = json.loads(response.text)

	if result['code'] == 200:
		print('submit job to sqlflow successful.')
		return result['data']['jobId']
	else:
		print(result['error'])
		sys.exit(0)


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


def getToken(userId, server, port,screctKey):

	if userId == 'gudu|0123456789':
		return 'token'

	url = '/gspLive_backend/user/generateToken'
	if port != '':
		url = server + ':' + port + url
	else:
		url = server + url
	mapA = {'secretKey': screctKey, 'userId': userId}
	header_dict = {"Content-Type": "application/x-www-form-urlencoded"}

	print('start get token.')
	try:
		r = requests.post(url, data=mapA, headers=header_dict)
		print(r)
	except Exception:
		print('get token failed.')
	result = json.loads(r.text)

	if result['code'] == '200':
		print('get token successful.')
		return result['token']
	else:
		print(result['error'])


def getResult(dataLineageFileType, userId, token, server, port, jobId, filePath):
	sep = 'data' + os.sep + 'result' + os.sep
	filePath = filePath + '_' + jobId
	if dataLineageFileType == 'json':
		url = "/gspLive_backend/sqlflow/job/exportLineageAsJson"
		filePath = sep + filePath + '_json.json'
	elif dataLineageFileType == 'graphml':
		url = "/gspLive_backend/sqlflow/job/exportLineageAsGraphml"
		filePath = sep + filePath + '_graphml.graphml'
	elif dataLineageFileType == 'csv':
		url = "/gspLive_backend/sqlflow/job/exportLineageAsCsv"
		filePath = sep + filePath + '_csv.csv'
	else:
		url = "/gspLive_backend/sqlflow/job/exportLineageAsJson"
		filePath = sep + filePath + '_json.json'

	if port != '':
		url = server + ':' + port + url
	else:
		url = server + url

	data = {'jobId': jobId, 'token': token, 'userId': userId, 'tableToTable': 'false'}
	datastr = json.dumps(data)

	print('start download result to sqlflow.')
	try:
		response = requests.post(url, data=eval(datastr))
	except Exception:
		print('download result to sqlflow failed.')
		sys.exit(0)

	if not os.path.exists(sep):
		os.makedirs(sep)

	try:
		with open(filePath, 'wb') as f:
			f.write(response.content)
	except Exception:
		print(filePath, 'is not exist.')
		sys.exit(0)

	print('download result to sqlflow successful.file path is ', filePath)



def getStatus(userId, token, server, port, jobId):
	url = "/gspLive_backend/sqlflow/job/displayUserJobSummary"

	if port != '':
		url = server + ':' + port + url
	else:
		url = server + url

	data = {'jobId': jobId, 'token': token, 'userId': userId}
	datastr = json.dumps(data)

	try:
		response = requests.post(url, data=eval(datastr))
	except Exception:
		print('get job status to sqlflow failed.')
		sys.exit(0)

	result = json.loads(response.text)
	if result['code'] == 200:
		status = result['data']['status']
		if status == 'fail':
			print(result['data']['errorMessage'])
			sys.exit(0)
		return status


if __name__ == '__main__':
	if len(sys.argv) < 1:
		print('Please enter the args.')
		sys.exit(0)

    # the user id of sqlflow web or client, required true
	userId = ''

    # the secret key of sqlflow user for webapi request, required true
	screctKey = ''

    
    # sqlflow server
	server = ''

    # sqlflow api port
	port = ''

    # database type
	dbvendor = 'dbvmysql'

	sqlfile = ''
	dataLineageFileType = ''
	for i in range(1, len(sys.argv)):
		if sys.argv[i] == '/f':
			try:
				if sys.argv[i + 1] is not None:
					sqlfile = sys.argv[i + 1]
			except Exception:
				print('Please enter the sqlfile path，required true. eg: /f sql.txt')
				sys.exit(0)
		elif sys.argv[i] == '/o':
			try:
				if sys.argv[i + 1] is not None:
					dataLineageFileType = sys.argv[i + 1]
			except Exception:
				dataLineageFileType = 'json'

	token = getToken(userId, server, port, screctKey);

    # sqlflow job name
	jobName = 'test'
	jobId = toSqlflow(userId, token, server, port, jobName, dbvendor, sqlfile)

	while 1==1:
		status = getStatus(userId, token, server, port, jobId)
		if status == 'fail':
			print('job execute failed.')
			break;
		elif status == 'success':
			print('job execute successful.')
			break;
		elif status == 'partial_success':
			print('job execute partial successful.')
			break;
		time.sleep(2)

    # data lineage file path
	filePath = 'datalineage'
	getResult(dataLineageFileType, userId, token, server, port, jobId, filePath)
