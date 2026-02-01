#!/usr/bin/env fish
# Guards your code before testing it.

echo "Guard!" &&
 poetry run isort ./src/ &&
 poetry run black ./src/ &&
 poetry run pylint ./src/ &&
 poetry run mypy ./src/ &&
 poetry run pytest \
  ./src/slim/test_*.py \
  ./src/sample_slim_application/test_*.py &&
 echo "Done."
