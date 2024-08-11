#!/bin/bash

# Create the new directory structure
echo "Creating new directory structure..."
mkdir -p chat_with_congress/app/api/endpoints
mkdir -p chat_with_congress/app/api/models
mkdir -p chat_with_congress/app/api/services
mkdir -p chat_with_congress/tests

# Move existing files to the new structure
echo "Moving files to the new structure..."
mv .devcontainer chat_with_congress/
mv Dockerfile.dev chat_with_congress/
mv README.md chat_with_congress/
mv requirements.txt chat_with_congress/
mv app.py chat_with_congress/app/api/main.py

# Create empty __init__.py files
echo "Creating __init__.py files..."
touch chat_with_congress/app/api/__init__.py
touch chat_with_congress/app/api/endpoints/__init__.py
touch chat_with_congress/app/api/models/__init__.py
touch chat_with_congress/app/api/services/__init__.py
touch chat_with_congress/tests/__init__.py

# Extract endpoint functions from app.py and move them to separate files
echo "Extracting endpoint functions..."
sed -n '/@app.post/,$p' chat_with_congress/app/api/main.py > chat_with_congress/app/api/endpoints/endpoints.py
sed -i '' '/@app.post/,$d' chat_with_congress/app/api/main.py

# Extract Pydantic models from app.py and move them to models/requests.py
echo "Extracting Pydantic models..."
sed -n '/class .*Request/,/class .*/p' chat_with_congress/app/api/main.py | sed '$d' > chat_with_congress/app/api/models/requests.py
sed -i '' '/class .*Request/,/class .*/d' chat_with_congress/app/api/main.py

# Extract the remaining models to models/requests.py
echo "Moving remaining Pydantic models..."
sed -n '/class .*Request/,$p' chat_with_congress/app/api/main.py >> chat_with_congress/app/api/models/requests.py
sed -i '' '/class .*Request/,$d' chat_with_congress/app/api/main.py

# Create a placeholder for services
echo "Creating placeholder files for services..."
echo -e "# Placeholder for Congress.gov API interactions\n\n" > chat_with_congress/app/api/services/congress_api.py
echo -e "# Placeholder for chunking logic\n\n" > chat_with_congress/app/api/services/chunking.py
echo -e "# Placeholder for semantic search logic\n\n" > chat_with_congress/app/api/services/semantic_search.py

# Clean up and final touches
echo "Cleaning up and finalizing..."
mv chat_with_congress/app/api/endpoints/endpoints.py chat_with_congress/app/api/endpoints/members.py
echo -e "# Main application setup\n\n" >> chat_with_congress/app/api/main.py
echo "Project restructured successfully!"
