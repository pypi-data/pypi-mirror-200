from setuptools import find_packages, setup

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="crawler-rocket",  # 应用名
    packages=find_packages(),
    version="0.1.0",  # 版本号
    description="Help you to build web crawlers easily and quickly",
    url="https://github.com/taoohong/crawler-rocket",
    author="TaoHong",
    license="MIT",
    install_requires=[
        "requests>=2.28.1",
        "pandas>=1.5.3",
        "retrying>=1.3.4",
        "selenium>=4.3.0",
        "APScheduler>=3.9.1",
        "fake-useragent>=1.1.3",
    ],  # 依赖列表
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # test
    setup_requires=["pytest-runner"],
    tests_require=["pytest==6.2.4"],
    test_suite="tests",
)
