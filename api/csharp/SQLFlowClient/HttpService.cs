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
                Token = "",
                UserId = "gudu|0123456789",
            };
            try
            {
                if (File.Exists("./config.json"))
                {
                    var json = JObject.Parse(File.ReadAllText("./config.json"));
                    if (!string.IsNullOrWhiteSpace(json["Host"]?.ToString()))
                    {
                        config.Host = json["Host"].ToString();
                    }
                    if (!string.IsNullOrWhiteSpace(json["Token"]?.ToString()))
                    {
                        config.Token = json["Token"].ToString();
                    }
                    if (!string.IsNullOrWhiteSpace(json["SecretKey"]?.ToString()))
                    {
                        config.SecretKey = json["SecretKey"].ToString();
                    }
                    if (!string.IsNullOrWhiteSpace(json["UserId"]?.ToString()))
                    {
                        config.UserId = json["UserId"].ToString();
                    }
                }
            }
            catch (Exception e)
            {
                Console.WriteLine($"Invalid config.json :\n{e.Message}");
                return;
            }
            //if (!string.IsNullOrWhiteSpace(options.Token))
            //{
            //    config.Token = options.Token;
            //}
            //if (!string.IsNullOrWhiteSpace(options.UserId))
            //{
            //    config.UserId = options.UserId;
            //}
            //if (!string.IsNullOrWhiteSpace(options.SecretKey))
            //{
            //    config.SecretKey = options.SecretKey;
            //}
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
            if (!string.IsNullOrWhiteSpace(config.SecretKey) && !string.IsNullOrWhiteSpace(config.UserId))
            {
                // request token
                string url2 = $"{config.Host}/gspLive_backend/user/generateToken";
                using var client2 = new HttpClient();
                using var response2 = await client2.PostAsync(url2, content: new FormUrlEncodedContent(new List<KeyValuePair<string, string>>
                {
                    new KeyValuePair<string, string>("userId", config.UserId),
                    new KeyValuePair<string, string>("secretKey", config.SecretKey)
                }));
                if (response2.IsSuccessStatusCode)
                {
                    var text = await response2.Content.ReadAsStringAsync();
                    var jobject = JObject.Parse(text);
                    var json = jobject.ToString();
                    var code = jobject.SelectToken("code");
                    if (code?.ToString() == "200")
                    {
                        config.Token = jobject.SelectToken("token").ToString();
                    }
                    else
                    {
                        Console.WriteLine($"{url2} error, code={code?.ToString() }");
                        return;
                    }
                }
                else
                {
                    Console.WriteLine($"Wrong response code {(int)response2.StatusCode} {response2.StatusCode}.url={url2}");
                    return;
                }

            }
            var form = new MultipartFormDataContent{
                { sqlfile                                                , "sqlfile"           , "sqlfile" },
                { new StringContent("dbv"+dbvendor)                      , "dbvendor"         },
                { new StringContent(options.ShowRelationType)            , "showRelationType" },
                { new StringContent(options.SimpleOutput.ToString())     , "simpleOutput"     },
                { new StringContent(options.IgnoreRecordSet.ToString())  , "ignoreRecordSet"  },
                { new StringContent(options.ignoreFunction.ToString())   , "ignoreFunction"   },
                { new StringContent(config.UserId)                       , "userId"   },
                { new StringContent(config.Token)                        , "token"   },
            };
            try
            {
                var stopWatch = Stopwatch.StartNew();
                string url = $"{config.Host}/gspLive_backend/sqlflow/generation/sqlflow/" + (options.IsGraph ? "graph" : "");
                using var client = new HttpClient();
                // client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Token", config.Token);
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
                var form = new MultipartFormDataContent{
                { new StringContent(config.UserId)                       , "userId"   },
            };
                using var response = await client.PostAsync(url, form);
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
                    Console.WriteLine("SQLFlowClient    1.2.0          2020/12/13");
                    Console.WriteLine($"gsp              {gsp.version}        {gsp.ReleaseDate}");
                    Console.WriteLine($"backend          {backend.version}          {backend.ReleaseDate}");
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
