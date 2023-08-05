from setuptools import setup, find_packages

with open('README.md', 'rt', encoding='UTF-8') as fh:
    long_description = fh.read()

setup(
    name='logger_via',
    version='1.0.2',
    packages=find_packages(),
    install_requires=[],
    description="Logging decorators (file or email)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.6'
)
