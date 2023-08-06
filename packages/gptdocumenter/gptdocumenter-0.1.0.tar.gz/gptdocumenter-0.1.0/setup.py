from setuptools import setup, find_packages

setup(
    name='gptdocumenter',
    version='0.1.0',
    description='Python function documentator using ChatGPT.',
    author='Agustín Céspedes',
    author_email='agustinces17@gmail.com',
    long_description=open("Readme.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Caceager/gpt-documenter",
    entry_points={
            "console_scripts": [
                "gptdocumenter=gpt_documenter.main:app",
            ],
        },
    packages=find_packages(),
    install_requires=[
        'langchain~=0.0.117',
        'openai',
        'typer~=0.7.0',
        'pydantic~=1.10.6',
        'tiktoken~=0.3.2'
    ],
)
