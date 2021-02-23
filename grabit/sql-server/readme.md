## Automated data lineage from SQL Server
This article introduces how to discover the data lineage from SQL Server database 
and keep it updated automatically. So the business users and developers can see
the SQL Server data lineage graph instantly.

### Software used in this solution
- [SQLFlow on-premise version](https://www.gudusoft.com/sqlflow-on-premise-version/)
- [Grabit tool](https://www.gudusoft.com/grabit/) for SQLFlow. It's free.

You may [request a 30 days SQLFlow on-premise version](https://www.gudusoft.com/submit-a-ticket/)
by filling out a form with the subject: request a 30 days SQLFlow on-premise version.

Our team will contact you in 1-3 working days after receive the message.


### Prerequisites
- A linux/mac/windows server with at least 8GB memory (ubuntu 20.04 is recommended).
- Java 8
- Nginx web server. 
- Port needs to be opened. (80, 8761,8081,8083. Only 80 port need to be opened if you setup the nginx reverse proxy as mentioned in [this document](https://github.com/sqlparser/sqlflow_public/blob/master/install_sqlflow.md))

### Install SQLFlow on-premise version
- [Guilde for install on linux](https://github.com/sqlparser/sqlflow_public/blob/master/install_sqlflow.md)
- [Guilde for install on window(https://github.com/sqlparser/sqlflow_public/blob/master/install_sqlflow_on_windows.md)
- [Guilde for install on mac](https://github.com/sqlparser/sqlflow_public/blob/master/install_sqlflow_on_mac.md)

### Install grabit tool
After [download grabit tool](https://www.gudusoft.com/grabit/), please [check this article](https://github.com/sqlparser/sqlflow_public/tree/master/grabit) to setup the grabit tool.

### Configure the grabit

[Please check this article] for how to install SQLFlow on-premise version.


### How it works
sqlflow_automated_data_lineage.png