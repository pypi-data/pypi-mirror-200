from setuptools import setup, find_packages

# list dependencies from file
with open('requirements.txt') as f:
    content = f.readlines()
requirements = [x.strip() for x in content]

setup(
    name="faciesteller",
    version="1.0.0",
    packages=find_packages(),
    install_requires=requirements,
    author="Xiaohu Jiang",
    author_email="xjiang@slb.com",
    description="This package is created to classify facies using FMI image and depth CSV data, output prediction result with csv format as well as image",
    url="https://github.com/yourusername/mypackage",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)