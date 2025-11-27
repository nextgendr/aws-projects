from aws_wsgi import AWSWSGIMiddleware
from app import app

application = AWSWSGIMiddleware(app)

def lambda_handler(event, context):
    return application(event, context)