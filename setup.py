from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='mkdocs-footermatter',
    version='1.0.0',
    description="A plugin to extract authors, created date and updated date from YAML frontmatter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='mkdocs markdown footer author edited created frontmatter obsidian',
    url='https://github.com/sondregronas/mkdocs-footermatter',
    author='Sondre Grønås',
    author_email='mail@sondregronas.com',
    license='AGPLv3',
    python_requires='>=3.9',
    install_requires=['mkdocs>=1', 'timeago==1.0.15', 'babel>=2.7.0'],
    tests_require=["pytest"],
    packages=find_packages("src"),
    package_dir={"": "src"},
    entry_points={'mkdocs.plugins': [
        'footermatter = mkdocs_footermatter.plugin:FootermatterPlugin']}
)
