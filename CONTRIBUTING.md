# Contributing to Cryptocurrency Forecast

Thank you for considering contributing to this project. This document outlines the process and guidelines for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## How to Contribute

### Reporting Bugs

Before creating a bug report, please check the existing issues to avoid duplicates.

When creating a bug report, include:
- A clear and descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Screenshots if applicable
- Environment details (OS, browser, versions)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:
- A clear and descriptive title
- Detailed description of the proposed functionality
- Explanation of why this enhancement would be useful
- Possible implementation approach

### Pull Requests

1. Fork the repository
2. Create a new branch from `main`
3. Make your changes
4. Write or update tests as needed
5. Update documentation if required
6. Ensure all tests pass
7. Commit your changes with clear commit messages
8. Push to your fork
9. Submit a pull request

## Development Setup

### Backend Development

1. Set up Python virtual environment:
```bash
cd server
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
cp .env.example .env
```

3. Run the development server:
```bash
python app.py
```

### Frontend Development

1. Install dependencies:
```bash
cd client
npm install
```

2. Configure environment:
```bash
cp .env.example .env
```

3. Start development server:
```bash
npm start
```

## Coding Standards

### Python (Backend)

- Follow PEP 8 style guide
- Use meaningful variable and function names
- Write docstrings for functions and classes
- Keep functions small and focused
- Handle errors gracefully
- Log important events
- Write unit tests for new functionality

Example:
```python
def calculate_prediction(data, period):
    """
    Calculate price predictions based on historical data.

    Args:
        data: Historical price data
        period: Time period for prediction

    Returns:
        List of predicted prices

    Raises:
        ValueError: If data is insufficient
    """
    try:
        # Implementation
        pass
    except Exception as e:
        logger.error(f"Error calculating prediction: {e}")
        raise
```

### JavaScript/TypeScript (Frontend)

- Follow the existing code style
- Use TypeScript types properly
- Write meaningful component and function names
- Keep components small and reusable
- Handle errors in async operations
- Write comments for complex logic

Example:
```typescript
interface PredictionData {
    coin: string;
    period: string;
    predictions: Array<[string, number]>;
}

const fetchPredictions = async (coin: string, period: string): Promise<PredictionData> => {
    try {
        const response = await axiosServices.post('/api/prediction', { coin, period });
        return response.data;
    } catch (error) {
        console.error('Failed to fetch predictions:', error);
        throw error;
    }
};
```

## Commit Message Guidelines

Use clear and descriptive commit messages:

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters
- Reference issues and pull requests after the first line

Examples:
```
Add user authentication with JWT tokens

Implement JWT-based authentication system with login and registration
endpoints. Includes password hashing with bcrypt and token validation.

Fixes #123
```

## Testing

### Backend Tests

Run tests with pytest:
```bash
cd server
pytest
```

### Frontend Tests

Run tests with Jest:
```bash
cd client
npm test
```

## Documentation

- Update README.md if you change functionality
- Add comments for complex logic
- Update API documentation for new endpoints
- Include examples in documentation

## Security

- Never commit sensitive data (API keys, passwords, etc.)
- Use environment variables for configuration
- Follow security best practices
- Report security vulnerabilities privately

## Questions?

Feel free to create an issue for any questions about contributing.
