from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pushingtest_4980",
    version="0.1.2",
    author="Michael Chupilnick",
    author_email="your_email@example.com",
    description="CI/CD test package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your_username/your_package_name",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "requests>=2.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
