from setuptools import find_packages, setup

setup(
    name="motiondev",
    author="ItsWilliboy",
    url="https://github.com/itswilliboy/motiondev",
    version="0.1.0",
    description="An asynchronous API wrapper for the Motion Development bot list API.",
    packages=find_packages(),
    install_requires=["aiohttp"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10" "Programming Language :: Python :: 3.11",
    ],
)
