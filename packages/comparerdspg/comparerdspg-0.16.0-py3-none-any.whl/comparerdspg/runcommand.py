import json
import os
import subprocess
def runcommand(s):
    rs=1
    while rs!=0:
        try:
            result = subprocess.run("cmd", stdout=subprocess.PIPE)
            if result.returncode == 0:
                rs=result.returncode
                print("Successfully query for RDS Parameter group : "+name)
                output = result.stdout.decode('utf-8').strip()
                data = json.loads(output)
                return data
        except Exception as e:
            print("Error : "+e+"\nRetrying now........")
