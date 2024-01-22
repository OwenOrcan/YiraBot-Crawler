from setuptools import setup, find_packages

setup(
    name='YiraBot',
    version='1.0.4',
    packages=find_packages(),
    install_requires=open('requirements.txt').readlines(),
    author='Owen Orcan',
    author_email='owenorcan@gmail.com',
    url='https://github.com/OwenOrcan/Yirabot-Crawler',
    license='MIT',
    description='A sophisticated Python-based command-line tool for web crawling',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',

    entry_points={
        'console_scripts': [
            'yirabot=yirabot.yirabot:main',
        ],
    },
)
