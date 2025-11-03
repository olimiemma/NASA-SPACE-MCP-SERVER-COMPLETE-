# Contributing to Space & Astronomy MCP Server

First off, thank you for considering contributing to the Space MCP Server! 🚀 This project aims to make space exploration data accessible to AI assistants, and your help can make it even better.

## 🌟 How Can I Contribute?

### Reporting Bugs 🐛

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

**Bug Report Template:**
```markdown
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Call tool '...'
2. With parameters '...'
3. See error

**Expected behavior**
What you expected to happen.

**Actual behavior**
What actually happened.

**Environment:**
 - OS: [e.g., macOS, Windows, Linux]
 - Python version: [e.g., 3.10]
 - MCP client: [e.g., Claude Desktop]

**Additional context**
Add any other context about the problem.
```

### Suggesting Features 💡

Feature suggestions are welcome! Before suggesting a feature:

1. **Check existing feature requests** to avoid duplicates
2. **Provide clear use cases** - explain why this feature would be useful
3. **Consider scope** - does it fit the project's goals?

**Feature Request Template:**
```markdown
**Is your feature request related to a problem?**
A clear description of the problem. Ex. I'm frustrated when [...]

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
Any alternative solutions or features you've considered.

**Additional context**
Add any other context or examples about the feature request.
```

### Contributing Code 💻

#### Getting Started

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub
   git clone https://github.com/YOUR-USERNAME/space-mcp-server.git
   cd space-mcp-server
   ```

2. **Set up development environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

#### Code Style Guidelines

**Python Style:**
- Follow [PEP 8](https://pep8.org/) style guide
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters
- Use meaningful variable and function names

**Type Hints:**
```python
# Always include type hints
def get_mars_photos(rover: str, sol: int) -> List[Dict[str, Any]]:
    pass
```

**Docstrings:**
```python
def tool_function(params: InputModel) -> str:
    """
    Brief description of what the tool does.
    
    Detailed explanation of functionality and use cases.
    
    Args:
        params (InputModel): Description of parameters containing:
            - field1 (type): Description
            - field2 (type): Description
    
    Returns:
        str: Description of return value including format
    
    Example use cases:
        - Use case 1
        - Use case 2
    """
    pass
```

**Async/Await:**
```python
# Use async for all I/O operations
async def make_api_request(url: str) -> Dict[str, Any]:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()
```

**Error Handling:**
```python
# Provide clear, actionable error messages
try:
    result = await api_call()
except httpx.HTTPStatusError as e:
    raise Exception(
        f"API request failed with status {e.response.status_code}. "
        f"Try using different parameters or check your API key."
    ) from e
```

#### Adding New Tools

When adding a new MCP tool:

1. **Create Pydantic input model:**
   ```python
   class NewToolInput(BaseModel):
       model_config = ConfigDict(
           str_strip_whitespace=True,
           validate_assignment=True,
           extra='forbid'
       )
       
       param1: str = Field(
           ...,
           description="Clear description with examples",
           min_length=1,
           max_length=100
       )
   ```

2. **Implement tool with decorator:**
   ```python
   @mcp.tool(
       name="space_new_tool",
       annotations={
           "title": "Human-Readable Title",
           "readOnlyHint": True,
           "destructiveHint": False,
           "idempotentHint": True,
           "openWorldHint": True
       }
   )
   async def new_tool(params: NewToolInput) -> str:
       """Comprehensive docstring..."""
       # Implementation
   ```

3. **Add comprehensive documentation:**
   - Update README.md with new tool
   - Add examples in API Reference section
   - Create evaluation questions

4. **Test thoroughly:**
   - Test with various inputs
   - Test error cases
   - Verify character limits
   - Check both Markdown and JSON formats

#### Testing

**Manual Testing:**
```bash
# Test syntax
python -m py_compile space_mcp.py

# Test with Claude Desktop or MCP Inspector
```

**Adding Tests (Future):**
```python
# tests/test_space_mcp.py
import pytest
from space_mcp import get_apod

async def test_get_apod():
    # Test implementation
    pass
```

#### Commit Messages

Use clear, descriptive commit messages:

```bash
# Good commits
git commit -m "Add Mars weather data tool"
git commit -m "Fix ISS tracking timeout issue"
git commit -m "Update documentation for NEO tracking"

# Bad commits
git commit -m "fix stuff"
git commit -m "update"
git commit -m "changes"
```

**Commit Message Format:**
```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Example:**
```
feat: Add Hubble telescope image search tool

Implements a new tool for searching and retrieving images from the
Hubble Space Telescope archive. Includes support for filtering by
collection, observation date, and target name.

Closes #42
```

#### Pull Request Process

1. **Update documentation**
   - Add/update docstrings
   - Update README.md if needed
   - Add examples

2. **Ensure code quality**
   - No syntax errors
   - Type hints complete
   - Follows style guide

3. **Create pull request**
   - Use descriptive title
   - Reference related issues
   - Explain changes clearly
   - Add screenshots/examples if applicable

4. **Respond to feedback**
   - Address review comments
   - Make requested changes
   - Be open to suggestions

**Pull Request Template:**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring

## Testing
How was this tested?

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No new warnings
- [ ] Tests pass
```

### Improving Documentation 📚

Documentation improvements are always welcome:

- Fix typos or grammatical errors
- Clarify confusing explanations
- Add more examples
- Improve API documentation
- Create tutorials or guides

To edit documentation:
1. Fork and clone the repository
2. Make changes to relevant `.md` files
3. Submit a pull request

## 🎯 Development Priorities

Current priorities for contributions:

### High Priority
- Additional space data sources (Mars weather, Hubble, etc.)
- Unit tests and test coverage
- Performance optimizations
- Better error messages

### Medium Priority
- Additional response format options
- Caching layer for API responses
- Rate limiting improvements
- Configuration options

### Low Priority
- UI/visualization tools
- Alternative transport protocols
- Database integration

## 🤔 Questions?

If you have questions about contributing:

1. Check the [README.md](README.md) for basic information
2. Search existing [Issues](https://github.com/yourusername/space-mcp-server/issues)
3. Ask in [Discussions](https://github.com/yourusername/space-mcp-server/discussions)
4. Contact maintainers

## 🏆 Recognition

Contributors will be recognized in:
- README.md Contributors section
- Release notes
- Project documentation

Thank you for contributing to making space exploration data accessible to AI! 🚀✨

## 📜 Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive behavior includes:**
- Being respectful of differing viewpoints
- Accepting constructive criticism gracefully
- Focusing on what's best for the community
- Showing empathy towards others

**Unacceptable behavior includes:**
- Harassment or discriminatory language
- Trolling or insulting comments
- Publishing others' private information
- Other unprofessional conduct

### Enforcement

Project maintainers are responsible for clarifying standards and may take appropriate action in response to unacceptable behavior.

### Contact

Report issues to [your.email@example.com](mailto:your.email@example.com)

---

*This document is adapted from [Contributor Covenant](https://www.contributor-covenant.org/) and various open source projects.*
