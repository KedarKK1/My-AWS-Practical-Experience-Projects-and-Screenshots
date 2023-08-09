import boto3
import json
from datetime import datetime
# from /custome_encoder.py import CustomEncoder
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodbTableName = "newestBirthdayReminderDB"
dynamodb = boto3.resource('dynamodb')
table1 = dynamodb.Table(dynamodbTableName)

getMethod = "GET"
postMethod = "POST"
deleteMethod = "DELETE"
patchMethod = "PATCH"
createuserbdentry = "/createbdentry"
usersandbdlist = "/getallbds"
todaysBdList = "/gettodaysbirthdays"


def buildResponse(statusCode, body=None):
    response = {
        'statusCode': statusCode,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps('Lambda executed successfully.')
    }
    if body is not None:
        # response['body'] = json.dumps(body, cls=CustomEncoder)
        response['body'] = json.dumps(body)

    return response


# This is the Lambda handler function that will be executed when the Lambda is triggered.
def lambda_handler(event, context):
    try:
        # Extract the name and DOB from the event payload
        # print("event ", event) # print("event['body'] ", event['body'])


        # httpMethod = event['httpMethod'] OR use below code
        httpMethod = event.get('httpMethod', '')
        # path = event['path'] OR use below code
        path = event.get('path', '')
        ans = ""

        today = datetime.today().strftime('%d-%m')
        # Extract only the month-day part from the DOB (MM-DD)

        if httpMethod == postMethod and path == createuserbdentry:
            # If event['body'] is a JSON string, convert it to a dictionary
            event_body = json.loads(event['body'])

            name = event_body["nameFieldId"]
            dob = event_body["dateFieldId"]
            dob = dob[:5]

            # Parse the DOB string into a datetime object
            # dob = datetime.strptime(dob, '%d-%m-%Y')

            response = table1.put_item(Item={
                'userNameField': name,
                'dobField': dob
            })

            ans = f"Successfully Added {str(name)}'s  birthday!" + json.dumps(response) + json.dumps(path) + json.dumps(httpMethod)
            response = buildResponse(200, f"Lambda executed successfully in post method! {ans}")
            return response

        elif(httpMethod == getMethod and path == usersandbdlist):

            response = table1.scan()
            result = response['Items']

            # Process the items as needed
            # for item in result:
            #     print(item)

            # Optionally, handle pagination if necessary
            while 'LastEvaluatedKey' in response:
                response = table1.scan(
                    ExclusiveStartKey=response['LastEvaluatedKey'])
                result.extend(response['Item'])
                # for item in result:
                # print(item)

            response = buildResponse(200, f"{json.dumps(result)}")
            return response

        elif(httpMethod == getMethod and path == todaysBdList):
            response = table1.scan()
            result = response['Items']

            ans = []

            for item in result:
                if(today == item['dobField']):
                    ans.append(item)

            response2 = buildResponse(200, f"{json.dumps(ans)}")
            return response2

        else:
            response = table1.scan()
            result = response['Items']

            ans = []

            # Process the items as needed
            for item in result:
                if(today == item['dobField']):
                    ans.append(item)

            client = boto3.client("ses")
            subject = ("Today's birthday list")
            body = "Test body from lambda" + json.dumps(ans)
            message = {"Subject": {"Data": subject}, "Body": {"Html": {"Data": body}}}
            response = client.send_email(Source="officialkedark1@gmail.com", Destination={"ToAddresses": ["officialkedark1@gmail.com"]}, Message=message)

            response2 = buildResponse(200, f"Lambda executed successfully  {json.dumps(ans)} & {json.dumps(response)}")
            return response2

            # response = buildResponse(200, f"Lambda executed successfully {path} {httpMethod}")
            # return response

    except Exception as err:
        response = buildResponse(500, f'Lambda encountered an error: {str(err)}')
        return response
        # return {'statusCode': 500, 'body': json.dumps(f'Lambda encountered an error: {str(err)}')}

# def send_whatsapp_message(name, dob):
#     # Set up SNS client
#     sns_client = boto3.client('sns')

#     # Replace 'YOUR_PHONE_NUMBER' with your actual WhatsApp number, including the country code. # Note: WhatsApp numbers need to be in the format 'whatsapp:+<country_code><phone_number>'
#     phone_number = 'whatsapp:+9195#90##14#'

#     # Construct the message
#     message = f"Today is {name}'s birthday! Date of Birth: {dob}"

#     # Send the message using Amazon SNS
#     sns_client.publish( PhoneNumber=phone_number, Message=message )
