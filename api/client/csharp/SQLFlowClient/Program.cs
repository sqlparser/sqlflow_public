using System;
using CommandLine;
using CommandLine.Text;

namespace SQLFlowClient
{
    public class Options
    {
        [Value(0, MetaName = "sqlfile", Required = false, HelpText = "Input sqlfile to be processed.")]
        public string SQLFile { get; set; }

        [Option('g', "graph", Required = false, Default = false, HelpText = "Get the graph from sql.")]
        public bool IsGraph { get; set; }

        [Option('v', "dbvendor", Required = false, Default = "oracle", HelpText = "Set the database of the sqlfile.")]
        public string DBVendor { get; set; }

        [Option('r', "showRelationType", Required = false, Default = "fdd", HelpText = "Set the relation type.")]
        public string ShowRelationType { get; set; }

        [Option('s', "simpleOutput", Required = false, Default = false, HelpText = "Set whether to get simple output.")]
        public bool SimpleOutput { get; set; }

        [Option("ignoreRecordSet", Required = false, Default = false, HelpText = "Set whether to ignore record set.")]
        public bool IgnoreRecordSet { get; set; }

        [Option("ignoreFunction", Required = false, Default = false, HelpText = "Set whether to ignore function.")]
        public bool ignoreFunction { get; set; }

        [Option('o', "output", Required = false, Default = "", HelpText = "Save output as a file.")]
        public string Output { get; set; }

        [Option("version", Required = false, Default = false, HelpText = "Show version.")]
        public bool Version { get; set; }
    }

    class Program
    {
        static void Main(string[] args)
        {
            var parser = new Parser(with =>
            {
                with.AutoVersion = false;
                with.AutoHelp = true;
            });
            var parserResult = parser.ParseArguments<Options>(args); ;
            parserResult
            .WithParsed(options =>
            {
                HttpService.Request(options).Wait();
            })
            .WithNotParsed(errs =>
            {
                var helpText = HelpText.AutoBuild(parserResult, h =>
                {
                    h.AutoHelp = true;
                    h.AutoVersion = false;
                    return h;
                }, e => e);
                Console.WriteLine(helpText);
            });
        }
    }
}
