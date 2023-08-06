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

def getdbclusterlist(region, family_name=None,custom=0):
    db_cluster={}
    cmdd = ['aws', 'rds', 'describe-db-cluster-parameter-groups' , '--region' , region]
    dbclusterdata = runcommand(cmdd, "aws rds describe-db-cluster-parameter-groups")
    for i in dbclusterdata['DBClusterParameterGroups']:
        if custom == 0:
            if i['DBParameterGroupFamily'] == family_name:
                db_cluster[i['DBClusterParameterGroupName']] = i['DBParameterGroupFamily']
        else:
            db_cluster[i['DBClusterParameterGroupName']] = i['DBParameterGroupFamily']
    return db_cluster

def getclusterdefaultfamily(region, family_name):
    cmdd = ['aws', 'rds', 'describe-db-cluster-parameters' ,'--db-cluster-parameter-group-name', 'default.'+family_name,  '--region' , region]
    dfamily=runcommand(cmdd, "aws rds describe-db-cluster-parameters --db-cluster-parameter-group-name default."+family_name)
    return dfamily['Parameters']


def getdefaultfamily(region, family_name):
    cmdd = ['aws', 'rds', 'describe-engine-default-parameters' ,'--db-parameter-group-family', family_name, '--region' , region]
    dfamily=runcommand(cmdd, "aws rds describe-engine-default-parameters --db-parameter-group-family"+family_name)
    return dfamily['EngineDefaults']['Parameters']

def getdbinstancelist(region, family_name=None,custom=0):
    db_instance={}
    cmdd = ['aws', 'rds', 'describe-db-parameter-groups' , '--region' , region]
    dbinstancedata =  runcommand(cmdd, "aws rds describe-db-parameter-groups")
    for i in dbinstancedata['DBParameterGroups']:
        if custom == 0:
            if i['DBParameterGroupFamily'] == family_name:
                db_instance[i['DBParameterGroupName']] = i['DBParameterGroupFamily']
        else:
            db_instance[i['DBParameterGroupName']] = i['DBParameterGroupFamily']
    return db_instance


def compareinstancerdspg(region,family_name,fname=None):
    if checkawsprofile():
        dlist = getdefaultfamily(region,family_name)
        db_instance = getdbinstancelist(region, family_name)
        cmdd = ['aws', 'rds', '--region', region ,'describe-db-parameters', '--db-parameter-group-name']
        cmdarg = "aws rds --region "+region+" describe-db-parameters --db-parameter-group-name "
        if fname != None:
            compare(dlist, db_instance,family_name,cmdd,cmdarg,fname)
        else:
            compare(dlist, db_instance,family_name,cmdd,cmdarg)
        

def compareclusterrdspg(region,family_name,fname = None):
    if checkawsprofile():
        dlist = getclusterdefaultfamily(region,family_name)
        db_cluster = getdbclusterlist(region, family_name)
        cmdd = ['aws', 'rds', '--region', region, 'describe-db-cluster-parameters', '--db-cluster-parameter-group-name' ]
        cmdarg = "aws rds --region "+region+" describe-db-cluster-parameters --db-cluster-parameter-group-name "
        if fname != None:
            compare(dlist, db_cluster,family_name,cmdd,cmdarg,fname)
        else:
            compare(dlist, db_cluster,family_name,cmdd,cmdarg)

def compare(dlist, alist,family_name,cmdd,cmdarg,fname = None):
    if fname != None:
        if os.path.exists(fname):
            os.remove(fname)
        file = open(fname, 'a')
    for i in alist:
        temp_dict = {}
        temp_dict['Name'] = []
        temp_dict['Value'] = []
        temp_dict['Default_Value'] = []
        if alist[i]==family_name:
            cmdd = cmdd + [i]
            cmdarg = cmdarg + i
            data = runcommand(cmdd,cmdarg)
            ll= data['Parameters']
            for j in range(len(ll)-1):
                if "ParameterValue" in ll[j].keys() and "ParameterValue" not in dlist[j].keys():  
                    if ll[j]['ParameterName'] == dlist[j]['ParameterName']:
                        temp_dict["Value"].append(ll[j]['ParameterValue'])
                        temp_dict["Name"].append(ll[j]['ParameterName'])
                        temp_dict["Default_Value"].append("NaN")
                if "ParameterValue" in ll[j].keys() and "ParameterValue"  in dlist[j].keys():  
                    if ll[j]['ParameterName'] == dlist[j]['ParameterName']:
                        if ll[j]['ParameterValue'] != dlist[j]['ParameterValue']:
                            temp_dict["Value"].append(ll[j]['ParameterValue'])
                            temp_dict["Name"].append(ll[j]['ParameterName'])
                            temp_dict["Default_Value"].append(dlist[j]["ParameterValue"])
        df = pd.DataFrame(temp_dict)
        wr = "\n\nName : "+i+"\n\n"+str(df)+"\n\n"
        print(wr)
        if fname != None:
            file.write(wr)
        break
    if fname != None:
        file.close()


def customcompareinstancepg(pglist,region):
    if checkawsprofile():
        custom = 1
        db_instance = getdbinstancelist(region,custom=custom)
        a = {}
        for i in pglist:
            if i in db_instance.keys():
                a[i]=db_instance[i]
            else:
                print("\n"+i+" RDS parameter group does not exist in "+ region+" region\n")
        for i in a:
            temp_dict = {}
            temp_dict[i] = a[i]
            dlist = getdefaultfamily(region,a[i])
            cmdd = ['aws', 'rds', '--region', region ,'describe-db-parameters', '--db-parameter-group-name']
            cmdarg = "aws rds --region "+region+" describe-db-parameters --db-parameter-group-name "
            compare(dlist,temp_dict,temp_dict[i],cmdd,cmdarg)


def customcompareclusterpg(pglist,region):
    if checkawsprofile():
        custom = 1
        db_cluster = getdbclusterlist(region,custom=custom)
        a = {}
        for i in pglist:
            if i in db_cluster.keys():
                a[i]=db_cluster[i]
            else:
                print("\n"+i+" RDS parameter group does not exist in "+ region+" region\n")
        for i in a:
            temp_dict = {}
            temp_dict[i] = a[i]
            dlist = getclusterdefaultfamily(region,a[i])
            cmdd = ['aws', 'rds', '--region', region, 'describe-db-cluster-parameters', '--db-cluster-parameter-group-name' ]
            cmdarg = "aws rds --region "+region+" describe-db-cluster-parameters --db-cluster-parameter-group-name "
            compare(dlist,temp_dict,temp_dict[i],cmdd,cmdarg)