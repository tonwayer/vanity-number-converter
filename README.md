# Vanity Numbers Converter

## Project Overview

This project is a full-stack application that retrieves and displays the last 5 vanity numbers from callers. It consists of a backend AWS Lambda function written in Python, deployed using AWS SAM, and a frontend React application.

## Project Directory Structure

```plaintext
my-project/
│
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── template.yaml
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   └── VanityNumbers.js
│   │   ├── App.js
│   │   ├── index.js
│   │   └── ...
│   ├── package.json
│   ├── package-lock.json
│   └── ...
│
├── README.md
└── .gitignore
```

## Backend Setup

### Prerequisites

- AWS CLI configured with your credentials
- AWS SAM CLI installed
- An S3 bucket for packaging the Lambda function code

### Steps

1. **Navigate to the `backend/` directory**:

    ```sh
    cd backend/
    ```

2. **Install dependencies**:

    ```sh
    pip install -r requirements.txt
    ```

3. **Package the SAM application**:

    ```sh
    sam package --template-file template.yaml --output-template-file packaged.yaml --s3-bucket YOUR_S3_BUCKET_NAME
    ```

    Replace `YOUR_S3_BUCKET_NAME` with the name of an existing S3 bucket.

4. **Deploy the SAM application**:

    ```sh
    sam deploy --template-file packaged.yaml --stack-name VanityNumberStack --capabilities CAPABILITY_IAM
    ```

5. **Note the API Gateway endpoint URL** from the output of the deployment. This URL will be used in the frontend application.

## Frontend Setup

### Prerequisites

- Node.js and npm installed

### Steps

1. **Navigate to the `frontend/` directory**:

    ```sh
    cd frontend/
    ```

2. **Install dependencies**:

    ```sh
    npm install
    ```

3. **Update the API Gateway URL** in `src/components/VanityNumbers.js`:

    ```javascript
    const response = await fetch('YOUR_API_GATEWAY_URL');
    ```

    Replace `YOUR_API_GATEWAY_URL` with the actual URL from the backend deployment step.

4. **Run the React application**:

    ```sh
    npm start
    ```

    The application will be available at `http://localhost:3000`.

## Project Components

### Backend

- **`app.py`**: Contains the Lambda function code to fetch the last 5 vanity numbers from DynamoDB.
- **`requirements.txt`**: Lists Python dependencies for the Lambda function.
- **`template.yaml`**: AWS SAM template that defines the Lambda function and DynamoDB table.

### Frontend

- **`src/components/VanityNumbers.js`**: React component that fetches and displays the last 5 vanity numbers.
- **`App.js`**: Main React application component.
- **`index.js`**: Entry point for the React application.
