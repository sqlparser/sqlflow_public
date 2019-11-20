Use SQLFlow in your flavor ways

### 1. Visit gudusoft.com website using browser
You may paste your SQL script into the SQLFlow web page, or upload the SQL file to the site.
select the correct database and then click the visualize button.

### 2. Use RESTFul APIs
Access the SQLFlow service using the SQLFlow RESTFul APIs. Send your SQL code 
to the SQLFlow and get back the data lineage in JSON format.Even better, The layout
information also included in the JSON ouput, so you can visualize the diagram in 
your own program by utilizing those layout data.

[Demo](https://github.com/sqlparser/sqlflow_public/tree/master/api/client/csharp)

### 3. Add visualize feature in your own application/website
The SQLFlow consists of the frontend and backend. Please [check here](https://github.com/sqlparser/sqlflow_public#sqlflow-components) for further information.
You may setup the frontend on you own web server, or include the frontend in your application to add visualize feature.

Your application still need connect to the SQLFlow backend in order to process the SQL code to get data lineage.

### 4. Install both frontend and backend on your own application/server
Setup both the frontend and backend of SQLFlow on our server. 

Please check the [setup manual](https://github.com/sqlparser/sqlflow_public/blob/master/install_sqlflow.md).
