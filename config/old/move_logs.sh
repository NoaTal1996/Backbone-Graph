#!/bin/bash
set -e

# Absolute path of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Backbone-Graph root (two levels up from src/config)
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

LOGS_DIR="$PROJECT_ROOT/logs"
mkdir -p "$LOGS_DIR"

echo "Moving log files to: $LOGS_DIR"
echo "--------------------------------"

find "$PROJECT_ROOT" \
  -type f \( -name "*.out" -o -name "*.err" \) \
  ! -path "$LOGS_DIR/*" \
  -print \
  -exec mv {} "$LOGS_DIR/" \;

echo "--------------------------------"
echo "Done."
