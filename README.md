# WebHack Playground

## Description
A Local Web-Based Hacking Environment for Learning XSS, SSRF, etc.

## Installation

1) Open Terminal and Clone Repository:

```bash
git clone https://github.com/AmerikanischerAdler/webhack_playground
```

2) Install Dependencies:

```bash
pip install -r requirements.txt
```

**TIP**: You may need to install pip

3) Set Up MYSQL Environment Variable:

Once you have created your mysql account, run this command in the terminal,
substituting your own password for "mypassword":

```bash
echo 'export MYSQLPW="mypassword"' >> .bashrc
```

**TIP**: This implies that you are using bash as your current shell. If not, run
the command, substituting your own shell config file for ".bashrc"

4) Create MYSQL Database and Tables:

Once you are logged into your mysql environment, enter:

```mysql
CREATE DATABASE mydb;
CREATE TABLE users (user_id VARCHAR(255) PRIMARY KEY AUTO_INCREMENT, username
VARCHAR(255), password VARCHAR(255));
```

5) Install Python

If python3 is not installed on your machine, run:

**MacOS:**

```bash
brew update 
brew install python3
``` 

**TIP**: For MacOS, be sure that homebrew is installed on your machine. If not, visit https://brew.sh to install.

**Ubuntu:**

```bash
sudo apt update 
sudo apt install python3
```

## Usage

1) Open Terminal

2) Navigate to webhack_playground Directory:

```bash
cd webhack_playground
```

3) Start Flask App:

*This will spin up a local backend server*

```bash
python3 app.py
```

If this doesn't work, try:

```bash
python3.11 app.py
```

**TIP**: You may need to install python3.11

4) Open Web Browser to New Tab or Window

5) Enter Server Address in Search Bar:

You may be able to simply click this link: http://127.0.0.1:5000/

## Inspiration
In Progress
