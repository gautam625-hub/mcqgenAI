from setuptools import find_packages,setup

setup(
    name='mcqgenerator',
    version='0.0.1',
    author='gautam sahota',
    author_email='gautamsahota625@gmail.com',
    install_requires=['openai','langchain','streamlit','python-dotenv','PyPDF2','langchain-community','tiktoken'],
    packages=find_packages()
)