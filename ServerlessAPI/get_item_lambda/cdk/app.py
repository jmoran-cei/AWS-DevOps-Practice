import aws_cdk as cdk
from cdk.cdk_stack import GetItemLambda

app = cdk.App()
GetItemLambda(app, "GetItemLambdaStack")
app.synth()
