import * as AWS from 'aws-sdk';

const dynamoDB = new AWS.DynamoDB.DocumentClient();
const tableName = process.env.TABLE_NAME;

export const handler = async (event: any): Promise<any> => {
    try {
        // Parse itemId
        const itemId = event.pathParameters.itemId;

        // DynamoDB params
        const params: AWS.DynamoDB.DocumentClient.DeleteItemInput = {
            TableName: tableName,
            Key: { itemId: itemId },
        };

        // Check if item exists
        const getResult = await dynamoDB.get(params).promise();

        // If the item doesn't exist, return a 404 error
        if (!getResult.Item) {
            return {
                statusCode: 404,
                body: JSON.stringify({ message: 'Item not found' }),
            };
        }

        // Delete item from DynamoDB
        await dynamoDB.delete(params).promise();

        // Success
        return {
            statusCode: 204,
            body: JSON.stringify({ message: 'Item deleted successfully' }),
        };
    } catch (error) {
        // Unexpected Error
        console.error('Error deleting item:', error);
        return {
            statusCode: 500,
            body: JSON.stringify({ message: 'Error deleting item' }),
        };
    }
};
