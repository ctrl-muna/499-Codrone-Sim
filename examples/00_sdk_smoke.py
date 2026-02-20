## Before Running on your local machine make sure to
##Verify you have venv installed and create a virtual environment using 'python -m venv .venv'
## Create the virtual evironment
 ## on windows use python -m venv .venv, Then env\scripts\activate.bat
## 1. Install the SDK using 'pip install -e ./sdk'
## 2. Run this file using 'python 00_sdk_smoke.py' to verify the SDK is working correctly
from sdk import setup
print("SDK smoke test passed successfully")