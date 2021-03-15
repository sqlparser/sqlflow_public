<?php


class Grabit
{

    function run($argv)
    {
        if (sizeof($argv) < 2) {
            echo 'please enter the correct parameters.';
            exit(1);
        }

        $userSecret = '';
        $userId = '';
        $dbvendor = '';
        $sqlfiles = '';
        $server = '';
        $port = '';
        $download = 1;
        for ($i = 0; $i < sizeof($argv) - 1; $i++) {
            if ($argv[$i] == '/s') {
                $server = $argv[$i + 1];
            }
            if ($argv[$i] == '/p') {
                $port = $argv[$i + 1];
            }
            if ($argv[$i] == '/f') {
                $sqlfiles = $argv[$i + 1];
                if (!file_exists($sqlfiles)) {
                    echo "The file is no exists";
                    exit(1);
                }
            }
            if ($argv[$i] == '/u') {
                $userId = $argv[$i + 1];
                $userId = str_replace("'", '', $userId);
            }
            if ($argv[$i] == '/t') {
                $dbvendor = 'dbv' . $argv[$i + 1];
                if ($dbvendor == 'dbvsqlserver') {
                    $dbvendor = 'dbvmssql';
                }
            }
            if ($argv[$i] == '/k') {
                $userSecret = $argv[$i + 1];
            }
            if ($argv[$i] == '/r') {
                $download = $argv[$i + 1];
            }
        }

        if (!substr($server, 0, 4) === "http" && !substr($server, 0, 5) === "https") {
            $server = "http://" . $server;
        }
        if (substr($server, -strlen(DIRECTORY_SEPARATOR)) === DIRECTORY_SEPARATOR) {
            $server = substr($server, 0, strlen($server) - 1);
        }
        if ($port != '') {
            $server = $server . ':' . $port;
        }

        echo '===================================== start =====================================';
        echo PHP_EOL;

        echo('start get token.');
        echo PHP_EOL;

        include('SqlFlowUtil.php');
        $obj = new SqlFlowUtil();
        $token = $obj->getToken($server, $userId, $userSecret);
        echo 'get token successful.';
        echo PHP_EOL;
        if (is_dir($sqlfiles)) {
            if (substr($sqlfiles, -strlen(DIRECTORY_SEPARATOR)) === DIRECTORY_SEPARATOR) {
                $sqlfiles = rtrim($sqlfiles, DIRECTORY_SEPARATOR);
            }

            $zip = new \ZipArchive();
            $sqlfileDir = $sqlfiles . '.zip';
            if (file_exists($sqlfileDir)) {
                if (PATH_SEPARATOR == ':') {
                    unlink($sqlfileDir);
                } else {
                    $url = iconv('utf-8', 'gbk', $sqlfileDir);
                    unlink($url);
                }
            }

            $open = $zip->open($sqlfileDir, \ZipArchive::CREATE);
            if ($open === true) {
                $this->toZip($sqlfiles, $zip);
                $zip->close();
            }
            $sqlfiles = $sqlfileDir;
        }

        echo 'start submit job.';
        echo PHP_EOL;

        $result = $obj->submitJob($server, $userId, $token, $sqlfiles, time(), $dbvendor);
        if ($result['code'] == 200) {
            echo 'submit job successful.';
            echo PHP_EOL;

            $jobId = $result['data']['jobId'];
            while (true) {
                $result = $obj->getStatus($server, $userId, $token, $jobId);
                if ($result['code'] == 200) {
                    $status = $result['data']['status'];
                    if ($status == 'partial_success' || $status == 'success') {
                        break;
                    }
                    if ($status == 'fail') {
                        echo 'job execution failed.';
                        exit(1);
                    }
                }
            }
            echo $status;
            echo 'start get result from sqlflow.';
            echo PHP_EOL;
            $filePath = $obj->getResult($server, $userId, $token, $jobId, $download);
            echo 'get result from sqlflow successful. file path is : ' . $filePath;
        } else {
            echo 'submit job failed.';
        }
        echo PHP_EOL;
        echo '===================================== end =====================================';
    }

    function toZip($path, $zip)
    {
        $handler = opendir($path);
        while (($filename = readdir($handler)) !== false) {
            if ($filename != "." && $filename != "..") {
                if (is_dir($path . DIRECTORY_SEPARATOR . $filename)) {
                    $obj = new Grabit();
                    $obj->toZip($path . DIRECTORY_SEPARATOR . $filename, $zip);
                } else {
                    $zip->addFile($path . DIRECTORY_SEPARATOR . $filename);
                    $zip->renameName($path . DIRECTORY_SEPARATOR . $filename, $filename);
                }
            }
        }
        @closedir($path);
    }
}

$obj = new Grabit();
$obj->run($argv);
