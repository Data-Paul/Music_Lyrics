#!/bin/sh

# Print a welcome message
echo "Starting MusicBrainz Data Collection..."

# Check if ARTIST_NAME environment variable is set
if [ -n "$ARTIST_NAME" ]; then
    echo "Using artist name from environment variable: $ARTIST_NAME"
    # Run the Python application with the artist name
    python -m package.main
    exit $?
fi

# Check if we're running in an interactive terminal
if [ -t 0 ]; then
    # Interactive mode - the script will wait for user input
    echo "Please enter an artist name to search:"
    read ARTIST_NAME
    if [ -n "$ARTIST_NAME" ]; then
        echo "Using artist name from input: $ARTIST_NAME"
        python -m package.main
        exit $?
    else
        echo "Error: No artist name provided"
        exit 1
    fi
else
    # Non-interactive mode - try to read from stdin
    if read -r ARTIST_NAME; then
        if [ -n "$ARTIST_NAME" ]; then
            echo "Using artist name from stdin: $ARTIST_NAME"
            python -m package.main
            exit $?
        fi
    fi
    echo "Error: No artist name provided via stdin"
    exit 1
fi 