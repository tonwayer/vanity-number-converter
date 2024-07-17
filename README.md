# Vanity Number Converter

This project converts phone numbers to vanity numbers using AWS Lambda and DynamoDB. It includes a deployment package built with AWS SAM.

## Setup and Deployment

### Prerequisites

- AWS CLI installed and configured
- AWS SAM CLI installed
- Python 3.8 installed

### Build and Deploy

1. **Build your SAM application**

    ```bash
    sam build
    ```

2. **Deploy your SAM application**

    ```bash
    sam deploy --guided
    ```

    Follow the prompts to configure your deployment:
    - **Stack Name**: vanity-number-converter
    - **AWS Region**: us-east-1
    - **Confirm changes before deploy**: Y
    - **Allow SAM CLI to create IAM roles**: Y
    - **Save arguments to samconfig.toml**: Y

### Import Amazon Connect Contact Flow

1. **Sign in to Amazon Connect**

2. **Go to Routing -> Contact Flows**

3. **Create a new contact flow and import the provided JSON configuration**

4. **Save and Publish the contact flow**

## Test

1. Go to the AWS Lambda console.
2. Create a test event with the following JSON:

    ```json
    {
      "Details": {
        "ContactData": {
          "CustomerEndpoint": {
            "Address": "2345678901"
          }
        }
      }
    }
    ```

3. Run the test and verify the output.
