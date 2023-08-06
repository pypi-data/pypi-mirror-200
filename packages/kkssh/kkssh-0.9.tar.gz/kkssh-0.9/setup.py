from setuptools import setup, find_packages

setup(
    name='kkssh',
    version='0.9',
    description='ssh client',
    author='xingkun',
    author_email='xingkunliu@qq.com',
    url='https://github.com/Beim/kkssh',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    keywords='ssh client',
    install_requires=[
        'paramiko',
    ],
    entry_points={
        'console_scripts': [
            'kkssh = kkssh.main:main'
        ]
    },
)
