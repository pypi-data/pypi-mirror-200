from setuptools import setup, find_packages

setup(
    name='disclog',
    version='0.0.1',
    description='A logging package that sends logs to Discord webhooks.',
    author='Yoel',
    author_email='yoelz@tlvtech.io',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=['requests'],
)
