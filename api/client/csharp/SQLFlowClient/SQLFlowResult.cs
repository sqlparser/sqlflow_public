using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace SQLFlowClient
{
    class SQLFlowResult
    {
        private readonly int maxLength = 24814437;// json will not be formatted if the string length exceeds this number
        public string json;
        public bool data;
        public bool error;
        public bool dbobjs;
        public bool sqlflow;
        public bool graph;

        public SQLFlowResult(string text)
        {
            if (text.Length <= maxLength)
            {
                var jobject = JObject.Parse(text);
                json = jobject.ToString();
                data = jobject.SelectToken("data") != null;
                error = jobject.SelectToken("error") != null;
                dbobjs = jobject.SelectToken("data.dbobjs") != null;
                sqlflow = jobject.SelectToken("data.sqlflow") != null;
                graph = jobject.SelectToken("data.graph") != null;
            }
            else
            {
                json = text;
                data = false;
                error = false;
                dbobjs = false;
                sqlflow = false;
                graph = false;

                using var reader = new JsonTextReader(new StringReader(text));
                while (reader.Read())
                {
                    if (reader.Value != null)
                    {
                        //Console.WriteLine("Token: {0}, Value: {1} ,Depth：{2}", reader.TokenType, reader.Value, reader.Depth);
                        if (reader.Depth > 3)
                        {
                            goto End;
                        }
                        if (reader.TokenType.ToString() == "PropertyName")
                        {
                            switch (reader.Value.ToString())
                            {
                                case "data":
                                    data = true;
                                    break;
                                case "error":
                                    error = true;
                                    break;
                                case "dbobjs":
                                    dbobjs = true;
                                    break;
                                case "sqlflow":
                                    sqlflow = true;
                                    break;
                                case "graph":
                                    graph = true;
                                    break;
                            }
                        }
                    }
                    else
                    {
                        //Console.WriteLine("Token: {0}", reader.TokenType);
                        if (error || dbobjs || sqlflow || graph)
                        {
                            reader.Skip();
                        }
                    }
                }
            End: { }
            }
        }
    }
}
