<?php


class HttpClient
{

    protected static $url;
    protected static $delimiter;

    function mkdirs($a1, $mode = 0777)
    {
        if (is_dir($a1) || @mkdir($a1, $mode)) return TRUE;
        if (!static::mkdirs(dirname($a1), $mode)) return FALSE;
        return @mkdir($a1, $mode);
    }


    public function __construct()
    {
        static::$delimiter = uniqid();
    }

    private static function buildData($param)
    {
        $data = '';
        $eol = "\r\n";
        $upload = $param['sqlfiles'];
        unset($param['sqlfiles']);

        foreach ($param as $name => $content) {
            $data .= "--" . static::$delimiter . "\r\n"
                . 'Content-Disposition: form-data; name="' . $name . "\"\r\n\r\n"
                . $content . "\r\n";
        }
        $data .= "--" . static::$delimiter . $eol
            . 'Content-Disposition: form-data; name="sqlfiles"; filename="' . $param['filename'] . '"' . "\r\n"
            . 'Content-Type:application/octet-stream' . "\r\n\r\n";

        $data .= $upload . "\r\n";
        $data .= "--" . static::$delimiter . "--\r\n";
        return $data;
    }

    function postFile($url, $param)
    {
        $post_data = static::buildData($param);
        $curl = curl_init($url);
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($curl, CURLOPT_POST, true);
        curl_setopt($curl, CURLOPT_POSTFIELDS, $post_data);
        curl_setopt($curl, CURLOPT_HTTPHEADER, [
            "Content-Type: multipart/form-data; boundary=" . static::$delimiter,
            "Content-Length: " . strlen($post_data)
        ]);
        $response = curl_exec($curl);
        curl_close($curl);
        $info = json_decode($response, true);
        return $info;
    }


    function postFrom($url, $data)
    {
        $headers = array('Content-Type: application/x-www-form-urlencoded');
        $curl = curl_init();
        curl_setopt($curl, CURLOPT_URL, $url);
        curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, 0);
        curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, 0);
        curl_setopt($curl, CURLOPT_FOLLOWLOCATION, 1);
        curl_setopt($curl, CURLOPT_AUTOREFERER, 1);
        curl_setopt($curl, CURLOPT_POST, 1);
        curl_setopt($curl, CURLOPT_POSTFIELDS, http_build_query($data));
        curl_setopt($curl, CURLOPT_TIMEOUT, 30);
        curl_setopt($curl, CURLOPT_HEADER, 0);
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($curl, CURLOPT_HTTPHEADER, $headers);
        $result = curl_exec($curl);
        if (curl_errno($curl)) {
            return 'Errno' . curl_error($curl);
        }
        curl_close($curl);
        return json_decode($result, true);
    }


    function postJson($url, $data, $filePath)
    {
        $headers = array('Content-Type: application/x-www-form-urlencoded');
        $curl = curl_init();
        curl_setopt($curl, CURLOPT_URL, $url);
        curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, 0);
        curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, 0);
        curl_setopt($curl, CURLOPT_FOLLOWLOCATION, 1);
        curl_setopt($curl, CURLOPT_AUTOREFERER, 1);
        curl_setopt($curl, CURLOPT_POST, 1);
        curl_setopt($curl, CURLOPT_POSTFIELDS, http_build_query($data));
        curl_setopt($curl, CURLOPT_TIMEOUT, 30);
        curl_setopt($curl, CURLOPT_HEADER, 0);
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($curl, CURLOPT_HTTPHEADER, $headers);
        $result = curl_exec($curl);
        if (curl_errno($curl)) {
            return 'Errno' . curl_error($curl);
        }
        $fp = @fopen($filePath, "a");
        fwrite($fp, $result);
        fclose($fp);
    }

}
