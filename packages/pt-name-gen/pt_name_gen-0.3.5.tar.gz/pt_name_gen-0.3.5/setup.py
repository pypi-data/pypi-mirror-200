from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='pt_name_gen',
    version='0.3.5',
    description='A name generator in Portuguese, with support to gender classification. Um gerador de nomes em português, com suporte para classificação de gênero.',
    author='Victor Figueredo',
    packages=['pt_name_gen'],
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['unidecode'],
    package_data={
        "pt_name_gen": ["*.csv"]
    },
    entry_points={
        'console_scripts': [
            'pt_name_gen=pt_name_gen.__main__:main'
        ]
    }
)
