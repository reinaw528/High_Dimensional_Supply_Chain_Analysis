# Profiling Module Design V1

## Purpose

The profiling module is responsible for generating a standardized summary of dataset structure and data quality.

It does not modify the original dataset.

The profiling result provides reusable metadata for downstream modules such as:

- Data Cleaning
- Feature Engineering
- Reporting
- Business Analysis

## Business Background

When analysts receive a new dataset, they usually spend the first few minutes understanding the data before performing any cleaning or analysis.

Typical questions include:

- How many rows and columns are there?
- Are there missing values?
- Are there duplicate records?
- What are the data types?
- Which columns are numeric?
- Which columns are categorical?

Instead of repeating these checks in every notebook, this module standardizes the profiling process.

## Responsibility

The module is responsible for:

- Inspecting the dataset
- Organizing profiling results
- Returning a reusable profile object

## Public API

generate_profile(df)

- Input
pandas DataFrame

- Output
Profile Dictionary

## Design Decisions

### Why return a dictionary?

Different profiling results naturally have different data types.

For example:

- shape -> tuple
- missing_values -> pandas Series
- describe -> pandas DataFrame

Instead of forcing all results into a single format, the module organizes them into a structured dictionary.

### Why not print results?

Printing is only useful for humans.

Returning structured data allows downstream modules to reuse profiling results.

For example:

- Cleaning
- Reporting
- AI Analysis