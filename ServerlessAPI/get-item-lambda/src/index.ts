import * as AWS from 'aws-sdk';

const dynamoDB = new AWS.DynamoDB.DocumentClient();
const tableName = process.env.TABLE_NAME;

export const handler = async (event: any): Promise<any> => {
    try {
        // Parse itemId
        const itemId = event.pathParameters.itemId;

        // DynamoDB params
        const params: AWS.DynamoDB.DocumentClient.GetItemInput = {
            TableName: tableName,
            Key: { itemId: itemId },
        };

        // Retrieve item from DynamoDB
        const result = await dynamoDB.get(params).promise();

        // Check if the item exists
        if (!result.Item) {
            // Item doesn't exist
            return {
                statusCode: 404,
                body: JSON.stringify({ message: 'Item not found' }),
            };
        }

        // Success
        return {
            statusCode: 200,
            body: JSON.stringify(result.Item),
        };
    } catch (error) {
    
        // Unexpected Error
        console.error('Error retrieving item:', error);
        return {
            statusCode: 500,
            body: JSON.stringify({ message: 'Error retrieving item' }),
        };
    }
};
