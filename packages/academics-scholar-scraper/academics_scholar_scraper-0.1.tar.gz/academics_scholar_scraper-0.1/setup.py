from setuptools import setup, find_packages

setup(
    name='academics_scholar_scraper',
    version='0.1',
    description='A Python package for scraping scholarly articles',
    author='Nathan Laundry',
    author_email='nathan.laundry@gmail.com',
    url='https://github.com/TheAcademicsFieldGuideToWritingCode/ScholarScraper',
    packages=find_packages(),
    install_requires=[
        'argparse',
        'requests',
        'tqdm',
        'openai'
    ],
    entry_points={
        'console_scripts': [
            'academics_scholar_scraper = academics_scholar_scraper:main'
        ]
    },
)
