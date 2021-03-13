package com.gudusoft.grabit;

import com.alibaba.fastjson.JSONObject;
import com.gudusoft.grabit.util.SqlFlowUtil;
import com.gudusoft.grabit.util.DateUtil;
import com.gudusoft.grabit.util.FileUtil;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.io.IOException;
import java.util.Arrays;
import java.util.Date;
import java.util.List;


public class Runner {

    private static final Logger LOG = LoggerFactory.getLogger(Runner.class);

    public static void main(String[] args) throws IOException {
        if (args.length < 2) {
            LOG.error("please enter the correct parameters.");
            return;
        }

        List<String> argList = Arrays.asList(args);
        matchParam("/f", argList);
        String fileVal = detectParam("/f", args, argList);
        File file = new File(fileVal);
        if (!file.exists()) {
            LOG.error("{} is not exist.", file);
            return;
        }

        matchParam("/s", argList);
        String server = detectParam("/s", args, argList);
        if (!server.startsWith("http") && !server.startsWith("https")) {
            server = "http://" + server;
        }
        if (server.endsWith(File.separator)) {
            server = server.substring(0, server.length() - 1);
        }

        if (argList.contains("/p") && argList.size() > argList.indexOf("/p") + 1) {
            server = server + ":" + detectParam("/p", args, argList);
        }

        matchParam("/u", argList);
        String userId = detectParam("/u", args, argList).replace("'", "");

        String userSecret = "";
        if (argList.contains("/k") && argList.size() > argList.indexOf("/k") + 1) {
            userSecret = detectParam("/k", args, argList);
        }

        String databaseType = "dbvoracle";
        if (argList.contains("/t") && argList.size() > argList.indexOf("/t") + 1) {
            databaseType = "dbv" + detectParam("/t", args, argList);
        }

        int resultType = 1;
        if (argList.contains("/r") && argList.size() > argList.indexOf("/r") + 1) {
            resultType = Integer.parseInt(detectParam("/r", args, argList));
        }

        LOG.info("=================  run start grabit ==================");
        run(file, server, userId, userSecret, databaseType, resultType);
        LOG.info("=================  run end grabit ==================");
    }

    private static void run(File file, String server, String userId, String userSecret, String databaseType, Integer resultType) throws IOException {
        String tokenUrl = String.format("%s/gspLive_backend/user/generateToken", server);
        String token = SqlFlowUtil.getToken(tokenUrl, userId, userSecret, 0);
        if ("".equals(token)) {
            LOG.error("connection to sqlflow failed.");
            System.exit(1);
        }

        String path = "";
        if (file.isDirectory()) {
            path = file.getPath() + ".zip";
            FileUtil.toZip(file.getPath(), FileUtil.outStream(path), true);
        } else if (file.isFile()) {
            path = file.getPath();
        }

        String submitUrl = String.format("%s/gspLive_backend/sqlflow/job/submitUserJob", server);
        final String taskName = DateUtil.format(new Date()) + "_" + System.currentTimeMillis();
        String result = SqlFlowUtil.submitJob(path, submitUrl,
                databaseType,
                userId, token,
                taskName);
        JSONObject object = JSONObject.parseObject(result);
        if (null != object) {
            Integer code = object.getInteger("code");
            if (code == 200) {
                JSONObject data = object.getJSONObject("data");
                LOG.info("submit job to sqlflow successful. SQLFlow is being analyzed...");
                String jobId = data.getString("jobId");

                String jsonJobUrl = String.format("%s/gspLive_backend/sqlflow/job/displayUserJobSummary", server);
                while (true) {
                    String statusRs = SqlFlowUtil.getStatus(jsonJobUrl, userId, token, jobId);
                    JSONObject statusObj = JSONObject.parseObject(statusRs);
                    if (null != statusObj) {
                        if (statusObj.getInteger("code") == 200) {
                            JSONObject val = statusObj.getJSONObject("data");
                            String status = val.getString("status");
                            if ("success".equals(status) || "partial_success".equals(status)) {
                                LOG.info("sqlflow analyze successful.");
                                break;
                            }
                            if ("fail".equals(status)) {
                                LOG.error(val.getString("errorMessage"));
                                System.exit(1);
                            }
                        }
                    }
                }

                String rsUrl = "";
                String downLoadPath = "";
                String rootPath = "data" + File.separator + "result" + File.separator + DateUtil.timeStamp2Date(System.currentTimeMillis()) + "_" + jobId;
                switch (resultType) {
                    case 1:
                        rsUrl = String.format("%s/gspLive_backend/sqlflow/job/exportLineageAsJson", server);
                        downLoadPath = rootPath + "_json.json";
                        break;
                    case 2:
                        rsUrl = String.format("%s/gspLive_backend/sqlflow/job/exportLineageAsCsv", server);
                        downLoadPath = rootPath + "_csv.csv";
                        break;
                    case 3:
                        rsUrl = String.format("%s/gspLive_backend/sqlflow/job/exportLineageAsGraphml", server);
                        downLoadPath = rootPath + "_graphml.graphml";
                        break;
                    default:
                        break;
                }

                SqlFlowUtil.ExportLineageReq request = new SqlFlowUtil.ExportLineageReq();
                request.setToken(token);
                request.setJobId(jobId);
                request.setTableToTable(true);
                request.setUserId(userId);
                request.setUrl(rsUrl);
                request.setDownloadFilePath(downLoadPath);

                LOG.info("start export result from sqlflow.");
                result = SqlFlowUtil.exportLineage(request);
                if (!result.contains("success")) {
                    LOG.error("export json result failed");
                    System.exit(1);
                }

                LOG.info("export json result successful,downloaded file path is {}", downLoadPath);
            } else {
                LOG.error("submit job to sqlflow failed.");
                System.exit(1);
            }
        }
    }

    private static String detectParam(String param, String[] args, List<String> argList) {
        try {
            return args[argList.indexOf(param) + 1];
        } catch (Exception e) {
            LOG.error("Please enter the correct parameters.");
            System.exit(1);
        }
        return null;
    }

    private static void matchParam(String param, List<String> argList) {
        if (!argList.contains(param) || argList.size() <= argList.indexOf(param) + 1) {
            LOG.error("{} parameter is required.", param);
            System.exit(1);
        }
    }

}
