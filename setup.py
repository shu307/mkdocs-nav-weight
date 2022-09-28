from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='mkdocs-nav-weight',
    version='0.0.5',
    author='shu307',
    author_email="shu307@qq.com",
    description='A simple mkdocs plugin, enable to sort nav by setting "weight" in markdown metadata',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shu307/mkdocs-nav-weight",
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'mkdocs>=1'
    ],
    include_package_data=True,
    entry_points={
        'mkdocs.plugins': [
            'mkdocs-nav-weight = mkdocs_nav_weight:MkDocsNavWeight'
        ]
    },
)
