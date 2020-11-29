find . -iname "*.py" -exec pylint -E {} ;\
FILES=$(find . -iname "*.py")
pylint -E $FILES