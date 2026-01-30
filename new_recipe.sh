#!/bin/bash

# Check if arguments are provided
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: ./new_recipe.sh \"Recipe Title\" category"
    echo "Example: ./new_recipe.sh \"Spicy Tacos\" mexican"
    exit 1
fi

TITLE="$1"
CATEGORY="$2"

# Convert title to slug (lowercase, spaces to hyphens, remove special chars)
SLUG=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd '[:alnum:]-')
FILENAME="${SLUG}.md"

# Define paths
TEMPLATE="templates/recipe.md"
TARGET_DIR="docs/recipes/$CATEGORY"
TARGET_FILE="$TARGET_DIR/$FILENAME"

# Create category directory if it doesn't exist
mkdir -p "$TARGET_DIR"

# Copy template and replace title
cp "$TEMPLATE" "$TARGET_FILE"

# Use sed to replace the first line with the actual title
# Different syntax for Mac (BSD sed) vs Linux (GNU sed)
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "1s/# Recipe Title/# $TITLE/" "$TARGET_FILE"
else
    sed -i "1s/# Recipe Title/# $TITLE/" "$TARGET_FILE"
fi

echo "✅ Created new recipe: $TARGET_FILE"
