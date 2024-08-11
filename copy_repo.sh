#!/bin/bash

# Define the list of files


files=(
/app/chat_with_congress/app/api/models/requests.py
/app/chat_with_congress/app/api/endpoints/members.py
/app/chat_with_congress/app/api/main.py

)


# Concatenate filenames and their contents
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "Filename: $file"
        echo "\`\`\`"
        cat "$file"
        echo "\`\`\`"
        echo # Add an empty line for separation
    else
        echo "File not found: $file"
    fi
done | pbcopy

echo "The filenames and their contents have been copied to the clipboard."
