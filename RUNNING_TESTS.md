# Running Tests Guide

## Prerequisites
Ensure you have installed all dependencies:
```bash
pip install -r requirements.txt
```

## Running BDD Tests

### All BDD tests
```bash
behave features/
```

### Specific feature file
```bash
behave features/search.feature
behave features/cart.feature
behave features/sorting.feature
```

### With specific tags
```bash
behave features/ --tags=@smoke
behave features/ --tags=@regression
```

### With Allure reports
```bash
behave features/ --format allure_behave.formatter:AllureFormatter -o allure-results
allure serve allure-results
```

### Headless mode
```bash
# Windows PowerShell
$env:HEADLESS="true"
behave features/

# Windows CMD
set HEADLESS=true
behave features/

# Linux/Mac
export HEADLESS=true
behave features/
```

## Running Unit Tests

### All unit tests
```bash
pytest unit_tests/ -v
```

### Specific test file
```bash
pytest unit_tests/test_home_page.py -v
pytest unit_tests/test_search_page.py -v
```

### With coverage report
```bash
pytest unit_tests/ -v --cov=. --cov-report=html --cov-report=term
```

### Open coverage report
```bash
# Windows
start htmlcov/index.html

# Linux
xdg-open htmlcov/index.html

# Mac
open htmlcov/index.html
```

### Run specific test class
```bash
pytest unit_tests/test_home_page.py::TestHomePage -v
```

### Run specific test method
```bash
pytest unit_tests/test_home_page.py::TestHomePage::test_search_product -v
```

### Run with markers
```bash
pytest unit_tests/ -v -m unit
pytest unit_tests/ -v -m slow
```

## Parallel Execution

### Run tests in parallel (faster)
```bash
# BDD tests - not recommended for BDD due to shared browser state
# Unit tests can run in parallel
pytest unit_tests/ -v -n 4  # 4 parallel workers
```

## Debugging Tests

### Run with print statements visible
```bash
pytest unit_tests/ -v -s
```

### Stop on first failure
```bash
pytest unit_tests/ -v -x
```

### Run last failed tests
```bash
pytest unit_tests/ --lf
```

### Run failed tests first, then others
```bash
pytest unit_tests/ --ff
```

## Test Reports

### Generate HTML report with pytest
```bash
pytest unit_tests/ -v --html=reports/report.html --self-contained-html
```

### Generate JUnit XML report
```bash
pytest unit_tests/ -v --junitxml=reports/junit.xml
```

## Environment Configuration

### Using different browsers
```bash
# Chrome (default)
$env:BROWSER="chrome"
behave features/

# Firefox
$env:BROWSER="firefox"
behave features/

# Edge
$env:BROWSER="edge"
behave features/
```

### Custom base URL
```bash
$env:BASE_URL="https://rozetka.com.ua"
behave features/
```

### Custom timeouts
```bash
$env:IMPLICIT_WAIT="20"
$env:PAGE_LOAD_TIMEOUT="60"
behave features/
```

## Continuous Integration

Tests automatically run on:
- Push to main/develop branches
- Pull requests to main
- Manual workflow dispatch

View results in GitHub Actions tab.

## Tips

1. Always run unit tests before BDD tests
2. Use headless mode for faster execution
3. Check logs/ directory for detailed execution logs
4. Screenshots are saved in screenshots/ on test failures
5. Use `--dry-run` with behave to validate scenarios without execution

```bash
behave features/ --dry-run
```
