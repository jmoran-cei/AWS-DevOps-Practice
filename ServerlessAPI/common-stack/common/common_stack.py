from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_iam as iam,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    aws_apigateway as apigateway
)
from constructs import Construct

class ItemsApiStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # DynamoDB Table
        table = dynamodb.Table(
            self,
            "SampleItemsDDBResource",
            table_name="SampleItemsTable",
            partition_key=dynamodb.Attribute(
                name="itemId", type=dynamodb.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.RETAIN,  # Keep table data independently from stack
        )

        # IAM Roles for Lambdas
        get_lambda_role = iam.Role(
            self, 
            "GetLambdaExecutionRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
        )
        update_lambda_role = iam.Role(
            self, 
            "UpdateLambdaExecutionRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
        )

        # Granting permissions to Lambda Roles
        table.grant_read_data(get_lambda_role)
        table.grant_read_data(update_lambda_role)
        table.grant_write_data(update_lambda_role)

        # Lambdas
        get_function = _lambda.Function( 
            self,
            "GetSampleItemFunc",
            function_name='ItemsApiStack-GetSampleItemFunc',
            runtime=_lambda.Runtime.NODEJS_20_X,
            handler="index.handler",
            code=_lambda.Code.from_asset("../get-item-lambda/dist"), 
            environment={"TABLE_NAME": table.table_name},
            role=get_lambda_role,
        )
        update_function = _lambda.Function( 
            self,
            "UpdateSampleItemFunc",
            function_name='ItemsApiStack-UpdateSampleItemFunc',
            runtime=_lambda.Runtime.NODEJS_20_X,
            handler="index.handler",
            code=_lambda.Code.from_asset("../update-item-lambda/dist"), 
            environment={"TABLE_NAME": table.table_name},
            role=update_lambda_role,
        )

        # API Gateway
        api = apigateway.RestApi(self, "SampleItemAPI")

        # -- Configure Endpoints and Resource Access --
        items_resource = api.root.add_resource("items")
        item_resource = items_resource.add_resource("{itemId}") # Set itemId param
        # GET item
        item_resource.add_method("GET", apigateway.LambdaIntegration(get_function))
        # PUT item
        items_resource.add_method("PUT", apigateway.LambdaIntegration(update_function))
