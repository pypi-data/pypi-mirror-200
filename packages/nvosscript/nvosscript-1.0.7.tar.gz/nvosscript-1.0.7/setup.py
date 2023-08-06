from setuptools import setup, find_namespace_packages

setup(
    name='nvosscript',
    version='1.0.7',
    description='nvos toolchain script',
    packages=find_namespace_packages(),
    author = 'andre.zhao',
    author_email = 'andre.zhao@nio.com',
    keywords='pack',
    readme = "README.md",
    install_requires=[
        'requests',
        'python-daemon',
        'boto3',
        'ldap3',
        'daemon',
        "tqdm"
        # Any other dependencies
    ],
    license="MIT",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'ndtc=nvos.main:main',
            # Any other console scripts
        ]
    }
)