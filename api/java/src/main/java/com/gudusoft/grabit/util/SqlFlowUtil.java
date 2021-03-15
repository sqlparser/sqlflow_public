package com.gudusoft.grabit.util;

import com.alibaba.fastjson.JSONObject;
import org.apache.http.HttpEntity;
import org.apache.http.NameValuePair;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.ContentType;
import org.apache.http.entity.mime.MultipartEntityBuilder;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class SqlFlowUtil {

    private static final Logger LOG = LoggerFactory.getLogger(SqlFlowUtil.class);

    private static String token = "";

    private SqlFlowUtil() {
    }

    public static String getToken(String url, String userId,
                                  String secretKey, Integer flag) {
        try {
            LOG.info("start get token from sqlflow.");
            Map<String, String> param = new HashMap<>();
            param.put("secretKey", secretKey);
            param.put("userId", userId);
            if ("gudu|0123456789".equals(userId)) {
                return "token";
            }
            String result = doPost(url, param);
            JSONObject object = JSONObject.parseObject(result);
            if ("200".equals(object.getString("code"))) {
                token = object.getString("token");
                LOG.info("get token from sqlflow successful.");
                return token;
            }
            return "";
        } catch (Exception e) {
            if (flag == 0) {
                if (url.startsWith("http:")) {
                    url = url.replace("http", "https");
                }
                return getToken(url, userId,
                        secretKey, 1);
            }
            if (flag == 1) {
                LOG.error("get token from sqlflow failed.", e);
            }
            return token;
        }
    }

    public static String submitJob(String filePath,
                                   String url,
                                   String dbVendor,
                                   String userId,
                                   String token,
                                   String jobName) throws IOException {
        LOG.info("start submit job to sqlflow.");
        CloseableHttpClient httpClient = HttpClients.createDefault();
        HttpPost uploadFile = new HttpPost(url);
        MultipartEntityBuilder builder = MultipartEntityBuilder.create();
        builder.addTextBody("dbvendor", dbVendor, ContentType.TEXT_PLAIN);
        builder.addTextBody("jobName", jobName, ContentType.TEXT_PLAIN);
        builder.addTextBody("token", token, ContentType.TEXT_PLAIN);
        builder.addTextBody("userId", userId, ContentType.TEXT_PLAIN);
        File f = new File(filePath);
        builder.addBinaryBody("sqlfiles", new FileInputStream(f), ContentType.APPLICATION_OCTET_STREAM, f.getName());

        HttpEntity multipart = builder.build();
        uploadFile.setEntity(multipart);
        CloseableHttpResponse response = httpClient.execute(uploadFile);
        HttpEntity responseEntity = response.getEntity();
        return EntityUtils.toString(responseEntity, "UTF-8");
    }


    public static String getStatus(String url,
                                   String userId,
                                   String token,
                                   String jobId) throws IOException {
        CloseableHttpClient httpClient = HttpClients.createDefault();
        HttpPost uploadFile = new HttpPost(url);
        MultipartEntityBuilder builder = MultipartEntityBuilder.create();
        builder.addTextBody("jobId", jobId, ContentType.TEXT_PLAIN);
        builder.addTextBody("token", token, ContentType.TEXT_PLAIN);
        builder.addTextBody("userId", userId, ContentType.TEXT_PLAIN);

        HttpEntity multipart = builder.build();
        uploadFile.setEntity(multipart);
        CloseableHttpResponse response = httpClient.execute(uploadFile);
        HttpEntity responseEntity = response.getEntity();
        return EntityUtils.toString(responseEntity, "UTF-8");
    }


    public static String exportLineage(ExportLineageReq req) throws IOException {
        CloseableHttpClient httpClient = HttpClients.createDefault();
        HttpPost uploadFile = new HttpPost(req.getUrl());
        MultipartEntityBuilder builder = MultipartEntityBuilder.create();
        builder.addTextBody("jobId", req.getJobId(), ContentType.TEXT_PLAIN);
        builder.addTextBody("userId", req.getUserId(), ContentType.TEXT_PLAIN);
        builder.addTextBody("token", req.getToken(), ContentType.TEXT_PLAIN);
        builder.addTextBody("tableToTable", String.valueOf(req.getTableToTable()), ContentType.TEXT_PLAIN);

        HttpEntity multipart = builder.build();
        uploadFile.setEntity(multipart);
        CloseableHttpResponse response = httpClient.execute(uploadFile);

        HttpEntity responseEntity = response.getEntity();

        InputStream in = responseEntity.getContent();
        FileUtil.mkFile(req.getDownloadFilePath());
        File file = new File(req.getDownloadFilePath());
        FileOutputStream fout = new FileOutputStream(file);
        int a;
        byte[] tmp = new byte[1024];
        while ((a = in.read(tmp)) != -1) {
            fout.write(tmp, 0, a);
        }
        fout.flush();
        fout.close();
        in.close();
        return "download success, path:" + req.getDownloadFilePath();
    }


    private static String doPost(String url, Map<String, String> param) {
        CloseableHttpClient httpClient = HttpClients.createDefault();
        CloseableHttpResponse response = null;
        String resultString = "";
        try {
            HttpPost httpPost = new HttpPost(url);
            if (param != null) {
                List<NameValuePair> paramList = new ArrayList<>();
                for (String key : param.keySet()) {
                    paramList.add(new BasicNameValuePair(key, param.get(key)));
                }
                UrlEncodedFormEntity entity = new UrlEncodedFormEntity(paramList, "utf-8");
                httpPost.setEntity(entity);
            }
            response = httpClient.execute(httpPost);
            resultString = EntityUtils.toString(response.getEntity(), "utf-8");
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            try {
                response.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        return resultString;
    }

    public static class ExportLineageReq {

        private String jobId;
        private String userId;
        private String token;

        private String url;
        private String downloadFilePath;
        private Boolean tableToTable = false;

        public String getJobId() {
            return jobId;
        }

        public void setJobId(String jobId) {
            this.jobId = jobId;
        }

        public String getUserId() {
            return userId;
        }

        public void setUserId(String userId) {
            this.userId = userId;
        }

        public String getToken() {
            return token;
        }

        public void setToken(String token) {
            this.token = token;
        }

        public Boolean getTableToTable() {
            return tableToTable;
        }

        public void setTableToTable(Boolean tableToTable) {
            this.tableToTable = tableToTable;
        }

        public String getUrl() {
            return url;
        }

        public void setUrl(String url) {
            this.url = url;
        }

        public String getDownloadFilePath() {
            return downloadFilePath;
        }

        public void setDownloadFilePath(String downloadFilePath) {
            this.downloadFilePath = downloadFilePath;
        }
    }

}


