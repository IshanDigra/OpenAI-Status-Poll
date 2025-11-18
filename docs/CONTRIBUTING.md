# Contributing to OpenAI Status Monitor

Thank you for considering contributing to this project!

## How to Contribute

### Reporting Issues

1. Check existing issues first
2. Use the issue template
3. Include:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details
   - Logs (if applicable)

### Suggesting Features

1. Open an issue with `[Feature]` prefix
2. Describe the use case
3. Explain the benefits
4. Consider implementation approach

### Code Contributions

#### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/IshanDigra/OpenAI-Status-Poll.git
cd OpenAI-Status-Poll

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black pylint mypy
```

#### Development Workflow

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes**
   - Follow PEP 8 style guide
   - Add type hints
   - Write docstrings
   - Include tests

3. **Test locally**
   ```bash
   # Run with test configuration
   export NOTIFIERS=console
   export STATE_BACKEND=file
   python -m src.openai_status_monitor --run-once
   ```

4. **Format code**
   ```bash
   black src/
   ```

5. **Lint code**
   ```bash
   pylint src/openai_status_monitor/
   ```

6. **Commit changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

7. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

#### Commit Message Convention

Follow conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting)
- `refactor:` Code refactoring
- `test:` Test additions or changes
- `chore:` Maintenance tasks

Examples:
```
feat: add Discord notifier support
fix: handle connection timeout gracefully
docs: update setup instructions for Windows
refactor: extract feed parsing logic
```

### Adding New Notifiers

1. Create new file: `src/openai_status_monitor/notifiers/your_notifier.py`
2. Inherit from `BaseNotifier`
3. Implement `notify(incident)` method
4. Update `__main__.py` to instantiate
5. Document in README

Example:
```python
from .base_notifier import BaseNotifier
import logging

logger = logging.getLogger(__name__)

class MyNotifier(BaseNotifier):
    def __init__(self, api_key):
        self.api_key = api_key
    
    def notify(self, incident):
        # Your implementation
        logger.info(f"Notifying: {incident['title']}")
```

### Adding New State Backends

1. Create new file: `src/openai_status_monitor/state_managers/your_backend.py`
2. Inherit from `BaseStateManager`
3. Implement `load_state()` and `save_state(state)` methods
4. Update `__main__.py` to support new backend
5. Document configuration

### Code Style Guidelines

- Follow PEP 8
- Maximum line length: 100 characters
- Use type hints for function parameters and returns
- Write docstrings for all public functions/classes
- Use meaningful variable names
- Add comments for complex logic

### Testing

- Test your changes locally before submitting
- Include test cases for new features
- Verify existing functionality isn't broken
- Test with different configurations

### Documentation

- Update README.md if adding features
- Document new configuration options
- Add examples for new functionality
- Update ARCHITECTURE.md if changing design

## Pull Request Process

1. Ensure your code follows style guidelines
2. Update documentation
3. Test thoroughly
4. Create PR with clear description
5. Link related issues
6. Wait for review
7. Address feedback

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Provide constructive feedback
- Focus on the code, not the person
- Maintain professionalism

## Questions?

Open an issue with the `question` label or reach out to the maintainers.

Thank you for contributing! 🎉
