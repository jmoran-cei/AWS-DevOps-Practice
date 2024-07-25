from aws_cdk import (
    Stack,
    RemovalPolicy,
    # aws_iam as iam,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
)
from constructs import Construct

# iam_lambda_serv_principal = iam.ServicePrincipal("lambda.amazonaws.com")
# mngd_lambda_exec_role = iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")

class ItemsApiStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Get parameters from context
        # Get 'env' from context (e.g., 'prod', 'stage', etc.)
        env = self.node.try_get_context('env')

        # Get the environment-specific context
        env_context = self.node.try_get_context(env)
        dynamo_db_context = env_context['dynamoDB']
        table_name = dynamo_db_context['tableName']
        lambdas_context = env_context['lambdas']

        # DynamoDB Table
        table = dynamodb.Table(
            self,
            f"{table_name}DDBResource",
            table_name=table_name,
            partition_key=dynamodb.Attribute(
                name="itemId", type=dynamodb.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.RETAIN,  # Keep table data independently from stack
        )

        # # IAM Roles for Lambdas
        # get_lambda_role = iam.Role(
        #     self,
        #     "GetLambdaExecutionRole",
        #     assumed_by=iam_lambda_serv_principal,
        # )
        get_function = _lambda.Function.from_function_name(self, 'GetItemFunction', lambdas_context['getItem'])
        # insert_lambda_role = iam.Role(
        #     self,
        #     "InsertLambdaExecutionRole",
        #     assumed_by=iam_lambda_serv_principal,
        # )
        insert_function = _lambda.Function.from_function_name(self, 'InsertItemFunction', lambdas_context['addItem'])
        # update_lambda_role = iam.Role(
        #     self,
        #     "UpdateLambdaExecutionRole",
        #     assumed_by=iam_lambda_serv_principal,
        # )
        update_function = _lambda.Function.from_function_name(self, 'UpdateItemFunction', lambdas_context['updateItem'])
        # delete_lambda_role = iam.Role(
        #     self,
        #     "DeleteLambdaExecutionRole",
        #     assumed_by=iam_lambda_serv_principal,
        # )
        delete_function = _lambda.Function.from_function_name(self, 'DeleteItemFunction', lambdas_context['deleteItem'])

        # -- Granting permissions to Lambda Roles --
        # GET
        # table.grant_read_data(get_lambda_role)
        # get_lambda_role.add_managed_policy(mngd_lambda_exec_role)
        # POST
        # table.grant_write_data(insert_lambda_role)
        # insert_lambda_role.add_managed_policy(mngd_lambda_exec_role)
        # PUT
        # table.grant_read_write_data(update_lambda_role)
        # update_lambda_role.add_managed_policy(mngd_lambda_exec_role)
        # DELETE
        # table.grant_read_write_data(delete_lambda_role)
        # delete_lambda_role.add_managed_policy(mngd_lambda_exec_role)

        # Lambdas
        health_check_function = _lambda.Function(
            self,
            "SimpleHealthCheckFunc",
            function_name="HealthCheckFunc",
            runtime=_lambda.Runtime.NODEJS_20_X,
            handler="index.handler",
            code=_lambda.Code.from_asset("./health_check_lambda/dist"),
        )
        # get_function = _lambda.Function(
        #     self,
        #     "GetSampleItemFunc",
        #     function_name="ItemsApiStack-GetSampleItemFunc",
        #     runtime=_lambda.Runtime.NODEJS_20_X,
        #     handler="index.handler",
        #     code=_lambda.Code.from_asset("../get-item-lambda/dist"),
        #     environment={"TABLE_NAME": table.table_name},
        #     role=get_lambda_role,
        # )
        # insert_function = _lambda.Function(
        #     self,
        #     "InsertSampleItemFunc",
        #     function_name="ItemsApiStack-InsertSampleItemFunc",
        #     runtime=_lambda.Runtime.NODEJS_20_X,
        #     handler="index.handler",
        #     code=_lambda.Code.from_asset("../add-item-lambda/dist"),
        #     environment={"TABLE_NAME": table.table_name},
        #     role=insert_lambda_role,
        # )
        # update_function = _lambda.Function(
        #     self,
        #     "UpdateSampleItemFunc",
        #     function_name="ItemsApiStack-UpdateSampleItemFunc",
        #     runtime=_lambda.Runtime.NODEJS_20_X,
        #     handler="index.handler",
        #     code=_lambda.Code.from_asset("../update-item-lambda/dist"),
        #     environment={"TABLE_NAME": table.table_name},
        #     role=update_lambda_role,
        # )
        # delete_function = _lambda.Function(
        #     self,
        #     "DeleteSampleItemFunc",
        #     function_name="ItemsApiStack-DeleteSampleItemFunc",
        #     runtime=_lambda.Runtime.NODEJS_20_X,
        #     handler="index.handler",
        #     code=_lambda.Code.from_asset("../delete-item-lambda/dist"),
        #     environment={"TABLE_NAME": table.table_name},
        #     role=delete_lambda_role,
        # )

        # API Gateway
        api = apigateway.RestApi(self, "SampleItemAPI")

        # -- Configure Endpoints and Resource Access --
        api.root.add_resource("health").add_method("GET", apigateway.LambdaIntegration(health_check_function))
        items_resource = api.root.add_resource("items")
        item_resource = items_resource.add_resource("{itemId}")  # Set itemId param
        # GET item
        item_resource.add_method("GET", apigateway.LambdaIntegration(get_function))
        # POST item
        items_resource.add_method("POST", apigateway.LambdaIntegration(insert_function))
        # PUT item
        item_resource.add_method("PUT", apigateway.LambdaIntegration(update_function))
        # DELETE item
        item_resource.add_method("DELETE", apigateway.LambdaIntegration(delete_function))

        # self.table = table
        # self.items_resource = items_resource
        # self.item_resource = item_resource
