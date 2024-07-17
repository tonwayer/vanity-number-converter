import json
import boto3
import itertools
from collections import defaultdict
from botocore.exceptions import ClientError

TABLE_NAME = "VanityNumbers"

digit_to_letters = {
    '2': 'ABC', '3': 'DEF', '4': 'GHI', '5': 'JKL', 
    '6': 'MNO', '7': 'PQRS', '8': 'TUV', '9': 'WXYZ'
}

word_dict = set(["CALL", "ME", "NOW", "HELP", "MY", "MONEY", "FUN", "FOOD", "HOME"])

def get_combinations(phone_number):
    # Generate all possible letter combinations for the given phone number
    char_combinations = []
    for digit in phone_number:
        if digit in digit_to_letters:
            char_combinations.append(digit_to_letters[digit])
        else:
            char_combinations.append(digit)
    return itertools.product(*char_combinations)

def score_vanity_number(vanity_number):
    # Score based on the length of recognizable words
    score = 0
    for word in word_dict:
        if word in vanity_number:
            score += len(word)
    return score

def lambda_handler(event, context):
    try:

        phone_number = event['phone_number']
        combinations = get_combinations(phone_number)
        scored_combinations = defaultdict(list)

        for comb in combinations:
            vanity_number = ''.join(comb)
            score = score_vanity_number(vanity_number)
            scored_combinations[score].append(vanity_number)

        # Sort vanity numbers by their scores in descending order
        sorted_vanity_numbers = sorted(scored_combinations.items(), key=lambda x: x[0], reverse=True)
        
        best_vanity_numbers = []
        for score, vanity_list in sorted_vanity_numbers:
            for vn in vanity_list:
                if len(best_vanity_numbers) < 5:
                    best_vanity_numbers.append(vn)
                else:
                    break
            if len(best_vanity_numbers) >= 5:
                break

        # Save to DynamoDB
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(TABLE_NAME)
        table.put_item(
            Item={
                'PhoneNumber': phone_number,
                'VanityNumbers': best_vanity_numbers
            }
        )

        return {
            'statusCode': 200,
            'body': {
                'PhoneNumber': phone_number,
                'VanityNumbers': best_vanity_numbers
            }
        }

    except ClientError as e:
        print(e.response['Error']['Message'])
        return {
            'statusCode': 500,
            'body': json.dumps('Error saving to DynamoDB')
        }
    except Exception as e:
        print(str(e))
        return {
            'statusCode': 500,
            'body': json.dumps('An unknown error occurred')
        }
