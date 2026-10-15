# AGENTS.md - Bitcoin Regression Analysis Project

This document provides guidance for AI coding agents working on the Bitcoin price analysis project. It covers build/test/lint commands, code style guidelines, and project conventions.

## Build, Test, and Lint Commands

### Environment Setup
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install dependencies (from README.md)
pip install pandas matplotlib scikit-learn
```

### Running Scripts
```bash
# Run individual analysis scripts (paths resolve from the repo root,
# so these work from any working directory)
python scripts/power-law-trend.py      # Generate power-law trend chart
python scripts/halving-cycle-chart.py  # Generate halving cycle chart

# Run all scripts
python scripts/power-law-trend.py && python scripts/halving-cycle-chart.py
```

### Testing
The project currently has no formal testing framework. Manual testing involves:
- Running scripts and verifying PNG outputs are generated
- Checking console output for expected predictions/messages
- Verifying charts display correctly (manual inspection)

### Linting and Code Quality
No linting tools are currently configured. Recommended setup:
```bash
# Install recommended linting tools
pip install flake8 black isort mypy

# Run linting
flake8 *.py                    # Check style issues
black --check --diff *.py      # Check formatting
isort --check-only --diff *.py # Check import sorting
mypy *.py                      # Type checking (after adding type hints)
```

## Code Style Guidelines

### Language and Environment
- **Python Version**: 3.12.3 (use features available in 3.12+)
- **File Encoding**: UTF-8
- **Line Endings**: Unix (LF)
- **Virtual Environment**: Always use `.venv` (gitignored)

### Import Organization
```python
# Standard library imports (alphabetical)
import datetime
import os
from pathlib import Path

# Third-party imports (alphabetical)
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# Local imports (if any, alphabetical)
# from .local_module import something
```

### Naming Conventions
- **Variables**: `snake_case` (e.g., `reference_date`, `future_days`)
- **Functions**: `snake_case` (e.g., `calculate_trend()`, `plot_chart()`)
- **Classes**: `PascalCase` (if any)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `REFERENCE_YEAR = 2009`)
- **Files**: `kebab-case.py` (e.g., `power-law-trend.py`)

### Code Structure
- **Functions**: Break complex operations into functions with single responsibilities
- **Constants**: Extract magic numbers and repeated strings to constants at top of file
- **Configuration**: Consider moving hardcoded values to config variables
- **Error Handling**: Add try/catch for file operations and data processing
- **Logging**: Use `print()` sparingly; consider logging module for debugging

### Formatting and Style
- **Line Length**: Maximum 88 characters (Black default)
- **Indentation**: 4 spaces (never tabs)
- **Blank Lines**: 2 between top-level functions/classes, 1 between methods
- **Trailing Commas**: Include in multi-line structures
- **Quotes**: Use double quotes for strings, single for characters
- **Comments**: Write docstrings for functions, inline comments for complex logic

### Data Handling
- **CSV Reading**: Use `pd.read_csv()` with appropriate dtypes and date parsing
- **Data Validation**: Check for missing/null values before processing
- **Date Handling**: Use pandas datetime operations consistently
- **Numeric Operations**: Use numpy for mathematical computations
- **Data Filtering**: Document filtering logic and assumptions

### Plotting and Visualization
- **Figure Size**: Use consistent sizing (e.g., `figsize=(14, 8)`)
- **Colors**: Use semantic color schemes (blue for data, red for trends)
- **Labels**: Include units in axis labels, comprehensive titles
- **Saving**: Use `dpi=300, bbox_inches='tight'` for high-quality output
- **File Names**: Follow existing pattern: `charts/{chart_type}.png`

### Type Hints (Future Enhancement)
When adding type hints:
```python
from typing import Optional, List, Tuple
import pandas as pd
import numpy as np

def process_data(df: pd.DataFrame, threshold: float = 1.0) -> pd.DataFrame:
    # Function implementation
    pass
```

### Error Handling Patterns
```python
try:
    df = pd.read_csv(PRICES_CSV, parse_dates=['date'])
except FileNotFoundError as err:
    raise FileNotFoundError(f"price data not found: {PRICES_CSV}") from err
except pd.errors.EmptyDataError as err:
    raise ValueError(f"price data is empty or invalid: {PRICES_CSV}") from err
```

### Documentation
- **README.md**: Update with new features and usage instructions
- **Docstrings**: Add to all public functions
- **Comments**: Explain complex algorithms and business logic
- **Commit Messages**: Use conventional commits (feat:, fix:, docs:, etc.)

### Project Structure
```
bitcoin-price-analysis/
├── README.md                        # Project documentation
├── AGENTS.md                        # This file - agent guidelines
├── SECURITY.md                      # Security policy
├── requirements.txt                 # Dependencies (create if needed)
├── .gitignore                       # Git ignore rules
├── .github/                         # GitHub config (RESERVED - never rename)
│   ├── dependabot.yml
│   └── workflows/renovate.yml
├── data/                            # Input data
│   └── bitcoin-monthly-prices.csv
├── scripts/                         # Chart-generating scripts
│   ├── power-law-trend.py
│   └── halving-cycle-chart.py
├── charts/                          # Generated PNG output
│   ├── power-law-trend.png
│   └── halving-cycle-chart.png
└── .venv/                           # Virtual environment (gitignored)
```

### Common Issues to Watch For
- **File Paths**: Scripts live in `scripts/` but read `data/` and write `charts/`.
  Resolve paths from `Path(__file__).resolve().parent.parent`, never from the
  current working directory, so scripts run correctly from anywhere.
- **Date Formats**: Ensure consistent date parsing and formatting
- **Memory Usage**: Be mindful with large datasets (though current data is small)
- **Dependencies**: Pin versions in requirements.txt for reproducibility
- **Platform Compatibility**: Test on multiple platforms if deploying

### Testing Recommendations
When implementing tests:
- Use `pytest` for unit tests
- Test data loading, processing, and output generation
- Mock file operations for isolated testing
- Test edge cases (empty data, invalid dates, etc.)

### Performance Considerations
- Current dataset is small (< 200 rows), so performance isn't critical
- Use vectorized pandas/numpy operations instead of loops
- Cache expensive computations if scripts become more complex
- Profile with `cProfile` if performance issues arise

### Security Notes
- No sensitive data handling in this project
- Validate CSV input to prevent injection-like issues
- Use safe file operations (no arbitrary file writes)

### Future Enhancements
- Add command-line arguments for configuration
- Create a main module with subcommands
- Implement proper logging instead of print statements
- Add unit tests and CI/CD pipeline
- Containerize with Docker for reproducible environment