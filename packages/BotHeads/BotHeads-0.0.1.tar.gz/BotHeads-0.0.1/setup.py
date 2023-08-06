from setuptools import setup, find_packages
import codecs
import os



VERSION = '0.0.1'
DESCRIPTION = 'Chat Bots on the Go using openAI API with UI'


# Setting up
setup(
    name="BotHeads",
    version=VERSION,
    author="Abicii",
    author_email="<abhijeettt.9876@gmail.com>",
    description=DESCRIPTION,
    
    packages=find_packages(),
    
    keywords=['python', 'chatbots', 'openai'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
