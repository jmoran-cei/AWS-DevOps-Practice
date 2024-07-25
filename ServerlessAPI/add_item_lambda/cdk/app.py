import aws_cdk as cdk
from cdk.cdk_stack import AddItemLambda

app = cdk.App()
AddItemLambda(app, "AddItemLambdaStack")
app.synth()
