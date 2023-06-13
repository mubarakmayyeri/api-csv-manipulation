from dotenv import load_dotenv
from decouple import config
import secrets

# Load environment variables
load_dotenv('.env')

# Generate API key
def generate_api_key():
    return secrets.token_hex(16)  # Generate a random hex string as the API key

# Append API key to .env file
def append_api_key(api_key):
    api_keys = config('API_KEYS', default='')

    if api_keys:
        # Check if the API key already exists in the API_KEYS variable
        if api_key not in api_keys.split(','):
            api_keys += ',' + api_key
    else:
        api_keys = api_key

    # Update the API_KEYS variable in the .env file
    with open('.env', 'r') as file:
        lines = file.readlines()

    with open('.env', 'w') as file:
        for line in lines:
            if line.startswith('API_KEYS='):
                line = f'API_KEYS={api_keys}\n'
            file.write(line)

# Generate and append API key
if __name__ == '__main__':
    api_key = generate_api_key()
    append_api_key(api_key)
    print(f"API key generated: {api_key}")