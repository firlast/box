from setuptools import setup

from box.__init__ import __version__

with open('README.md') as file:
    readme = file.read()

setup(
    author='Firlast',
    author_email='firlastinc@gmail.com',
    name='box-vcs',
    description='Fast, easy-to-use file versioning with Box',
    version=__version__,
    packages=['box'],
    url='https://github.com/firlast/box',
    long_description=readme,
    long_description_content_type='text/markdown',
    license='GNU GPLv2',
    python_requires='>=3.7',
    install_requires=['argeasy==3.1.0'],
    entry_points={
        'console_scripts': [
            'box = box.__main__:main'
        ]
    },
    keywords=['version', 'control', 'versioning', 'vcs'],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Version Control'
    ],
)
