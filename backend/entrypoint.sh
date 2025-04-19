#!/bin/bash

#If an argument is provided, try to execute the corresponding Python script
if [ -n "$1" ]; then
    script_path="/backend/scripts/$1.py"
    if [ -f "$script_path" ]; then
        python "$script_path"
        exit 0
    else
        echo "Error: Script '$1.py' not found in /backend/scripts/"
        exit 1
    fi
fi

#If no argument is provided, run the default backend
exec uvicorn main:app --host 0.0.0.0 --port 80 --reload