# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands
- `python manage.py runserver` - Run local development server
- `just test` - Run all tests
- `just test path/to/file.py` - Run specific test file
- `just test app_name.tests.TestClass.test_method` - Run single test
- `just build` - Build Docker containers
- `just static` - Build static assets (including Tailwind CSS)
- `just lint` - Run all pre-commit hooks including our linter and python code formatter

## Code Style
- Python version: 3.10+
- Django version: 4.2
- Line length: 120 characters
- Formatting: ruff-format (similar to Black)
- Naming: PEP8 (snake_case for variables/functions, CamelCase for classes)
- Imports: Django convention (stdlib, third-party, Django, local apps)
- HTML formatting: 4-space tabs via djhtml
- Error handling: Try/except with specific exceptions
- Type annotations: Used where beneficial (not strictly enforced)

## Project templates
- Our shared templates live and main trailhawks.com templates live in: templates/tailwind/defaults
- Our hawkhundred.com custom templates live in: templates/tailwind/hawkhundred.com
- Some shared race templates are in: templates/tailwind/race_defaults
