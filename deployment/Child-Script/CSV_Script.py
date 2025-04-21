import boto3
import csv
import io
import time
from datetime import datetime

# AWS clients
config_client = boto3.client('config')
s3_client = boto3.client('s3')

# Configuration
S3_BUCKET_NAME = "demo-python-separate-bucket-name"  # Replace with your S3 bucket name
S3_FILE_NAME = f"config-rules-compliance-{datetime.now().strftime('%Y-%m-%d')}.csv"

def get_all_config_rules():
    """Retrieve all AWS Config rules."""
    rules = []
    response = config_client.describe_config_rules()
    
    while True:
        rules.extend(response.get("ConfigRules", []))
        if "NextToken" in response:
            response = config_client.describe_config_rules(NextToken=response["NextToken"])
        else:
            break

    return [rule["ConfigRuleName"] for rule in rules]

def get_config_rule_evaluations(rule_name):
    """Fetch compliance details of a given AWS Config rule."""
    evaluations = []
    response = config_client.get_compliance_details_by_config_rule(
        ConfigRuleName=rule_name,
        ComplianceTypes=['COMPLIANT', 'NON_COMPLIANT'],
        Limit=100
    )

    while True:
        evaluations.extend(response.get('EvaluationResults', []))
        if 'NextToken' in response:
            response = config_client.get_compliance_details_by_config_rule(
                ConfigRuleName=rule_name,
                ComplianceTypes=['COMPLIANT', 'NON_COMPLIANT'],
                Limit=100,
                NextToken=response['NextToken']
            )
        else:
            break

    return evaluations

def write_csv_to_s3(data, bucket_name, file_name):
    """Write data to a CSV file and upload it to S3."""
    csv_buffer = io.StringIO()
    csv_writer = csv.writer(csv_buffer)
    
    # Writing headers
    csv_writer.writerow(["ConfigRuleName", "ResourceId", "ComplianceType", "Annotation", "TimeStamp"])
    
    # Writing rows
    for item in data:
        csv_writer.writerow([
            item["ConfigRuleName"],
            item["ResourceId"],
            item["ComplianceType"],
            item.get("Annotation", "N/A"),
            item["ResultRecordedTime"]
        ])
    print("Generated Value are as follows - ")
    print(csv_buffer.getvalue())
    # Upload to S3
    s3_client.put_object(
        Bucket=bucket_name,
        Key=file_name,
        Body=csv_buffer.getvalue()
    )
    print(f"CSV file uploaded successfully to s3://{bucket_name}/{file_name}")
    return csv_buffer.getvalue()

def lambda_handler(event, context):
    all_rules = get_all_config_rules()
    all_evaluations = []
    time.sleep(60)
    for rule in all_rules:
        evaluations = get_config_rule_evaluations(rule)
        for eval_result in evaluations:
            all_evaluations.append({
                "ConfigRuleName": rule,
                "ResourceId": eval_result["EvaluationResultIdentifier"]["EvaluationResultQualifier"]["ResourceId"],
                "ComplianceType": eval_result["ComplianceType"],
                "Annotation": eval_result.get("Annotation", "N/A"),
                "ResultRecordedTime": eval_result["ResultRecordedTime"]
            })

    if not all_evaluations:
        print("No evaluation results found.")
        return

    details = write_csv_to_s3(all_evaluations, S3_BUCKET_NAME, S3_FILE_NAME)
    return details
