import json
import boto3

def evaluate_compliance():
    client = boto3.client("config")
    response = client.describe_config_rules()
    evaluations = []
    
    for rule in response.get("ConfigRules", []):
        rule_name = rule["ConfigRuleName"]
        if rule_name.startswith("configrule-"):
            compliance_type = "COMPLIANT"
            Annotation = "Following Naming pattern"
        else:
            compliance_type = "NON_COMPLIANT"
            Annotation = "Config rules is not in correct naming convention it should start with configrule-"
        evaluations.append({
            "ComplianceResourceType": "AWS::Config::ConfigRule",
            "ComplianceResourceId": rule_name,
            "ComplianceType": compliance_type,
            "Annotation": Annotation
        })
    
    return evaluations

def lambda_handler(event, context):
    config_client = boto3.client("config")
    evaluations = evaluate_compliance()
    
    if evaluations:
        response = config_client.put_evaluations(
            Evaluations=[{
                "ComplianceResourceType": eval["ComplianceResourceType"],
                "ComplianceResourceId": eval["ComplianceResourceId"],
                "ComplianceType": eval["ComplianceType"],
                "Annotation": eval["Annotation"],
                "OrderingTimestamp": json.loads(event["invokingEvent"]).get("notificationCreationTime")
            } for eval in evaluations],
            ResultToken=event["resultToken"]
        )
    
    return response
