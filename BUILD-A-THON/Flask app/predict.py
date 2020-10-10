from flask import Flask,render_template,url_for,request
import os
from credentials import *
import boto3



app = Flask(__name__)
db = boto3.resource('dynamodb',aws_access_key_id = access_key_id,aws_secret_access_key = secret_access_key,aws_session_token = session_token,region_name = region )
client = boto3.client('dynamodb',aws_access_key_id = access_key_id,aws_secret_access_key = secret_access_key,aws_session_token = session_token,region_name = region )
table = db.Table("my_table")
final_table = db.Table("my_table2")#employee count table used for updating.(second table)
comprehend_client = boto3.client('comprehend',aws_access_key_id = access_key_id,aws_secret_access_key = secret_access_key,aws_session_token = session_token,region_name = region )



@app.route('/')
def index():
    return render_template('home.html')

@app.route('/process',methods =['POST'])
def process():
    customer_name = request.form['customer_name'] 
    employee_id = request.form['emp']
    feedback = request.form['review']
    
    if employee_id == 'Emp_001':
        employee_name = "Employee 1"
    elif employee_id == "Emp_002":
        employee_name = "Employee 2"
    elif employee_id == "Emp_003":
        employee_name = "Employee 3"
    elif employee_id == "Emp_004":
        employee_name = "Employee 4"
    elif employee_id == "Emp_005":
        employee_name = "Employee 5"
    
    print("The name ofthe customer :",customer_name)
    print("The employee id:",employee_id)
    print("The feedback is : ",feedback)
    print("The name of the employee : ",employee_name)

    
    ItemCount = client.describe_table(TableName='my_table')
    no_of_item_in_employee_review = ItemCount['Table']['ItemCount']

    items = [no_of_item_in_employee_review,customer_name,feedback,employee_id,employee_name]

    table.put_item(
        Item  = {
            'order_id':items[0],
            'customer_name':items[1],
            'feedback':items[2],
            'emp_id':items[3],
            'emp_name':items[4]
        }
    )
    print("The number  of element in the first data base : ",ItemCount)

    
    
    get_employee_id = employee_id

    count_table_response = final_table.get_item(
        Key={
            'emp_id':get_employee_id
        }
    ) # it gives the responses of the Employee count table

    review_count = count_table_response["Item"]['no_of_reviews']  # second table
    score = count_table_response["Item"]['score'] # second table

    comprehend_response = comprehend_client.detect_sentiment(Text= feedback,LanguageCode="en")
    result = comprehend_response['Sentiment']

    if result == 'POSITIVE':
        final_table.update_item(
            Key={
                'emp_id':get_employee_id
            },
            UpdateExpression='SET no_of_reviews = :val1',
            
            ExpressionAttributeValues={
                ':val1' : review_count + 1
            }
        )
        final_table.update_item(
            Key={
                'emp_id':get_employee_id
            },
            UpdateExpression='SET score = :val2',
            
            ExpressionAttributeValues={
                ':val2' : score + 30
            }
        )

    elif (result == 'NEGATIVE'):
        final_table.update_item(
            Key={
                'emp_id':get_employee_id
            },
            UpdateExpression='SET no_of_reviews = :val1',
            
            ExpressionAttributeValues={
                ':val1' : review_count + 1,
            }

        )

        final_table.update_item(
            Key={
                'emp_id':get_employee_id
            },
            UpdateExpression='SET score = :val2',
            
            ExpressionAttributeValues={
                ':val2' : score + 5
            }
        )
        
    else:
        final_table.update_item(
            Key={
                'emp_id':get_employee_id
            },
            UpdateExpression='SET no_of_reviews = :val1',
            
            ExpressionAttributeValues={
                ':val1' : review_count + 1,
                
            }
        )

        final_table.update_item(
            Key={
                'emp_id':get_employee_id
            },
            UpdateExpression='SET score = :val2',
            
            ExpressionAttributeValues={
                ':val2' : score + 15
            }
        )
    print("Updated suceesfully")


    return render_template('home.html',solu="Updated Successfully")


@app.route('/result')
def result():
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
    return render_template("draw.html", review = review, score = score)


if __name__=='__main__':
    app.run(debug= True)

