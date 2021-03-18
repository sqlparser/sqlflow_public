package com.gudusoft.grabit;

import com.alibaba.fastjson.JSONObject;
import com.gudusoft.grabit.SqlFlowUtil;
import com.gudusoft.grabit.DateUtil;
import com.gudusoft.grabit.FileUtil;

import java.io.File;
import java.io.IOException;
import java.util.Arrays;
import java.util.Date;
import java.util.List;


public class Runner {


    public static void main(String[] args) throws IOException {
        if (args.length < 2) {
            System.err.println("please enter the correct parameters.");
            return;
        }

        List<String> argList = Arrays.asList(args);
        matchParam("/f", argList);
        String fileVal = detectParam("/f", args, argList);
        File file = new File(fileVal);
        if (!file.exists()) {
            System.err.println("{} is not exist." + file);
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
            if ("dbvsqlserver".equalsIgnoreCase(databaseType)) {
                databaseType = "dbvmssql";
            }
        }

        int resultType = 1;
        if (argList.contains("/r") && argList.size() > argList.indexOf("/r") + 1) {
            resultType = Integer.parseInt(detectParam("/r", args, argList));
        }

        System.out.println("=================  run start grabit ==================");
        run(file, server, userId, userSecret, databaseType, resultType);
        System.out.println("=================  run end grabit ==================");
    }

    private static void run(File file, String server, String userId, String userSecret, String databaseType, Integer resultType) throws IOException {
        String tokenUrl = String.format("%s/gspLive_backend/user/generateToken", server);
        String token = SqlFlowUtil.getToken(tokenUrl, userId, userSecret, 0);
        if ("".equals(token)) {
            System.err.println("connection to sqlflow failed.");
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
                System.out.println("submit job to sqlflow successful. SQLFlow is being analyzed...");
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
                                System.out.println("sqlflow analyze successful.");
                                break;
                            }
                            if ("fail".equals(status)) {
                                System.err.println(val.getString("errorMessage"));
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

                System.out.println("start export result from sqlflow.");
                result = SqlFlowUtil.exportLineage(request);
                if (!result.contains("success")) {
                    System.err.println("export json result failed");
                    System.exit(1);
                }

                System.out.println("export json result successful,downloaded file path is {}" + downLoadPath);
            } else {
                System.err.println("submit job to sqlflow failed.");
                System.exit(1);
            }
        }
    }

    private static String detectParam(String param, String[] args, List<String> argList) {
        try {
            return args[argList.indexOf(param) + 1];
        } catch (Exception e) {
            System.err.println("Please enter the correct parameters.");
            System.exit(1);
        }
        return null;
    }

    private static void matchParam(String param, List<String> argList) {
        if (!argList.contains(param) || argList.size() <= argList.indexOf(param) + 1) {
            System.err.println("{} parameter is required." + param);
            System.exit(1);
        }
    }

}
