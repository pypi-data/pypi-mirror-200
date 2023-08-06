from setuptools import setup


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='uncrawl',
    version='1.0.2',
    description='A lightweight package for webpage scraping and content extraction.',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Tensaye Yuan',
    author_email='yyuan.tech@gmail.com',
    url='https://github.com/tensaye-o/uncrawl',
    license=license,
    package_dir={"uncrawl": "uncrawl"},
    packages=["uncrawl"],
    install_requires=["newspaper3k"]
)
