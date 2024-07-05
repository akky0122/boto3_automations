import json
import boto3

# Replace with your new identity store ID
new_identity_store_id = 'identity_store_id'

# Initialize AWS Identity Store client
identity_store_client = boto3.client('identitystore')

# Load groups data from JSON file
with open('groups.json', 'r') as file:
    groups_data = json.load(file)
    groups = groups_data['Groups']

# Function to create a group
def create_group(group):
    try:
        # Provide a default description if none exists
        description = group.get('Description', 'Default group description')

        # Create group in the new identity store
        response = identity_store_client.create_group(
            IdentityStoreId=new_identity_store_id,
            DisplayName=group['DisplayName'],
            Description=description
        )
        print(f"Created group: {group['DisplayName']}")
    except identity_store_client.exceptions.ConflictException:
        print(f"Error creating group {group['DisplayName']}: Duplicate GroupDisplayName")
    except Exception as e:
        print(f"Error creating group {group['DisplayName']}: {e}")

# Iterate over the groups and create them in the new identity store
for group in groups:
    create_group(group)

print("Group creation process completed.")
