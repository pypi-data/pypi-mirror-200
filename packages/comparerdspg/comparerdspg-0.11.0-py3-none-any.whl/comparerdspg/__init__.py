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


# def getdbclusterlist(region, family_name=None,custom=0):
#     db_cluster={}
#     cmdd = ['aws', 'rds', 'describe-db-cluster-parameter-groups' , '--region' , region]
#     dbclusterdata = runcommand(cmdd, "aws rds describe-db-cluster-parameter-groups")
#     for i in dbclusterdata['DBClusterParameterGroups']:
#         if custom == 0:
#             if i['DBParameterGroupFamily'] == family_name:
#                 db_cluster[i['DBClusterParameterGroupName']] = i['DBParameterGroupFamily']
#         else:
#             db_cluster[i['DBClusterParameterGroupName']] = i['DBParameterGroupFamily']
#     return db_cluster

def getclusterdefaultfamily(region, family_name):
    cmdd = ['aws', 'rds', 'describe-db-cluster-parameters' ,'--db-cluster-parameter-group-name', 'default.'+family_name,  '--region' , region]
    dfamily=runcommand(cmdd, "aws rds describe-db-cluster-parameters --db-cluster-parameter-group-name default."+family_name)
    return dfamily['Parameters']

# def compareclusterrdspg(region,family_name,fname = None):
#     if checkawsprofile():
#         dlist = getclusterdefaultfamily(region,family_name)
#         db_cluster = getdbclusterlist(region, family_name)
#         cmdd = ['aws', 'rds', '--region', region, 'describe-db-cluster-parameters', '--db-cluster-parameter-group-name' ]
#         cmdarg = "aws rds --region "+region+" describe-db-cluster-parameters --db-cluster-parameter-group-name "
#         if fname != None:
#             compare(dlist, db_cluster,family_name,cmdd,cmdarg,fname)
#         else:
#             compare(dlist, db_cluster,family_name,cmdd,cmdarg)


# def compare(dlist, alist,family_name,cmdd,cmdarg,fname = None):
#     if fname != None:
#         if os.path.exists(fname):
#             os.remove(fname)
#         file = open(fname, 'a')
#     for i in alist:
#         temp_dict = {}
#         temp_dict['Name'] = []
#         temp_dict['Value'] = []
#         temp_dict['Default_Value'] = []
#         if alist[i]==family_name:
#             cmdd = cmdd + [i]
#             cmdarg = cmdarg + i
#             data = runcommand(cmdd,cmdarg)
#             ll= data['Parameters']
#             for j in range(len(ll)-1):
#                 if "ParameterValue" in ll[j].keys() and "ParameterValue" not in dlist[j].keys():  
#                     if ll[j]['ParameterName'] == dlist[j]['ParameterName']:
#                         temp_dict["Value"].append(ll[j]['ParameterValue'])
#                         temp_dict["Name"].append(ll[j]['ParameterName'])
#                         temp_dict["Default_Value"].append("NaN")
#                 if "ParameterValue" in ll[j].keys() and "ParameterValue"  in dlist[j].keys():  
#                     if ll[j]['ParameterName'] == dlist[j]['ParameterName']:
#                         if ll[j]['ParameterValue'] != dlist[j]['ParameterValue']:
#                             temp_dict["Value"].append(ll[j]['ParameterValue'])
#                             temp_dict["Name"].append(ll[j]['ParameterName'])
#                             temp_dict["Default_Value"].append(dlist[j]["ParameterValue"])
#         df = pd.DataFrame(temp_dict)
#         wr = "\n\nName : "+i+"\n\n"+str(df)+"\n\n"
#         print(wr)
#         if fname != None:
#             file.write(wr)
#         break
#     if fname != None:
#         file.close()
