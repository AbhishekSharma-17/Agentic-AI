# Agentic AI

A collection of examples and implementations for working with AI agents, primarily using OpenAI's APIs.

## Overview

This repository contains code examples and implementations for building AI agents with various capabilities. It focuses on OpenAI's APIs and demonstrates different approaches to creating intelligent, autonomous agents.

## Repository Structure

```
.
├── Basic_openai/              # Basic OpenAI API usage examples
│   ├── 1-basic.py            # Basic API interaction
│   ├── 2-structured_0utput.py # Working with structured outputs
│   ├── 3-using_tools.py      # Implementing tool usage
│   ├── 4-retrieval.py        # Knowledge retrieval examples
│   └── Kb.json               # Knowledge base data
├── Openai_Agents/            # OpenAI agent implementations
│   ├── basics/               # Basic agent examples
│   │   ├── first.py          # First agent implementation
│   │   ├── function_calls.py # Function calling with agents
│   │   └── Handoffs.py       # Agent handoff examples
│   └── init/                 # Agent initialization
│       └── quickstar.py      # Quick start guide
└── Web Agent/                # Web-based agent implementation
    └── basic.py              # Basic web agent
```

## Installation

This project uses Poetry for dependency management. To install:

1. Make sure you have [Poetry installed](https://python-poetry.org/docs/#installation)
2. Clone this repository
3. Run the following command in the project root:

```bash
poetry install
```

This will install all required dependencies based on the `poetry.lock` file.

## Usage

The repository is organized into different sections, each demonstrating specific aspects of AI agents:

### Basic OpenAI Examples

Navigate to the `Basic_openai` directory to explore fundamental OpenAI API interactions:

```bash
cd Basic_openai
poetry run python 1-basic.py
```

### OpenAI Agents

The `Openai_Agents` directory contains more advanced agent implementations:

```bash
cd Openai_Agents/basics
poetry run python first.py
```

### Web Agent

Explore web-based agent capabilities:

```bash
cd "Web Agent"
poetry run python basic.py
```

## Prerequisites

- Python 3.8+
- OpenAI API key (set as an environment variable)
- Poetry for dependency management

## Environment Setup

Set your OpenAI API key as an environment variable:

```bash
# For Windows
set OPENAI_API_KEY=your-api-key

# For macOS/Linux
export OPENAI_API_KEY=your-api-key
```

## License

[Specify license information here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
