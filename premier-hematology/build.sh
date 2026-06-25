#!/bin/bash
# Full site build — generates all pages AND injects forms in one step.
# Usage: ./build.sh
set -e
cd "$(dirname "$0")"
python3 generate.py
# build_forms.py is called automatically at the end of generate.py
echo ""
echo "✅ Full build complete"
