"""
Setup script for TikTok Parser
"""

from setuptools import setup, find_packages

setup(
    name="tiktok_parser",
    version="0.1.0",
    description="A tool for parsing TikTok users by topic and extracting influencer data",
    author="TikTok Parser Team",
    packages=find_packages(),
    install_requires=[
        "playwright>=1.20.0",
        "asyncio>=3.4.3",
    ],
    entry_points={
        "console_scripts": [
            "tiktok-parser=cli:main",
        ],
    },
    python_requires=">=3.7",
)
