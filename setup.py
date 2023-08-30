from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='emonic-admin',
    version='1.0.1',
    description='A battery startup for Emonic web framework',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Pawan kumar',
    author_email='control@vvfin.in',
    url='https://github.com/embracke/emonicadmin',
    packages=find_packages(),
    install_requires=['emonic'],  
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    entry_points={
        'console_scripts': [
            'emonic-admin = emonicadmin.admin:main',
        ],
    },
)
