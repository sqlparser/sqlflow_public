'''
************************************************************************************************************************************************************

Properties
================
NAME:				SQLFlow API Python Client
DESCRIPTION:		A simple wrapper written for Gudusoft's SQLFlow API.
AUTHOR:				Bence Kiss
ORIGIN DATE:		21-MAR-2020
PYTHON VERSION:		3.7.3

Additional Notes
================
-


ADDITIONAL INFORMATION
============================================================================================================================================================
Resources						URL
==============================	============================================================================================================================
API configuration				https://api.gudusoft.com/gspLive_backend/swagger-ui.html#!/sqlflow-controller/generateSqlflowUsingPOST
------------------------------	----------------------------------------------------------------------------------------------------------------------------
SQLFlow Git repo				https://github.com/sqlparser/sqlflow_public
------------------------------	----------------------------------------------------------------------------------------------------------------------------
Dataflow relationship types		https://github.com/sqlparser/sqlflow_public/blob/master/dbobjects_relationship.md
------------------------------	----------------------------------------------------------------------------------------------------------------------------
SQLFlow front end				http://www.gudusoft.com/sqlflow/#/
------------------------------	----------------------------------------------------------------------------------------------------------------------------
C# API client					https://github.com/sqlparser/sqlflow_public/tree/master/api/client/csharp
------------------------------	----------------------------------------------------------------------------------------------------------------------------


REVISION HISTORY
============================================================================================================================================================
Version	Change Date		Author	Narrative
=======	===============	======	============================================================================================================================
1.0.0	21-MAR-2020		BK		Created
------- ---------------	------	----------------------------------------------------------------------------------------------------------------------------
0.0.0	DD-MMM-YYYY		XXX		What changed and why...
------- ---------------	------	----------------------------------------------------------------------------------------------------------------------------

************************************************************************************************************************************************************
'''

# ==========================================================================================================================================================

# Import required modules

import os
import requests
import json

# ==========================================================================================================================================================

