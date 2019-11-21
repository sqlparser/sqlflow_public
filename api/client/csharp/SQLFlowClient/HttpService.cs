using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using System.Linq;
using System.Net.Http.Headers;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System.IO;

namespace SQLFlowClient
{
    public static class HttpService
    {
        public static async Task Request(Options options)
        {
            Config config;
            try
            {
                var json = JObject.Parse(File.ReadAllText("./config.json"));
                if (json["Host"] == null || json["Host"].ToString() == "")
                {
                    throw new Exception("Invalid host.");
                }
                if (json["Token"] == null || json["Token"].ToString() == "")
                {
                    throw new Exception("Invalid token.");
                }
                config = json.ToObject<Config>();
            }
            catch (Exception e)
            {
                Console.WriteLine($"Invalid config.json :\n{e.Message}");
                return;
            }
            StreamContent sqlfile;
            try
            {
                string path = Path.GetFullPath(options.SQLFile);
                sqlfile = new StreamContent(File.Open(options.SQLFile, FileMode.Open));
            }
            catch (Exception e)
            {
                Console.WriteLine($"Open file failed.\n{e.Message}");
                return;
            }
            var types = options.ShowRelationType.Split(",")
                .Where(p => Enum.GetNames(typeof(RelationType)).FirstOrDefault(t => t.ToLower() == p.ToLower()) == null)
                .ToList();
            if (types.Count != 0)
            {
                Console.WriteLine($"Wrong relation type : { string.Join(",", types) }.\nIt should be one or more from the following list : fdd, fdr, frd, fddi, join");
                return;
            }
            string dbvendor = Enum.GetNames(typeof(DBVendor)).FirstOrDefault(p => p.ToLower() == options.DBVendor.ToLower());
            if (dbvendor == null)
            {
                Console.WriteLine($"Wrong database vendor : {options.DBVendor}.\nIt should be one of the following list : " +
                    $"bigquery, couchbase, db2, greenplum, hana , hive, impala , informix, mdx, mysql, netezza, openedge," +
                    $" oracle, postgresql, redshift, snowflake, mssql, sybase, teradata, vertica");
                return;
            }
            var form = new MultipartFormDataContent{
                { sqlfile                                                , "sqlfile"           , "sqlfile" },
                { new StringContent("dbv"+dbvendor)                      , "dbvendor"         },
                { new StringContent(options.ShowRelationType)            , "showRelationType" },
                { new StringContent(options.SimpleOutput.ToString())     , "simpleOutput"     },
            };
            try
            {
                string url = $"{config.Host}/gspLive_backend/sqlflow/generation/sqlflow/" + (options.IsGraph ? "graph" : "");
                using var client = new HttpClient();
                client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Token", config.Token);
                using var response = await client.PostAsync(url, form);
                var text = await response.Content.ReadAsStringAsync();
                var json = JObject.Parse(text);
                var data = json["data"]?.ToString();
                if (json["error"]?.ToString() != null)
                {
                    Console.WriteLine($"{json["message"]?.ToString() ?? ""}");
                }
                else if (data != null)
                {
                    Console.WriteLine(data ?? "");
                }
                else
                {
                    Console.WriteLine($"Wrong response code {(int)response.StatusCode} {response.StatusCode}.");
                }
            }
            catch (Exception e)
            {
                Console.WriteLine($"An unknonwn exeception occurs :\n{e.Message}");
            }
        }
    }
}
