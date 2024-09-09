import secrets
import string

def generate_api_key(length=32):
    """Generate a securely random API key."""
    # Define the characters to use for the API key
    alphabet = string.ascii_letters + string.digits
    # Generate a secure random string using the secrets module
    api_key = ''.join(secrets.choice(alphabet) for _ in range(length))
    return api_key

def main():
    # Generate an API key of a desired length (32 characters by default)
    api_key = generate_api_key()
    print(f"Generated API Key: {api_key}")
    


if __name__ == "__main__":
    main()
