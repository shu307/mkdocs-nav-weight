from setuptools import setup, find_packages



setup(
    name='mkdocs-nav-weight',
    version='0.0.1',
    author='shu307',
    description='A mkdocs plugin, enable to sort nav by set a "weight" in markdown metadata',
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
