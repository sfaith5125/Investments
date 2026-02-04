from setuptools import setup, find_packages

setup(
    name="tech-investment-crawler",
    version="0.1.0",
    description="Web crawler for tech investment news and trends",
    author="Your Name",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.2",
        "feedparser>=6.0.10",
        "python-dateutil>=2.8.2",
        "aiohttp>=3.9.1",
        "sqlalchemy>=2.0.23",
        "python-dotenv>=1.0.0",
    ],
)
