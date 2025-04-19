# Installation Guide for Data Engineering Project

## Overview
This document outlines the installation process for setting up the data engineering environment, specifically focusing on Apache Airflow with Kafka streaming capabilities. It includes lessons learned and best practices based on our experience.

## Prerequisites
- Python 3.x
- pip (Python package installer)
- Virtual environment
- Windows OS (specific notes for Windows users included)

## Virtual Environment Setup
1. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
2. Activate the virtual environment:
   - Windows (CMD): `.venv\Scripts\activate`
   - Windows (Git Bash): `source .venv/Scripts/activate`
   - Linux/Mac: `source .venv/bin/activate`

## Installation Process

### Key Learnings and Best Practices

1. **Avoid Problematic Dependencies**
   - The initial installation attempts with full Airflow dependencies faced issues with `google-re2` package on Windows
   - `google-re2` requires C++ build tools and Abseil headers, which are challenging to set up on Windows
   - Solution: Use minimal installation approach with only required providers

2. **Recommended Requirements File Structure**
   ```
   apache-airflow==2.7.2
   apache-airflow-providers-postgres==5.11.3
   psycopg2-binary==2.9.10
   python-dotenv==1.0.0
   kafka-python==2.0.2
   pyspark==3.5.0
   cassandra-driver==3.28.0
   pandas==2.2.3
   ```

3. **Packages to Exclude**
   - `google-re2`: Requires complex C++ setup
   - `python-nvd3`: Optional visualization package
   - `unicodecsv`: Optional package

4. **Installation Steps**
   a. Install Airflow first with minimal dependencies:
      ```bash
      pip install --no-cache-dir apache-airflow==2.7.2
      ```
   
   b. Install providers and other dependencies:
      ```bash
      pip install --no-cache-dir -r requirements.txt
      ```

### Common Issues and Solutions

1. **C++ Build Tools Issues**
   - Problem: Some packages require C++ build tools
   - Solution: Use binary distributions when available (e.g., `psycopg2-binary` instead of `psycopg2`)

2. **Dependency Conflicts**
   - Problem: Complex dependency trees can cause conflicts
   - Solution: Install packages incrementally, starting with core packages

3. **Cache-Related Issues**
   - Problem: Cached packages can cause installation problems
   - Solution: Use `--no-cache-dir` flag with pip

## Docker Setup (Optional)
If using Docker for Airflow:
1. Ensure Docker and Docker Compose are installed
2. Use the official Airflow Docker image
3. Configure environment variables appropriately
4. Initialize the database before starting services

## Verification Steps
After installation:
1. Verify Airflow installation:
   ```bash
   airflow version
   ```
2. Test database connection
3. Verify all required providers are installed:
   ```bash
   airflow providers list
   ```

## Troubleshooting

1. **Installation Fails with Build Errors**
   - Check Python version compatibility
   - Verify virtual environment is activated
   - Try using pre-compiled wheels when available

2. **Import Errors After Installation**
   - Verify all dependencies are installed
   - Check for version conflicts
   - Consider using `pip check` to verify dependencies

## Maintenance

1. **Updating Dependencies**
   - Keep track of security updates
   - Test updates in development environment first
   - Update packages individually to isolate issues

2. **Version Control**
   - Keep requirements.txt in version control
   - Document any special installation steps
   - Maintain changelog for dependency updates

## Contact and Support
For issues and support:
- Create an issue in the project repository
- Document the exact error message
- Include your environment details (OS, Python version, etc.) 