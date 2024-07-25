import * as AWS from 'aws-sdk';
import { v4 as uuidv4 } from 'uuid';

const dynamoDB = new AWS.DynamoDB.DocumentClient();
const tableName = process.env.TABLE_NAME;

export const handler = async (event: any): Promise<any> => {
    try {
        // Parse the new item data
        let newData;

        // Check if the body is valid JSON
        try {
            newData = JSON.parse(event.body); // assuming the new data is in the body of the request
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
                body: JSON.stringify({ message: 'Both "name" and "description" must be provided' }),
            };
        }

        // Generate a unique itemId
        const itemId = uuidv4();

        // DynamoDB params
        const params: AWS.DynamoDB.DocumentClient.PutItemInput = {
            TableName: tableName,
            Item: {
                itemId: itemId,
                name: newData.name,
                description: newData.description,
            },
        };

        // Insert item into DynamoDB
        await dynamoDB.put(params).promise();

        // Success
        return {
            statusCode: 201,
            body: JSON.stringify({
                itemId: params.Item.itemId,
                name: params.Item.name,
                description: params.Item.description
            }),
        };
    } catch (error) {
        // Unexpected Error
        console.error('Error inserting item:', error);
        return {
            statusCode: 500,
            body: JSON.stringify({ message: 'Error inserting item' }),
        };
    }
};
