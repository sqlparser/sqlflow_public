========================================================================================================================================================================================================
SQLFlow API Python Client Documentation
========================================================================================================================================================================================================


--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
DESCRIPTION
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

High-level Python client of the SQLFlow API.

SQLFlow is a product of Gudusoft. The software's purpose is to analyze the flow of data, data relationships and dependencies coded into various SQL scripts.

This Python wrapper is built to process SQL scripts using the API with the option to export the API responses into JSON files.


--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
BASIC USAGE
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

The Python client is built into a single module. To use it, one must have a valid API key (currently available for the community at https://github.com/sqlparser/sqlflow_public/tree/master/api/client/csharp).

****************************************************************************************************

SQLFlowClient(api_key, api_url) class stores relevant parameters and methods to utilize SQLFlow API.

It has all the default values included for both the API key (which is currently available to the public) and the API base URL.

Initializig it will create an object with the following variables: API key, API URL, and it will also initialize the default request header and a default API parameter configuration.

****************************************************************************************************

configure_api(db_vendor, rel_type, simple_output, ignore_rs) method is created to change default API parameters as per required. It will change the pre-set API configuration based to provided parameter values.

Detailed explanations regarding API configuration could be found here: https://github.com/sqlparser/sqlflow_public/tree/master/api/client/csharp and here: https://api.gudusoft.com/gspLive_backend/swagger-ui.html#!/sqlflow-controller/generateSqlflowUsingPOST.

While using the method, one must provide all four parameters. Omitting one will result in error, while passing an invalid value will result in a notification and both will prevent the client from configuring the API request, and a notification message will be returned.

Valid parameters are as follows:

- db_vendor: dbvbigquery, dbvcouchbase, dbvdb2, dbvgreenplum, dbvhana, dbvhive, dbvimpala, dbvinformix, dbvmdx, dbvmysql, dbvnetezza, dbvopenedge, dbvoracle, dbvpostgresql, dbvredshift, dbvsnowflake, dbvmssql, bvsybase, dbvteradata, dbvvertica

- rel_type: fdd, fdr, frd, fddi, join

- simple_output: true, false

- ignore_rs: true, false

****************************************************************************************************

analyze_script(script_path) method can be used to submit a SQL script to the SQLFlow API for analysis. If the analysis returns a response sucessfully, the results will be stored in the SQLFlowClient object's results variable. Results variable is a dictionary object containing script paths and API responses as key-value pairs.

The method won't perform if the in-built check of the provided file path is not pointing to a SQL script. This will result in a notification message instead.

If the API call results in an error (e.g. invalid API key, server being busy), the response won't be stored, but a notification message will be returned instead.

****************************************************************************************************

export_results(export_folder) method simply dumps all the API call results stored already in SQLFlowClient's results variable to the specified output folder path.

The API responses will be saved as JSON files, with a filename corresponding to their source scripts'.

If the provided path doesn't exist, the method will automatically build the path.

If there are no stored responses yet, the function won't perform, and will return a notification message.

****************************************************************************************************

mass_process_scripts(source_folder, export_folder = None) method will scan the entire directory tree of the provided source folder for SQL script files and submits each to the API, storing all the responses in the results variable.

It can optionally export the results of the detected scripts to a desired export folder. If export_folder is left as None, this operation will be skipped.

Please note that this method will only execute the exporting of API results of scripts which were discovered in the specified directory at the function's execution.

****************************************************************************************************


--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
CODE EXAMPLES
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Initialize API client

client = SQLFlowClient()

# =============================================================================

# Configure the API parameters

client.configure('dbvmssql', 'fddi', 'false', 'false')

# Check config values after setting the parameters

print(client.config)

# =============================================================================

# Execute the analysis of a single script file

client.analyze_script('C:/Users/TESTUSER/Desktop/EXAMPLESCRIPT.sql')

# Check stored API response of the previous step

print(client.results)

# =============================================================================

# Export the stored response

client.export_results('C:/Users/TESTUSER/Desktop/EXPORTFOLDER')

# =============================================================================

# Execute mass processing of SQL scripts in a folder with an export folder specified

client.mass_process_scripts('C:/Users/TESTUSER/Desktop/SOURCEFOLDER', 'C:/Users/TESTUSER/Desktop/EXPORTFOLDER')


--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
AUTHORS
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Bence Kiss (vencentinus@gmail.com)


--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
ADDITIONAL INFORMATION
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Detailed information about the SQLFlow project could be accessed via the following links:

API configuration				https://api.gudusoft.com/gspLive_backend/swagger-ui.html#!/sqlflow-controller/generateSqlflowUsingPOST

SQLFlow Git repo				https://github.com/sqlparser/sqlflow_public

Dataflow relationship types			https://github.com/sqlparser/sqlflow_public/blob/master/dbobjects_relationship.md

SQLFlow front end				http://www.gudusoft.com/sqlflow/#/

C# API client					https://github.com/sqlparser/sqlflow_public/tree/master/api/client/csharp


In case of any questions regarding SQLFlow please contact Mr. James Wang at info@sqlparser.com.

In case of bugs, comments, questions etc. please feel free to contact the author at vencentinus@gmail.com or Mr. James Wang at info@sqlparser.com.


--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
ACKNOWLEDGEMENTS
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

The author of this project acknowledges that SQLFlow is a product and intellectual property exclusively of Gudusoft.

This project has been created to facilitate the utilization of the tool by the community, and the author of this Python client neither received nor expects to receive any compensation from Gudusoft in exchange.

This development has been created with good faith and with the intention to contribute to a great development, which the author of this wrapper has been utilizing for free under its development period.

The code is free to use for anyone intending to use SQLFlow API in any manner.

Thanks to Mr. James Wang, CTO of Gudusoft for his kind support and allowing me to utilize the tool under it's development and contribute to his company's project.