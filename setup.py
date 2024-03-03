from setuptools import setup, find_packages

setup(
    name='YiraBot',
    version='1.0.9.1',
    packages=find_packages(),
    install_requires=open('requirements.txt').readlines(),
    author='Owen Orcan',
    author_email='owenorcan@gmail.com',
    url='https://github.com/OwenOrcan/Yirabot-Crawler',
    license='MIT License',
    description="YiraBot: Simplifying Web Scraping for All. A user-friendly tool for developers and enthusiasts, offering command-line ease and Python integration. Ideal for research, SEO, and data collection.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',

    entry_points={
        'console_scripts': [
            'yirabot=yirabot.yirabot:main',
        ],
    },
)
