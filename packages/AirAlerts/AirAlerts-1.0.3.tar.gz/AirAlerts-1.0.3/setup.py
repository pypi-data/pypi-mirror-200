from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='AirAlerts',
    version='1.0.3',
    description='A Python module for monitoring Air Raid Alerts in Ukraine',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Romikan',
    author_email='romikan.code@gmail.com',
    packages=['AirAlerts'],
    install_requires=[
        'requests',
        'pillow'
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)