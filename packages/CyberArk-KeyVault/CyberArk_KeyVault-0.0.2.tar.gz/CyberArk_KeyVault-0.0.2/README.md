# CyberArk-Management
This is a python helper function for retrieving keyvault secrets from CyberArk
<br>
<br>
[![Upload Python Package](https://github.com/ayajnik/CyberArk-Management/actions/workflows/python-publish.yml/badge.svg?event=workflow_run)](https://github.com/ayajnik/CyberArk-Management/actions/workflows/python-publish.yml)
<br>
<br>
# Prerequisites
1. Python 3.x
2. CyberArk KeyVault account<br>
# Installation
pip install CyberArk-KeyVault
# Usage
Import the VaultManager module into your script.
Create an instance of the VaultManager class by calling vm = VaultManager()
Call the get_password() method of the cyberArkVault class with the following parameters:

-cyberArk_host: The host name of your organization<br>
-appId: The App ID of the application you want to retrieve secrets for<br>
-safe: The name of the safe where the secret is stored<br>
-cyberark_usr: username you want to retrieve secrets for<br>

