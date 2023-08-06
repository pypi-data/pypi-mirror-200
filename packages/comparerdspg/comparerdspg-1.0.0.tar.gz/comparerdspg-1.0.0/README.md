# comparerdspg

Under construction! Still you can use!

Developed by Tanmay Varade

This project help to compare your RDS parameter group with their default.
## If you get error for comparerdspg- ModuleNotFoundError: No module named 'comparerdspg'
```
python3 -m pip install comparerdspg
```

## Examples of How To Use
Make sure you export your AWS credential to terminal
### Compare one or more RDS instance parameter group

```python
import comparerdspg

comparerdspg.customcompareclusterpg(["rds-instance-pg-1","rds-instance-pg-1",,"rds-instance-pg-n"], "aws-region")
# provide name of only custom RDS instance parameter name.
```

### Compare one or more RDS instance parameter group

```python
import comparerdspg

comparerdspg.customcompareinstancepg(["rds-cluster-pg-1","rds-cluster-pg-1",,"rds-cluster-pg-n"], "aws-region")
# provide name of only custom RDS cluster parameter name.
```

### Compare all the custom RDS instance parameter group with specific family.

```python
import comparerdspg

comparerdspg.compareinstancerdspg("aws-region","family-name")

# family-name = aurora-mysql5.7 if you wants to copare all instance parameter group having default family aurora-mysql5.7

# If you wants to store output in file provide filename argument to above function. 

comparerdspg.compareinstancerdspg("aws-region","family-name", "file-name")
```


### Compare all the custom RDS cluster parameter group with specific family.

```python
import comparerdspg

comparerdspg.compareclusterrdspg("aws-region","family-name")

# family-name = aurora-mysql5.7 if you wants to copare all cluster parameter group having default family aurora-mysql5.7

# If you wants to store output in file provide filename argument to above function. 

comparerdspg.compareclusterrdspg("aws-region","family-name", "file-name")
```

```python
import comparerdspg

comparerdspg.compareclusterrdspg("aws-region","family-name")

# family-name = aurora-mysql5.7 if you wants to copare all cluster parameter group having default family aurora-mysql5.7

# If you wants to store output in file provide filename argument to above function. 

comparerdspg.compareclusterrdspg("aws-region","family-name", "file-name")
```

## If you get error for pandas module use below command to install
```
python3 -m pip install pandas
```
