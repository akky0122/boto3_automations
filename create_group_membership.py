import json
import boto3

# Replace with your new identity store ID
new_identity_store_id = 'identity_store_id'

# Initialize AWS Identity Store client
identity_store_client = boto3.client('identitystore')

# Load the users to groups data from JSON file
with open('users_to_groups.json', 'r') as file:
    users_to_groups = json.load(file)

# Function to get user ID by user name
def get_user_id_by_username(username):
    try:
        response = identity_store_client.list_users(
            IdentityStoreId=new_identity_store_id,
            Filters=[{'AttributePath': 'UserName', 'AttributeValue': username}]
        )
        if response['Users']:
            return response['Users'][0]['UserId']
        else:
            print(f"User {username} not found in new identity store.")
            return None
    except Exception as e:
        print(f"Error retrieving user ID for {username}: {e}")
        return None

# Function to get group ID by group name
def get_group_id_by_groupname(groupname):
    try:
        response = identity_store_client.list_groups(
            IdentityStoreId=new_identity_store_id,
            Filters=[{'AttributePath': 'DisplayName', 'AttributeValue': groupname}]
        )
        if response['Groups']:
            return response['Groups'][0]['GroupId']
        else:
            print(f"Group {groupname} not found in new identity store.")
            return None
    except Exception as e:
        print(f"Error retrieving group ID for {groupname}: {e}")
        return None

# Iterate over the groups and add users to their respective groups
for group in users_to_groups['Groups']:
    group_name = group['GroupName']
    users = group['Users']
    print(f"Processing group: {group_name}")
    group_id = get_group_id_by_groupname(group_name)
    if group_id:
        for username in users:
            user_id = get_user_id_by_username(username)
            if user_id:
                try:
                    identity_store_client.create_group_membership(
                        IdentityStoreId=new_identity_store_id,
                        GroupId=group_id,
                        MemberId={'UserId': user_id}
                    )
                    print(f"Added {username} to group {group_name}.")
                except Exception as e:
                    print(f"Error adding {username} to group {group_name}: {e}")

print("Completed adding users to groups.")

