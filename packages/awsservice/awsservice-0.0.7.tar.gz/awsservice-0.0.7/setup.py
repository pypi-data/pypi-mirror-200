from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='awsservice',
    version='0.0.7',
    description="A small example package for AWS: S3, EC2, CloudWatch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Vitalik Kost',
    author_email='vitalii.kostyreva@gmail.com',
    packages=find_packages(),
    url='https://github.com/Vitalikys/AWS_s3_app',
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
