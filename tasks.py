from invoke import task
from pathlib import Path
from robot.libdoc import libdoc


# Paths
ROOT = Path(__file__).parent
SRC = ROOT / "src" / "FastHTTPMock"
TESTS = ROOT / "tests"
ATESTS = ROOT / "atests"
DOCS = ROOT / "docs"

@task
def clean(ctx):
    """Clean up build artifacts."""
    patterns = [
        "*.pyc",
        "*.pyo",
        "*.pyd",
        "*.so",
        "*.egg",
        "*.egg-info",
        "*.eggs",
        ".coverage",
        "htmlcov",
        ".pytest_cache",
        ".tox",
        ".venv",
        "build",
        "dist",
        "__pycache__",
        "FastHTTPMock-debug.log"
    ]
    
    for pattern in patterns:
        ctx.run(f"find . -type f -name '{pattern}' -delete")
        ctx.run(f"find . -type d -name '{pattern}' -exec rm -rf {{}} +")

@task
def format(ctx):
    """Format code using black and ruff."""
    print("Formatting with black...")
    ctx.run(f"black {SRC} {TESTS}")
    print("Formatting with ruff...")
    ctx.run(f"ruff check --fix {SRC} {TESTS}")

@task
def lint(ctx):
    """Run linting checks."""
    print("Running black check...")
    ctx.run(f"black --check {SRC} {TESTS}")
    print("Running ruff check...")
    ctx.run(f"ruff check {SRC} {TESTS}")

@task
def test_unit(ctx):
    """Run unit tests."""
    ctx.run(f"pytest {TESTS}")

@task
def test_acceptance(ctx):
    """Run acceptance tests."""
    ctx.run(f"robot {ATESTS}")

@task
def test(ctx):
    """Run all tests."""
    test_unit(ctx)
    test_acceptance(ctx)

@task
def docs(ctx):
    """Generate library documentation."""
    DOCS.mkdir(exist_ok=True)
    print("Generating library documentation...")
    # ctx.run(f"python -m robot.libdoc FastHTTPMock {DOCS}/FastHTTPMock.html")
    output = f"{DOCS}/FastHTTPMock.html"
    libdoc("FastHTTPMock", str(output))
    print(f"Documentation generated at {DOCS}/FastHTTPMock.html")

@task
def build(ctx):
    """Build the package."""
    clean(ctx)
    ctx.run("python -m build")

@task
def install(ctx):
    """Install the package in development mode."""
    ctx.run("pip install -e '.[dev]'")

@task
def uninstall(ctx):
    """Uninstall the package."""
    ctx.run("pip uninstall robotframework-fasthttpmock -y")

@task(pre=[clean, lint, test, docs, build])
def release(ctx):
    """Prepare for release."""
    print("Release preparation complete")

@task
def dev_setup(ctx):
    """Set up development environment."""
    install(ctx)
    docs(ctx) 