import aws_cdk as cdk
from cdk.cdk_stack import DeleteItemLambda

app = cdk.App()
DeleteItemLambda(app, "DeleteItemLambdaStack")
app.synth()
