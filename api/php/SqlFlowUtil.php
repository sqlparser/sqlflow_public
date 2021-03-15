<?php
include('HttpClient.php');

class SqlFlowUtil
{
    function getToken($server, $userId, $userSecret)
    {
        if ($userId == 'gudu|0123456789') {
            return 'token';
        }

        $httpVendor = new HttpClient();
        $json['userId'] = $userId;
        $json['secretKey'] = $userSecret;
        $url = $server . '/gspLive_backend/user/generateToken';
        $result = $httpVendor->postFrom($url, $json);
        return $result['token'];
    }

    function submitJob($server, $userId, $token, $sqlfiles, $jobName, $dbvendor)
    {
        $httpVendor = new HttpClient();
        $params = array(
            'userId' => $userId,
            'token' => $token,
            'jobName' => $jobName,
            'dbvendor' => $dbvendor,
            'filename' => $jobName,
            'sqlfiles' => file_get_contents($sqlfiles)
        );
        $url = $server . '/gspLive_backend/sqlflow/job/submitUserJob';
        $result = $httpVendor->postFile($url, $params);
        return $result;
    }

    function getStatus($server, $userId, $token, $jobId)
    {
        $httpVendor = new HttpClient();
        $json['userId'] = $userId;
        $json['token'] = $token;
        $json['jobId'] = $jobId;
        $url = $server . '/gspLive_backend/sqlflow/job/displayUserJobSummary';
        $result = $httpVendor->postFrom($url, $json);
        return $result;
    }

    function getResult($server, $userId, $token, $jobId, $download)
    {
        $dir = 'data' . DIRECTORY_SEPARATOR . 'result';
        $str = $dir . DIRECTORY_SEPARATOR . date("Ymd") . '_' . $jobId;
        $filePath = '';
        $url = '';
        if ($download == 1) {
            $url = $server . '/gspLive_backend/sqlflow/job/exportLineageAsJson';
            $filePath = $str . '_json.json';
        } else if ($download == 2) {
            $url = $server . '/gspLive_backend/sqlflow/job/exportLineageAsGraphml';
            $filePath = $str . '_graphml.graphml';
        } else if ($download == 3) {
            $url = $server . '/gspLive_backend/sqlflow/job/exportLineageAsCsv';
            $filePath = $str . '_csv.csv';
        }

        $httpVendor = new HttpClient();
        $json['userId'] = $userId;
        $json['token'] = $token;
        $json['jobId'] = $jobId;
        $httpVendor->mkdirs($dir);
        $httpVendor->postJson($url, $json, $filePath);
        return $filePath;
    }
}
