from setuptools import setup, find_packages

setup(
    name='futureasync',
    version='2.0',
    author='futureasync',
    author_email='pymaniaclib@hotmail.com',
    description='Simple python module to perform your web requests simultaneously in an asynchronous and colors toolkit, simple, efficient and powerful way.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/votre_compte/futureasync',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'colorama',
        'httpx',
        'pyautogui',
        'telegram',
        'pycountry',
        'requests',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
