#!/bin/bash

# Define the list of files


files=(

/Users/alexdevoid/Documents/Chat_w_Congress_GPT/chat_with_congress/tests/test_endpoints.py
/Users/alexdevoid/Documents/Chat_w_Congress_GPT/chat_with_congress/tests/test_chunking.py

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
