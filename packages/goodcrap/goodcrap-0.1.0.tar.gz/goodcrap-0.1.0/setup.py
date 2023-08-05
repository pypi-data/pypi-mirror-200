from distutils.core import setup
setup(
    name='goodcrap',
    packages=['goodcrap'],
    version='0.1.0',
    license='gpl-3.0',
    description='goodcrap generates controlled random data.',
    author='Sherif Abdulkader Tawfik',
    author_email='sherif.tawfic@gmail.com',
    url='https://github.com/goodcrap/goodcrap',
    keywords=['ai', 'data engineering', 'fake data',
              'data science'],
    install_requires=['scipy', 'numpy', 'pandas', 'matplotlib'],

)
