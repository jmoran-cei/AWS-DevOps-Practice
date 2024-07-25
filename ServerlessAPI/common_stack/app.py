from aws_cdk import App
from common.common_stack import ItemsApiStack
# from get_item_lambda.cdk.cdk.cdk_stack import GetItemLambda
# from add_item_lambda.cdk.cdk.cdk_stack import AddItemLambda
# from update_item_lambda.cdk.cdk.cdk_stack import UpdateItemLambda
# from delete_item_lambda.cdk.cdk.cdk_stack import DeleteItemLambda

app = App()

# Create the common stack
common_stack = ItemsApiStack(app, "ItemsApiStack")

# Create the Lambda stacks, passing the API and resources as parameters
# get_item_lambda = GetItemLambda(app, "GetItemLambdaStack", common_stack.table, common_stack.item_resource, "../get_item_lambda/dist")
# add_item_lambda = AddItemLambda(app, "AddItemLambdaStack", common_stack.table, common_stack.item_resource, "../add_item_lambda/dist")
# update_item_lambda = UpdateItemLambda(app, "UpdateItemLambdaStack", common_stack.table, common_stack.item_resource, "../update_item_lambda/dist")
# delete_item_lambda = DeleteItemLambda(app, "DeleteItemLambdaStack", common_stack.table, common_stack.item_resource, "../delete_item_lambda/dist")

app.synth()
