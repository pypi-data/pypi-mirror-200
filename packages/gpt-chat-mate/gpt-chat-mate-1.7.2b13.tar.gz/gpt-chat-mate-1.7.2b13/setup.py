from setuptools import find_packages, setup

with open("README.md") as f:
    ld = f.read()

setup(
    name="gpt-chat-mate",
    version="1.7.2b13",
    description="A cli app for communicating with chatGPT",
    license="GPLv3",
    url="https://gitlab.com/fizzizist/gpt-chat-mate",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "gpt-chat-mate=gpt_chat_mate.main:main",
        ],
    },
    install_requires=[
        "pygments",
        "openai",
        "pyfiglet",
        "func-timeout",
        "tiktoken",
    ],
    author="Fizzizist",
    author_email="gpt-chat-mate@fizzizist.33mail.com",
    long_description=ld,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
