# GSP and SQLFlow Documentation

Welcome to the GSP (Generic SQL Parser) documentation. This site provides comprehensive information about GSP's features, capabilities, and usage.

## Documentation Sections

* **[Product Introduction](features/product-introduction.md)** - Overview of GSP and its capabilities
* **[User Tutorials](tutorials/getting-started.md)** - Step-by-step guides to help you get started with GSP
* **[SQL Syntax Support](reference/sql-support/index.md)** - Detailed information about supported SQL syntax for different databases
* **[SQL Parsing Analysis](reference/sql-analysis/index.md)** - Analysis of SQL parsing effects and capabilities
* **[Java API Documentation](reference/javadoc/index.html)** - Complete GSP Java API documentation

## Quick Start

To get started with the GSP documentation locally:

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sqlflow_public.git
cd sqlflow_public/site-docs
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the documentation server:
```bash
mkdocs serve
```

5. Open your browser to http://127.0.0.1:8000/ to view the documentation.

## About GSP

GSP (Generic SQL Parser) is a powerful SQL parsing library that supports multiple database dialects, providing accurate SQL parsing, analysis, and transformation capabilities.