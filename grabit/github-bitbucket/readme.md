Grab files in a Github/Bitbucket repository and send them to the SQLFlow
for analyzing and return the data lineage.

### 1. Prerequisites

#### Install Java

- Java 8 or higher version must be installed and configured correctly.

setup the PATH like this: (Please change the JAVA_HOME according to your environment)

```bash
export JAVA_HOME=/usr/lib/jvm/default-java
export PATH=$JAVA_HOME/bin:$PATH
```

```bash
java -version

java version "1.8.0_281"
Java(TM) SE Runtime Environment (build 1.8.0_281-b09)
Java HotSpot(TM) 64-Bit Server VM (build 25.281-b09, mixed mode)
```

#### Install git

- **ubuntu:**

```
sudo apt-get install git
```

- **centos:**

```
sudo yum install git
```

- **mac:**

```
brew install git
```

- **windows:**

```
1.Go to the Git official website to download, website address: https://git-scm.com/downloads
2.Run the Git installation file and click Next to finish the installation
```

After the installation is completed, run **git --version** to check it is installed successfully.

```bash
git --version

git version 2.30.1 (Apple Git-130)
```

### 2. Set up grabit configuration file

Create a config file with name such as: `gitServer.conf.json`

```json
{
	"optionType":3,
	"resultType":1,
	"databaseType":"sparksql",
	"SQLFlowServer":{
		"server":"https://api.gudusoft.com", 
		"serverPort":"",
		"userId":"auth0|5fc735a542843a006e29a399",
		"userSecret":"c1e11c16040d8a274045c7e773a658e0808e3f4cebf3326da154027d9f04a53d"
	},
	"bitbucketRepo":{
					"url":"https://bitbucket.org/ShenHuan001/sparksql",
					"username":"ShenHuan001",
					"password":"9vW57XznDthGMaWPXavX",
					"sshkeyPath":""
				}
}
```

Please check this document (https://github.com/sqlparser/sqlflow_public/blob/master/sqlflow-userid-secret.md) if you don't know your userId and userSecret of the SQLFlow Cloud.

### 3. Run grabit in command line

Linux or Mac:
```bash
./start.sh /f gitServer.conf.json
```

Windows:
```bash
start.bat /f gitServer.conf.json
```

### 4. Check data lineage on SQLFlow Cloud
