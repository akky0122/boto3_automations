import json
import boto3

# Replace with your old identity store ID
old_identity_store_id = 'identity_store_id'

# Initialize AWS Identity Store client
identity_store_client = boto3.client('identitystore')

# Load the groups data from JSON file
with open('groups.json', 'r') as file:
    groups_data = json.load(file)
    groups = groups_data['Groups']

users_to_groups = {"Groups": []}

# Function to get members of a group by group ID
def get_group_members(group_id):
    members = []
    paginator = identity_store_client.get_paginator('list_group_memberships')
    for page in paginator.paginate(IdentityStoreId=old_identity_store_id, GroupId=group_id):
        for membership in page['GroupMemberships']:
            user_id = membership['MemberId']['UserId']
            try:
                user_response = identity_store_client.describe_user(IdentityStoreId=old_identity_store_id, UserId=user_id)
                # Extract UserName directly from user_response
                if 'UserName' in user_response:
                    members.append(user_response['UserName'])
                else:
                    print(f"Warning: No 'UserName' key in response for user ID {user_id}. Response: {user_response}")
            except Exception as e:
                print(f"Error retrieving user {user_id}: {e}")
    return members

# Iterate over the groups and get their members
for group in groups:
    group_name = group['DisplayName']
    group_id = group['GroupId']
    print(f"Processing group: {group_name}")
    members = get_group_members(group_id)
    users_to_groups['Groups'].append({
        "GroupName": group_name,
        "Users": members
    })

# Save the users to groups data to a JSON file
with open('users_to_groups.json', 'w') as file:
    json.dump(users_to_groups, file, indent=4)

print("Created users_to_groups.json file.")
