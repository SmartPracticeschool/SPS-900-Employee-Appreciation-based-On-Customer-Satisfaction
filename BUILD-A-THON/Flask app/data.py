import boto3
from boto3.dynamodb.conditions import Key
from credentials import *



client = boto3.client('dynamodb',aws_access_key_id = access_key_id,aws_secret_access_key = secret_access_key,aws_session_token = session_token,region_name = region )
db = boto3.resource('dynamodb',aws_access_key_id = access_key_id,aws_secret_access_key = secret_access_key,aws_session_token = session_token,region_name = region )






    
    
table = db.Table('my_table2')      
id=['Emp_001','Emp_002','Emp_003','Emp_004','Emp_005']   
score=[]
review=[]
for i in id:
    resp = table.get_item(
            Key={
                'emp_id' : i,
            }
        )
    d= (resp['Item']['score'])
    e=(resp['Item']['no_of_reviews'])
    d=int(d)
    e=int(e)
    score.append(d)  
    review.append(e) 
print(score)
print(review)


