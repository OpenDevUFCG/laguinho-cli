from setuptools import setup


setup(
    name="laguinho",
    version="1.0",
    packages=['laguinho', 'laguinho.commands'],
    include_package_data=True,
    install_requires=[
        "click"
    ],
    entry_points='''
        [console_scripts]
        laguinho=laguinho.cli:cli
    '''
)