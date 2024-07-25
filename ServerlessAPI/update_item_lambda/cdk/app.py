import aws_cdk as cdk
from cdk.cdk_stack import UpdateItemLambda

app = cdk.App()
UpdateItemLambda(app, "UpdateItemLambdaStack")
app.synth()
