from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_lambda as _lambda
)
from aws_cdk.aws_dynamodb import Table
from constructs import Construct

iam_lambda_serv_principal = iam.ServicePrincipal("lambda.amazonaws.com")
mngd_lambda_exec_role = iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")

class DeleteItemLambda(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Get parameters from context
        # Get 'env' from context (e.g., 'prod', 'stage', etc.)
        env = self.node.try_get_context('env')

        # Get the environment-specific context
        env_context = self.node.try_get_context(env)
        common_stack_context = env_context['commonStack']
        table_name = common_stack_context['tableName']
        lambda_stack_context = env_context['lambdaStack']
        name = lambda_stack_context['name']
        codepath = lambda_stack_context['codepath']

        # Reference existing resources
        table = Table.from_table_name(self, f"{table_name}DDBResource", table_name)

        # IAM Role for Lambda
        lambda_role = iam.Role(
            self,
            f"{name}LambdaExecutionRole",
            assumed_by=iam_lambda_serv_principal,
        )

        # Granting permissions to Lambda Role
        table.grant_read_write_data(lambda_role)
        lambda_role.add_managed_policy(mngd_lambda_exec_role)

        # Lambda
        _lambda.Function(
            self,
            name,
            function_name=name,
            runtime=_lambda.Runtime.NODEJS_20_X,
            handler="index.handler",
            code=_lambda.Code.from_asset(codepath),
            environment={"TABLE_NAME": table.table_name},
            role=lambda_role,
        )
        