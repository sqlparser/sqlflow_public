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
using System.Diagnostics;

namespace SQLFlowClient
{
    public static class HttpService
    {
        private static Config config;

        public static async Task Request(Options options)
        {
            config = new Config
            {
                Host = "https://api.gudusoft.com",
                Token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJndWR1c29mdCIsImV4cCI6MTYwMzc1NjgwMCwiaWF0IjoxNTcyMjIwODAwfQ.EhlnJO7oqAHdr0_bunhtrN-TgaGbARKvTh2URTxu9iU"
            };
            try
            {
                if (File.Exists("./config.json"))
                {
                    var json = JObject.Parse(File.ReadAllText("./config.json"));
                    if (json["Host"] != null && json["Host"].ToString() != "")
                    {
                        config.Host = json["Host"].ToString();
                    }
                    if (json["Token"] != null && json["Token"].ToString() != "")
                    {
                        config.Token = json["Token"].ToString();
                    }
                }
            }
            catch (Exception e)
            {
                Console.WriteLine($"Invalid config.json :\n{e.Message}");
                return;
            }
            if (options.Version)
            {
                await Version();
            }
            else
            {
                await SQLFlow(options);
            }

        }

        public static async Task SQLFlow(Options options)
        {
            StreamContent sqlfile;
            if (options.SQLFile == null)
            {
                Console.WriteLine($"Please specify an input file. (e.g. SQLFlowClient test.sql)");
                return;
            }
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
                { new StringContent(options.IgnoreRecordSet.ToString())  , "ignoreRecordSet"  },
                { new StringContent(options.ignoreFunction.ToString())   , "ignoreFunction"   },
            };
            try
            {
                var stopWatch = Stopwatch.StartNew();
                string url = $"{config.Host}/gspLive_backend/sqlflow/generation/sqlflow/" + (options.IsGraph ? "graph" : "");
                using var client = new HttpClient();
                client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Token", config.Token);
                using var response = await client.PostAsync(url, form);
                if (response.IsSuccessStatusCode)
                {
                    stopWatch.Stop();
                    var text = await response.Content.ReadAsStringAsync();
                    var result = new SQLFlowResult(text);
                    if (result.data && result.dbobjs || result.data && result.sqlflow && result.graph)
                    {
                        if (options.Output != "")
                        {
                            try
                            {
                                File.WriteAllText(Path.GetFullPath(options.Output), result.json);
                                Console.WriteLine($"Output has been saved to {options.Output}.");
                            }
                            catch (Exception e)
                            {
                                Console.WriteLine($"Save File failed.{e.Message}");
                            }
                        }
                        else
                        {
                            Console.WriteLine(result.json ?? "");
                        }
                    }
                    if (result.error)
                    {
                        Console.WriteLine($"Success with some errors.Executed in {stopWatch.Elapsed.TotalSeconds.ToString("0.00")} seconds by host {config.Host}.");
                    }
                    else
                    {
                        Console.WriteLine($"Success.Executed in {stopWatch.Elapsed.TotalSeconds.ToString("0.00")} seconds by host {config.Host}.");
                    }
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

        public static async Task Version()
        {
            try
            {
                string url = $"{config.Host}/gspLive_backend/version";
                using var client = new HttpClient();
                client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Token", config.Token);
                using var response = await client.PostAsync(url, new StringContent(""));
                if (response.IsSuccessStatusCode)
                {
                    var text = await response.Content.ReadAsStringAsync();
                    var json = JObject.Parse(text);
                    var gsp = new
                    {
                        ReleaseDate = json.SelectToken("version.gsp.['release.date']")?.ToString(),
                        version = json.SelectToken("version.gsp.version")?.ToString(),
                    };
                    var backend = new
                    {
                        ReleaseDate = json.SelectToken("version.backend.['release.date']")?.ToString(),
                        version = json.SelectToken("version.backend.version")?.ToString(),
                    };
                    Console.WriteLine("                 version        relase date");
                    Console.WriteLine("SQLFlowClient    1.1.0          2020/10/12");
                    Console.WriteLine($"gsp              {gsp.version}        {gsp.ReleaseDate}");
                    Console.WriteLine($"backend         {backend.version}         {backend.ReleaseDate}");
                }
                else
                {
                    Console.WriteLine($"Not connected.Wrong response code {(int)response.StatusCode} {response.StatusCode}.");
                }
            }
            catch (Exception e)
            {
                Console.WriteLine($"An unknonwn exeception occurs :\n{e.Message}");
            }
        }
    }
}
