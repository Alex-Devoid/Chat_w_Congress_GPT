import secrets

# Generate a 32-byte random API key
api_key = secrets.token_urlsafe(32)
print(api_key)