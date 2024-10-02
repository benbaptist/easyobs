from setuptools import setup, find_packages

setup(
    name='easyobs',
    version='0.1.0',
    author='Ben Baptist',  # Replace with your name
    author_email='sawham6@gmail.com',  # Replace with your email
    description='easyobs adds a layer of pythonic abstraction over the OBS remote protocol',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/benbaptist/easyobs',  # Replace with your GitHub URL
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)