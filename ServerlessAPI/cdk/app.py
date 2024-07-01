from aws_cdk import core
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_apigateway as apigateway

class ItemsApiStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # DynamoDB Table
        table = dynamodb.Table(
            self,
            "SampleItems",
            partition_key=dynamodb.Attribute(
                name="itemId", type=dynamodb.AttributeType.STRING
            ),
            removal_policy=core.RemovalPolicy.RETAIN,  # Keep table data independently from stack
        )

        # Lambdas
        get_function = _lambda.Function( 
            self,
            "GetSampleItemFunc",
            runtime=_lambda.Runtime.NODEJS_20_X,
            handler="index.handler",
            code=_lambda.Code.from_asset("../get-item/src"), 
            environment={"TABLE_NAME": table.table_name},
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

        items_resource = api.root.add_resource("items")
        items_resource.add_method("GET", apigateway.LambdaIntegration(get_function))
        # items_resource.add_method("POST", apigateway.LambdaIntegration(insert_function))
        # items_resource.add_method("PUT", apigateway.LambdaIntegration(update_function))


app = core.App()
ItemsApiStack(app, "ItemsApiStack")
app.synth()
