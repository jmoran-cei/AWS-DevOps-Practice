from aws_cdk import App
from common.common_stack import ItemsApiStack

app = App()
ItemsApiStack(app, "ItemsApiStack")
app.synth()
