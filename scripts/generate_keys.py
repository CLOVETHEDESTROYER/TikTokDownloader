import secrets
import base64
import os


def generate_key(length=32):
    """Generate a secure random key."""
    return base64.urlsafe_b64encode(secrets.token_bytes(length)).decode('utf-8')


def main():
    # Create production environment files if they don't exist
    api_env_file = 'app/api/.env.production'
    web_env_file = 'app/web/.env.production'

    # Generate keys
    api_secret_key = generate_key(32)
    jwt_secret_key = generate_key(32)
    website_api_key = generate_key(32)
    admin_api_key = generate_key(32)

    # Backend environment file content
    api_env_content = f"""ENV=production
API_SECRET_KEY={api_secret_key}
JWT_SECRET_KEY={jwt_secret_key}
WEBSITE_API_KEY={website_api_key}
ADMIN_API_KEY={admin_api_key}
FRONTEND_URL=http://localhost:3000
DOWNLOAD_FOLDER=downloads
REQUIRE_API_KEY=true
CORS_ALLOW_CREDENTIALS=true
VERIFY_SSL=false
MAX_DOWNLOADS=10
MAX_CONCURRENT_DOWNLOADS=5
DOWNLOAD_EXPIRY_MINUTES=60
ENABLE_METRICS=true
RATE_LIMIT_PER_MINUTE=60
WORKERS=4"""

    # Frontend environment file content
    web_env_content = f"""NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_WEBSITE_API_KEY={website_api_key}"""

    # Ensure directories exist
    os.makedirs(os.path.dirname(api_env_file), exist_ok=True)
    os.makedirs(os.path.dirname(web_env_file), exist_ok=True)

    # Write the files
    with open(api_env_file, 'w') as f:
        f.write(api_env_content)

    with open(web_env_file, 'w') as f:
        f.write(web_env_content)

    print("\nProduction environment files have been created successfully!")
    print("\nGenerated Keys (save these somewhere secure):")
    print(f"API_SECRET_KEY: {api_secret_key}")
    print(f"JWT_SECRET_KEY: {jwt_secret_key}")
    print(f"WEBSITE_API_KEY: {website_api_key}")
    print(f"ADMIN_API_KEY: {admin_api_key}")
    print("\nFiles created:")
    print(f"- {api_env_file}")
    print(f"- {web_env_file}")


if __name__ == "__main__":
    main()
