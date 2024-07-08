import * as AWS from 'aws-sdk';

const dynamoDB = new AWS.DynamoDB.DocumentClient();
const tableName = process.env.TABLE_NAME;

export const handler = async (event: any): Promise<any> => {
    try {
        // Parse itemId and the new item data
        const itemId = event.pathParameters.itemId;
        let newData;

        // Check if the body is valid JSON
        try {
            newData = JSON.parse(event.body);
        } catch (error) {
            // Invalid JSON
            console.error('Invalid JSON:', error);
            return {
                statusCode: 400,
                body: JSON.stringify({ message: 'Invalid JSON' }),
            };
        }

        // Check if name and description are provided
        if (!newData.name || !newData.description) {
            return {
                statusCode: 400,
                body: JSON.stringify({ message: 'Both name and description must be provided' }),
            };
        }

        // Check if item exists
        const getItemParams: AWS.DynamoDB.DocumentClient.GetItemInput = {
            TableName: tableName,
            Key: { itemId: itemId },
        };
        const getResult = await dynamoDB.get(getItemParams).promise();

        // If the item doesn't exist, return a 404 error
        if (!getResult.Item) {
            return {
                statusCode: 404,
                body: JSON.stringify({ message: 'Item not found' }),
            };
        }

        // If the item exists, update it
        const updateParams: AWS.DynamoDB.DocumentClient.UpdateItemInput = {
            TableName: tableName,
            Key: { itemId: itemId },
            ExpressionAttributeNames: {
                '#name': 'name',
                '#description': 'description',
            },
            ExpressionAttributeValues: {
                ':name': newData.name,
                ':description': newData.description,
            },
            UpdateExpression: 'SET #name = :name, #description = :description',
            ReturnValues: 'ALL_NEW',
        };
        const updateResult = await dynamoDB.update(updateParams).promise();

        // Success
        return {
            statusCode: 204,
            body: JSON.stringify({
                name: updateResult.Attributes.name,
                description: updateResult.Attributes.description
            })
        };
    } catch (error) {
        // Unexpected Error
        console.error('Error updating item:', error);
        return {
            statusCode: 500,
            body: JSON.stringify({ message: 'Error updating item' }),
        };
    }
};
