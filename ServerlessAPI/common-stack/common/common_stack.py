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

        # IAM Role for Lambda
        lambda_role = iam.Role(
            self, 
            "LambdaExecutionRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
        )

        # Granting permissions to Lambda Role
        table.grant_read_data(lambda_role)

        # Lambdas
        get_function = _lambda.Function( 
            self,
            "GetSampleItemFunc",
            function_name='ItemsApiStack-GetSampleItemFunc',
            runtime=_lambda.Runtime.NODEJS_20_X,
            handler="index.handler",
            code=_lambda.Code.from_asset("../get-item-lambda/dist"), 
            environment={"TABLE_NAME": table.table_name},
            role=lambda_role,
        )

        # **** Starting with one lambda for simplicity, then will add the others. Also want to get practice re-initiating an update of a stack
        # insert_function = _lambda.Function(
        #     self,
        #     "InsertSampleItemFunc",
        #     runtime=_lambda.Runtime.NODEJS_20_X,
        #     handler="index.handler",
        #     code=_lambda.Code.from_asset("../insert-item/src"), 
        #     environment={"TABLE_NAME": table.table_name},
        # )

        # update_function = _lambda.Function(
        #     self,
        #     "UpdateSampleItemFuncn",
        #     runtime=_lambda.Runtime.NODEJS_20_X,
        #     handler="index.handler",
        #     code=_lambda.Code.from_asset("../update-item/src"),
        #     environment={"TABLE_NAME": table.table_name},
        # )

        # API Gateway
        api = apigateway.RestApi(self, "SampleItemAPI")

        # Configure Endpoints and Resource Access
        items_resource = api.root.add_resource("items")
        item_resource = items_resource.add_resource("{itemId}")
        item_resource.add_method("GET", apigateway.LambdaIntegration(get_function))

        # items_resource.add_method("POST", apigateway.LambdaIntegration(insert_function))
        # items_resource.add_method("PUT", apigateway.LambdaIntegration(update_function))
