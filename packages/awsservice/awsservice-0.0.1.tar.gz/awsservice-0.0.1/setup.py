from setuptools import setup, find_packages

setup(
    name='awsservice',
    version='0.0.1',
    description= "A small example package for AWS: S3, EC2, CloudWatch",
    author='Vitalik Kost',
    author_email='vitalii.kostyreva@gmail.com',
    packages=find_packages(),
    install_requires=[
        'boto3',
        'pytz',
        'botocore',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)