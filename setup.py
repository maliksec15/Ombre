from setuptools import setup, find_packages

setup(
    name="ombre",
    version="1.0.0",
    description="Autonomous AI Reasoning Data Infrastructure",
    author="Ombre",
    author_email="ombreaiq@gmail.com",
    url="https://github.com/ombreaiq/ombre",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "flask>=2.0.0",
        "numpy>=1.21.0",
        "requests>=2.28.0",
        "python-dotenv>=1.0.0",
        "scipy>=1.9.0",
        "scikit-learn>=1.1.0",
    ],
    entry_points={
        "console_scripts": [
            "ombre=ombre.__main__:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
