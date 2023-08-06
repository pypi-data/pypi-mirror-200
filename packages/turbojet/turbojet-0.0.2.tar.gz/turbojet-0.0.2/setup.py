from setuptools import setup

# python setup.py sdist
# twine upload dist/*

setup(
    name='turbojet',
    version='0.0.2',
    description='Biblioteka do liczenia silnikow odrzutowych',
    url='https://github.com/JakUrb04/turbojet.git',
    author='Jakub Urbaniak',
    author_email='urbaniak627@gmail.com',
    license='None license',
    packages=['turbojet'],
    install_requires=[
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
