import json
import os
import subprocess
import pandas as pd


def checkawsprofile():
    if ("AWS_PROFILE" in os.environ.keys()) or (("AWS_ACCESS_KEY_ID" in os.environ.keys()) and ("AWS_SECRET_ACCESS_KEY" in os.environ.keys())):
        return 1
    else:
        print("Please setup AWS PROFILE or export your ACCESS KEY and SECRET KEY First.....")
        return 0
        
