# Vanity Number Converter

## Overview
This project converts phone numbers to vanity numbers and saves the best 5 resulting vanity numbers and the caller's number in a DynamoDB table. The project includes a Lambda function, an Amazon Connect contact flow, and a web application to display the vanity numbers.

## Determining the "Best" Vanity Numbers
The "best" vanity numbers are determined based on a scoring algorithm. The algorithm evaluates potential vanity numbers by the length and relevance of recognizable words within them. Words are chosen from a predefined dictionary of meaningful words (e.g., "CALL", "HELP", "SAVE"). Each word found within a vanity number contributes to the overall score of that number. The top 5 vanity numbers with the highest scores are selected as the "best" ones.

### Example
For the phone number `18005551234`, possible vanity numbers might be `1-800-CALL-1234`, `1-800-HELP-1234`, etc. The algorithm scores these based on the presence and length of the words "CALL" and "HELP", respectively.

## Implementation Details
- **Lambda Function**: The function `lambda_function.py` is responsible for generating and scoring vanity numbers. It uses a dictionary of digits to letters and a set of predefined words to generate potential vanity numbers and score them.
- **DynamoDB**: The results are stored in a DynamoDB table, which keeps the original phone number and the top 5 vanity numbers.
- **Amazon Connect**: An Amazon Connect contact flow retrieves the vanity numbers from the Lambda function and reads out the top 3 possibilities to the caller.
- **Web Application**: A React web application displays the vanity numbers from the last 5 callers by fetching data from the API endpoint.

## Challenges and Solutions
- **Generating Meaningful Vanity Numbers**: Creating a comprehensive dictionary of meaningful words was crucial. This dictionary directly influences the quality of the generated vanity numbers.
- **Performance Optimization**: To ensure efficient processing, the scoring algorithm precomputes scores for words and avoids recalculations for each phone number.

## Future Improvements
- **Expanded Dictionary**: Increasing the dictionary size to include more meaningful words.
- **Enhanced Scoring Algorithm**: Improving the algorithm to better recognize and prioritize more complex word patterns.
- **User Customization**: Allowing users to customize the dictionary of words based on their specific needs or preferences.

## Deployment

### Prerequisites
- AWS CLI configured with appropriate permissions
- Node.js and npm installed

### Backend Deployment
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/vanity-number-converter.git
   cd backend
   ```

2. Deploy the backend using AWS SAM:
   ```bash
   sam build
   sam deploy --guided
   ```

3. Note the output API URL from the deployment process.

### Web Application Setup
1. Create a `.env` file in the root of the `frontend` directory with the following content:
   ```bash
   REACT_APP_API_URL=https://your-api-url.execute-api.us-east-1.amazonaws.com/Prod/vanitynumbers
   ```

2. Install the dependencies and run the web application:
   ```bash
   cd frontend
   npm install
   npm start
   ```

3. Open your browser and navigate to `http://localhost:3000` to see the web application in action.

### Amazon Connect Setup
1. Create an Amazon Connect instance if you don't have one already.
2. Import `backend/aws-connect-flow.json` into your Amazon Connect instance.
3. Ensure the Lambda function ARN is correctly referenced in the contact flow.

## Architecture Diagram
![Architecture Diagram](path/to/your/architecture-diagram.png)

## Writing and Documentation
### Reasons for Implementation
The solution was implemented to leverage AWS serverless technologies for scalability and cost-effectiveness. The Lambda function handles the core logic of converting phone numbers to vanity numbers and storing them in DynamoDB, ensuring quick retrieval and scalability. The web application provides a user-friendly interface to display the vanity numbers, while the Amazon Connect integration allows for real-time interaction with callers.

### Struggles and Problems Overcome
- **AWS Permissions**: Configuring the correct IAM roles and policies for the Lambda function to interact with DynamoDB and API Gateway.
- **Data Processing**: Efficiently generating and scoring vanity numbers within the constraints of Lambda's execution environment.

### Shortcuts and Potential Issues
- **Dictionary Size**: The predefined dictionary of words could be expanded for better results.
- **Error Handling**: More comprehensive error handling and logging could be implemented for production.

### Potential Improvements
- **Enhanced User Interface**: Improving the web application's UI for better user experience.
- **Additional Features**: Adding features like user authentication, personalized dictionaries, and more sophisticated scoring algorithms.
