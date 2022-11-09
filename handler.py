from datetime import datetime
import boto3
from io import BytesIO
from PIL import Image, ImageOps
import os
import uuid
import json
from decimal import *

s3 = boto3.client('s3')
size = int(os.environ['THUMBNAIL_SIZE'])
dbtable = str(os.environ['DYNAMODB_TABLE'])
dynamodb = boto3.resource('dynamodb')


def get_s3_image(bucket, image):
    reponse = s3.get_object(Bucket=bucket, Key=image)
    imagecontent = reponse['Body'].read()
    file = BytesIO(imagecontent)

    img = Image.open(file)
    return img


def image_to_thumbnail(image):
    return ImageOps.fit(image, (size, size), Image.ANTIALIAS)


def new_filename(key):
    key_split = key.rsplit('.', 1)
    return key_split[0] + '_thumbnail.png'


def upload_to_s3(bucket, key, image, img_size):
    out_thumbnail = BytesIO()

    image.save(out_thumbnail, 'PNG')
    out_thumbnail.seek(0)

    response = s3.put_object(
        ACL='public-read',
        Body=out_thumbnail,
        Bucket=bucket,
        ContentType='image/png',
        Key=key
    )
    print(response)
    url = '{}/{}/{}'.format(s3.meta.endpoint_url, bucket, key)

    s3_save_thumbnail_url_to_dynamo(url, img_size)
    return url


def s3_thumbnail_generator(event, context):
    # parse the event
    print("EVENT:::", event)

    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        img_size = event['Records'][0]['s3']['object']['size']

        if (not key.endswith('_thumbnail.png')):
            image = get_s3_image(bucket, key)
            thumbnail = image_to_thumbnail(image)
            thumbnail_key = new_filename(key)
            url = upload_to_s3(bucket, thumbnail_key, thumbnail, img_size)

            return url

    except Exception as e:
        print(e)
        print('Error getting object'.format(key, bucket))
        raise e


def s3_save_thumbnail_url_to_dynamo(url_path, img_size):
    table = dynamodb.Table(dbtable)
    toint = float(img_size*0.53)/1000

    response = table.put_item(
        Item={
            'id': str(uuid.uuid4()),
            'url': url_path,
            'size': img_size,
            'approxReducedSize': str(toint) + str(' KB'),
            'created_at': str(datetime.now()),
            'updated_at': str(datetime.now())
        }
    )
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
        },
        'body': json.dumps(response)
    }


# === get, post, delete, put thumbnail===
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        # 👇️ if passed in object is instance of Decimal
        # convert it to a string
        if isinstance(obj, Decimal):
            return str(obj)
        # 👇️ otherwise use the default behavior
        return json.JSONEncoder.default(self, obj)


def s3_get_item(event, context):
    table = dynamodb.Table(dbtable)
    response = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(response['Item'], cls=DecimalEncoder)
    }


def s3_delete_item(event, context):
    table = dynamodb.Table(dbtable)
    response = table.delete_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({
                'message': 'Item deleted successfully',
                'id': event['pathParameters']['id']
            })
        }

    return {
        'statusCode': 500,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(response, cls=DecimalEncoder)
    }


def s3_get_thumbnail_urls(event, context):
    table = dynamodb.Table(dbtable)
    response = table.scan()
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(data, cls=DecimalEncoder)
    }
