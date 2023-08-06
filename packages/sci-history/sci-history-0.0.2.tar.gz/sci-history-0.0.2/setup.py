import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='sci-history',
    version='0.0.2',
    author='Siddhu Pendyala',
    author_email='elcientifico.pendyala@hotmail.com',
    description='python package for scientific historical information',
    long_description = long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/PyndyalaCoder/history',
    project_urls = {
        "Bug Tracker": "https://github.com/PyndyalaCoder/history/issues"
    },
    license='MIT',
    packages=['sci-history'],
    install_requires=['requests'],
)
