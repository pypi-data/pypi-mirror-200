from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="mangust228",
    version="0.6.2",
    description="Library for take current proxy from API",
    author="mangust228",
    author_email="bacek.mangust@gmail.com",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mangustik228/proxy_manager',
    install_requires=[
        'requests',
        'pandas',
        'pydantic',
        'loguru',
        'aiohttp',
        'asyncio',
        
    ],
    classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
    ],
    python_requires = '>=3.8'
)