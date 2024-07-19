import json
import boto3
import itertools
from collections import defaultdict
from botocore.exceptions import ClientError

TABLE_NAME = "VanityNumbers"
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

digit_to_letters = {
    '2': 'ABC', '3': 'DEF', '4': 'GHI', '5': 'JKL', 
    '6': 'MNO', '7': 'PQRS', '8': 'TUV', '9': 'WXYZ'
}

word_dict = set([
    "CALL", "ME", "NOW", "HELP", "MY", "MONEY", "FUN", "FOOD", "HOME", "FREE", 
    "GIFT", "LOVE", "LIFE", "SAVE", "TALK", "WORK", "FIND", "GOOD", "BEST", 
    "SHOP", "DEAL", "COOL", "EASY", "LIVE", "JOIN", "NEW", "HOT", "FAST", 
    "CARE", "SAFE", "TEAM", "WIN", "WOW", "KIND", "PLAN", "TOP", "HIT", 
    "BIG", "SMILE", "GREAT", "HAPPY", "BRIGHT", "SMART", "CLEAR", "PEACE",
    "LUCKY", "TRUST", "CALM", "HONEST", "PRO", "VIP", "STAR", "KING", "QUEEN", 
    "CHAMP", "GOAL", "HERO", "GLOW", "DREAM", "HOPE", "JOY", "FUNNY", "HUGS",
    "CHEER", "BOLD", "ZEN", "MAGIC", "SHINE", "WAVE", "WISE", "UNITY", 
    "GRACE", "STRONG", "BRAVE", "FOCUS", "POWER", "ENERGY", "LIGHT", "SOUL",
    "HEART", "HANDS", "MIND", "BODY", "SPIRIT", "ACTION", "YOUTH", "BLOOM",
    "ROCK", "JAZZ", "BLUES", "POET", "SONG", "TUNE", "DANCE", "VIBE", "BEAT"
])

# Precompute scores for words in word_dict to optimize scoring
precomputed_scores = {word: len(word) for word in word_dict}

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
    # Score based on the length of recognizable words using precomputed scores
    score = 0
    for word, word_score in precomputed_scores.items():
        if word in vanity_number:
            score += word_score
    return score

def is_valid_phone_number(phone_number):
    # Validate that the phone number contains only valid digits
    return all(digit in digit_to_letters or digit.isdigit() for digit in phone_number)

def lambda_handler(event, context):
    if event.get('httpMethod') == 'GET':
        try:
            response = table.scan(Limit=5)
            items = response.get('Items', [])
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },
                'body': json.dumps(items)
            }
        except ClientError as e:
            print(f"ClientError: {e.response['Error']['Message']}")
            return {
                'statusCode': 500,
                'body': json.dumps('Error retrieving data from DynamoDB')
            }
    else:
        try:
            phone_number = event['Details']['ContactData']['CustomerEndpoint']['Address']
            
            if not is_valid_phone_number(phone_number):
                return {
                    'statusCode': 400,
                    'body': json.dumps('Invalid phone number format')
                }
                
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
            table.put_item(
                Item={
                    'PhoneNumber': phone_number,
                    'VanityNumbers': best_vanity_numbers
                }
            )
            print(f"Successfully saved vanity numbers for {phone_number}: {best_vanity_numbers}")
            response = {
                'VanityNumber1': best_vanity_numbers[0] if len(best_vanity_numbers) > 0 else '',
                'VanityNumber2': best_vanity_numbers[1] if len(best_vanity_numbers) > 1 else '',
                'VanityNumber3': best_vanity_numbers[2] if len(best_vanity_numbers) > 2 else ''
            }
            return {
                'statusCode': 200,
                'body': json.dumps(response)
            }

        except ClientError as e:
            print(f"ClientError: {e.response['Error']['Message']}")
            return {
                'statusCode': 500,
                'body': json.dumps('Error saving to DynamoDB')
            }
        except Exception as e:
            print(f"Exception: {str(e)}")
            return {
                'statusCode': 500,
                'body': json.dumps('An unknown error occurred')
            }
