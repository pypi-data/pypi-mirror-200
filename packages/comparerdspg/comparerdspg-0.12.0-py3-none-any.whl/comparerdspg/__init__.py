import json
import os
import subprocess
import pandas as pd


def checkawsprofile():
    if ("AWS_PROFILE" in os.environ.keys()) or (("AWS_ACCESS_KEY_ID" in os.environ.keys()) and ("AWS_SECRET_ACCESS_KEY" in os.environ.keys())):
        return 1
    else:
        print("Please setup AWS PROFILE or export your ACCESS KEY and SECRET KEY First.....")
        quit()
        
def runcommand(cmd, name):
    rs=1
    while rs!=0:
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE)
            if result.returncode == 0:
                rs=result.returncode
                print("Successfully query for RDS Parameter group : "+name)
                output = result.stdout.decode('utf-8').strip()
                data = json.loads(output)
                return data
        except Exception as e:
            print("Error : "+e+"\nRetrying now........")

def getclusterdefaultfamily(region, family_name):
    cmdd = ['aws', 'rds', 'describe-db-cluster-parameters' ,'--db-cluster-parameter-group-name', 'default.'+family_name,  '--region' , region]
    dfamily=runcommand(cmdd, "aws rds describe-db-cluster-parameters --db-cluster-parameter-group-name default."+family_name)
    return dfamily['Parameters']