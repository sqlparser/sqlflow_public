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
	"optionType":2,
	"resultType":1,
	"databaseType":"sparksql",
	"SQLFlowServer":{
		"server":"https://api.gudusoft.com", 
		"serverPort":"",
		"userId":"your premium account user id",
		"userSecret":"your user secret key"
	},
	"gitServer":{
		"url":"https://bitbucket.org/AccountName/repoName",
		"username":"git user name",
		"password":"git password",
		"sshkeyPath":"ssh file if used"
		}
}
```

Please check this document (https://github.com/sqlparser/sqlflow_public/blob/master/sqlflow-userid-secret.md) if you don't know your userId and userSecret of the SQLFlow Cloud.

### 3. Run grabit in command line

```bash
./start.sh /f gitServer.conf.json
```