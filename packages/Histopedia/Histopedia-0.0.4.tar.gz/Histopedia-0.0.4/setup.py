import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='Histopedia',
    version='0.0.4',
    author='Siddhu Pendyala',
    author_email='elcientifico.pendyala@hotmail.com',
    description='python package for scientific historical information',
    long_description = long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/PyndyalaCoder/Histopedia',
    project_urls = {
        "Bug Tracker": "https://github.com/PyndyalaCoder/Histopedia/issues"
    },
    license='MIT',
    packages=['Histopedia'],
    install_requires=['requests'],
)
