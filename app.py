from flask import Flask, jsonify
import boto3
import botocore

app = Flask(__name__)

AWS_REGION = "us-east-2"
TABLE_NAME = "customerMaster"

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table(TABLE_NAME)

@app.route("/")
def hello_world():
    return "Hello World from Flask + DynamoDB"

@app.route("/customers/<customer_id>")
def get_customer(customer_id):
    try:
        print(f"Fetching customerId: {customer_id}")
        response = table.get_item(Key={"customerID": customer_id})
        print("DynamoDB response:", response)
        item = response.get("Item")
        if not item:
            return jsonify({
                "error": "Customer not found",
                "customerId": customer_id,
                "full_response": response
            }), 404
        return jsonify(item)
    except botocore.exceptions.ClientError as e:
        error = e.response['Error']['Message']
        print(f"ClientError: {error}")
        return jsonify({"error": error}), 500
    except Exception as e:
        print(f"Exception: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)