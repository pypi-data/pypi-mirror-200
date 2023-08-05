import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="youtuber",
    version="0.1.3",
    author="parkminwoo",
    author_email="parkminwoo1991@gmail.com",
    description="Support tools including crawler, video editing, YouTube API, etc.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DSDanielPark/youtuber",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=[
        "selenium",
        "google-api-python-client",
        "pandas"
    ])