class SQLFlowClient:
       
    '''
    
    Class description
    ------------------------------------------------------------------------------------------------------------------------------------------------------------
    
        Class containing various functions to use SQLFlow API.
        
    Class instance variables
    ------------------------------------------------------------------------------------------------------------------------------------------------------------
    
        - api_key: The token needed for authorization. Default public token can be found here:
            
            https://github.com/sqlparser/sqlflow_public/tree/master/api/client/csharp
            
        - api_url: Default base URL of the API requests. Can be changed at class initialization.
        
    Class methods
    ------------------------------------------------------------------------------------------------------------------------------------------------------------
    
        - configure_api:            Set the API parameters for the requests.
        - analyze_script:           Submit a single SQL script using POST request to the API. Responses are stored in the class instance's results variable.
        - export_responses:         Export all stored API responses to a target folder as JSON files.
        - mass_process_scripts:     Process all SQL scripts found in a directory tree, optionally exporting results to a designated folder.
    
    Class dependencies
    ------------------------------------------------------------------------------------------------------------------------------------------------------------
    
        Packages used in the script considered to be core Python packages.
        
        - os:                       Used to handle input/output file and folder paths.
        - requests:                 Used to generate POST requests and submit script files to the API.
        - json:                     Used to process API responses when it comes to exporting.
        
    '''
    
    # ==========================================================================================================================================================
    # ==========================================================================================================================================================
    
    def __init__(self,
                 api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJndWR1c29mdCIsImV4cCI6MTYwMzc1NjgwMCwiaWF0IjoxNTcyMjIwODAwfQ.EhlnJO7oqAHdr0_bunhtrN-TgaGbARKvTh2URTxu9iU',
                 api_url = 'https://api.gudusoft.com/gspLive_backend/sqlflow/generation/sqlflow'
                 ):
        
        '''
        ------------------------------------------------------------------------------------------------------------------------------------------------------------
        Initialize SQLFlow API client.
        ------------------------------------------------------------------------------------------------------------------------------------------------------------
        '''
        
        # Set instance variables
        
        self.key = api_key
        
        self.url = api_url
        
        # Set default request header
        
        self.headers = {'Accept': 'application/json;charset=utf-8',
                        'Authorization': self.key
                        }
        
        # =============================================================================
        
        # Set lists of allowed API configuration values
        
        # List of allowed database vendors
        
        self.dbvendors = ['dbvbigquery',
                          'dbvcouchbase',
                          'dbvdb2',
                          'dbvgreenplum',
                          'dbvhana',
                          'dbvhive',
                          'dbvimpala',
                          'dbvinformix',
                          'dbvmdx',
                          'dbvmysql',
                          'dbvnetezza',
                          'dbvopenedge',
                          'dbvoracle',
                          'dbvpostgresql',
                          'dbvredshift',
                          'dbvsnowflake',
                          'dbvmssql',
                          'dbvsybase',
                          'dbvteradata',
                          'dbvvertica'
                          ]
        
        # List of allowed data relationship types
        
        self.reltypes = ['fdd',
                         'fdr',
                         'frd',
                         'fddi',
                         'join'
                         ]
        
        # List of allowed values for Boolean parameters
        
        self.switches = ['true',
                         'false'
                         ]
        
        # =============================================================================
        
        # Set default API configuration
        
        self.config = {'dbvendor': 'dbvmssql',
                       'showRelationType': 'fdd',
                       'simpleOutput': 'false',
                       'ignoreRecordSet': 'false'
                       }
        
        # Variable to store API responses
        
        self.results = dict()
        
    # ==========================================================================================================================================================
    # ==========================================================================================================================================================
    
    def configure_api(self,
                      db_vendor,
                      rel_type,
                      simple_output,
                      ignore_rs
                      ):
        
        '''
        ------------------------------------------------------------------------------------------------------------------------------------------------------------
        Configure the API request parameters. Only works if all parameters are provided.
        ------------------------------------------------------------------------------------------------------------------------------------------------------------
        '''
        
        # Check if the provided configuration values are valid
        
        if db_vendor in self.dbvendors and rel_type in self.reltypes and simple_output in self.switches and ignore_rs in self.switches:
            
            # Assign valid configuration parameters to config variable
            
            self.config = {'dbvendor': db_vendor,
                           'showRelationType': rel_type,
                           'simpleOutput': simple_output,
                           'ignoreRecordSet': ignore_rs
                           }
        
        # If any of the provided parameters are invalid, quit function and notify user
        
        else:
            
            print('\n\n' + '=' * 75 + '\n\nOne or more configuration values are missing or invalid. Please try again.\n\nAllowed values for db_vendor:\n\n' +
                  ' / '.join(self.dbvendors) +
                  '\n\nAllowed values for relation_type:\n\n' +
                  ' / '.join(self.reltypes) +
                  '\n\nAllowed values for simple_output and ignore_rs:\n\n' +
                  ' / '.join(self.switches) +
                  '\n\n' + '=' * 75
                  )
    
    # ==========================================================================================================================================================
    # ==========================================================================================================================================================
    
    def analyze_script(self,
                       script_path
                       ):
        
        '''
        ------------------------------------------------------------------------------------------------------------------------------------------------------------
        Submit SQL script file for SQLFlow analysis.
        ------------------------------------------------------------------------------------------------------------------------------------------------------------
        '''
        
        # Compile the API request URL
        
        configuredURL = self.url + '?' + ''.join(str(parameter) + '=' + str(setting) + '&' for parameter, setting in self.config.items()).rstrip('&')
        
        # =============================================================================
        
        # Check if provided path points to a SQL script file
        
        if os.path.isfile(script_path) and script_path.lower().endswith('.sql'):
            
            # Open the script file in binary mode so it could be submitted in a POST request
            
            with open(script_path, mode = 'rb') as scriptFile:
                
                # Use requests module's POST function to submit file and retrieve API response
                
                response = requests.post(configuredURL, files = {'sqlfile': scriptFile}, headers = self.headers)
            
            # =============================================================================
            
            # Add the request response to the class variable if response was OK
            
            if response.status_code == 200:
                
                self.results[script_path] = json.loads(response.text)
            
            # If response returned a different status, quit function and notify user
            
            else:
                
                print('\nAn invalid response was returned for < ' + os.path.basename(script_path) + ' >.\n', '\nStatus code: ' + str(response.status_code) + '\n')
        
        # If script file's path is invalid, quit function and notify user
        
        else:
            
            print('\nProvided path is not pointing to a SQL script file. Please try again.\n')
    
    # ==========================================================================================================================================================
    # ==========================================================================================================================================================
    
    def export_results(self,
                       export_folder
                       ):
        
        '''
        ------------------------------------------------------------------------------------------------------------------------------------------------------------
        Export all stored API responses as JSON files to a specified folder.
        ------------------------------------------------------------------------------------------------------------------------------------------------------------
        '''
        
        # Check if there are responses to be exported
        
        if len(self.results) != 0:
        
            # Create the directory for the result files if it doesn't exist
        
            os.makedirs(export_folder, exist_ok = True)
            
            # =============================================================================
            
            # Iterate the API results stored in the class
            
            for scriptpath, response in self.results.items():
                
                # Create a JSON file and export API results of each processed script file into the JSON file
                
                with open(os.path.join(export_folder, os.path.basename(scriptpath).replace('.sql', '') + '.json'), mode = 'w') as resultFile:
                    
                    # Write the response into the JSON file
                    
                    json.dump(response, resultFile)
        
        # If there are no responses yet, quit function and notify user
         
        else:
            
            print('\nThere are no API responses stored by the client yet.\n')
    
    # ==========================================================================================================================================================
    # ==========================================================================================================================================================
              
    def mass_process_scripts(self,
                             source_folder,
                             export_folder = None):
        
        '''
        ------------------------------------------------------------------------------------------------------------------------------------------------------------
        Scan a directory tree for SQL script files and pass each to an API call. Optionally export results to a desired folder.
        ------------------------------------------------------------------------------------------------------------------------------------------------------------
        '''
        
        # List to store SQL script file paths found in source folder
    
        scriptPaths = list()
        
        # =============================================================================
        
        # Scan source folder and subfolders
    
        for (dirpath, dirnames, filenames) in os.walk(source_folder):
            
            # Collect all paths which refer SQL scripts
                
            scriptPaths += [os.path.join(dirpath, file) for file in filenames if os.path.isfile(os.path.join(dirpath, file)) and file.lower().endswith('.sql')]
        
        # =============================================================================
        
        # If there is at least one SQL script in the directory tree execute API call
        
        if len(scriptPaths) != 0:
            
            # Iterate the SQL scrip paths and call the API for each file
            
            [self.analyze_script(script_path = path) for path in scriptPaths]
            
            # =============================================================================
            
            # If an export folder is provided, save the responses to that folder (but only those which have been analyzed at function call)
            
            if export_folder:
                
                # Store the current set of API responses
                
                allResults = self.results
                
                # Filter for responses related to current function call
                
                self.results = {scriptpath: response for scriptpath, response in self.results.items() if scriptpath in scriptPaths}
                
                # Export the responses of the current function call to the desired target folder
                
                self.export_results(export_folder = export_folder)
                
                # Reset the results variable to contain all responses again
                
                self.results = allResults
                
        # If no SQL script files were found in the directory tree, quit finction and notify user
        
        else:
            
            print('\nNo SQL script files have been found in the specified source folder and its subfolders.\n')