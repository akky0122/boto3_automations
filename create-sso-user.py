import json
import boto3

# Replace with your new Identity Store ID
new_identity_store_id = 'identity_store_id'

# Initialize AWS Identity Store client
identity_store_client = boto3.client('identitystore')

# Load users from JSON file
with open('users.json', 'r') as file:
    data = json.load(file)
    users = data['Users']

# Function to create a user in the new identity store
def create_user(user):
    try:
        response = identity_store_client.create_user(
            IdentityStoreId=new_identity_store_id,
            UserName=user['UserName'],
            Name=user['Name'],
            DisplayName=user['DisplayName'],
            Emails=user['Emails']
        )
        print(f"Created user: {user['UserName']}")
    except Exception as e:
        print(f"Error creating user {user['UserName']}: {e}")

# Iterate over the users and create them in the new identity store
for user in users:
    create_user(user)
