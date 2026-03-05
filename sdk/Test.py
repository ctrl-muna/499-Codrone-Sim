import time
import csv
import os
import re
import json
from UserControl import UserControl



if __name__ == "__main__":
    userC = UserControl()
    testing = True
    while testing:
        userC.Input_Command()
        Input = input("Continue Testing? (y/n): ")
        if Input.lower() == "n":
            testing = False
    