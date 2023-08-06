from setuptools import setup, find_packages

with open("readme.md", "r",encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='chat-mistress',
    description='chat-mistress: 基于GPT3.5的女王聊天室',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.7.4',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'chatmis=chatmistress.chatmistress:main'
        ]
    },
    package_data={
        '': ['templates/*', 'roles/*']
    },
    include_package_data=True,
    install_requires=[
        "langchain>=0.0.123",
        "tiktoken>=0.3.2",
        "openai",
        "python-dotenv",
        "prompt_toolkit",
        "guardrails-ai",
        "xmltodict",
        "gradio",
    ],
)
