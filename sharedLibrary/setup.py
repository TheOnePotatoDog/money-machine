from setuptools import setup, find_packages

setup(
    name="ai-shared-lib",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.95.0",
        "sqlalchemy>=2.0.0",
        "pydantic>=2.0.0",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4",
        "python-multipart>=0.0.5",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="Shared library for AI Projects",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/shared-library",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
