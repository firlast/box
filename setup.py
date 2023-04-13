from setuptools import setup

from box.__init__ import __version__

setup(
    author='Firlast',
    author_email='firlastinc@gmail.com',
    name='box',
    description='Simple and fast file versioning with Box',
    version=__version__,
    packages=['box'],
    url='https://github.com/firlast/box',
    python_requires='>=3.7',
    install_requires=['argeasy==3.0.0'],
    entry_points={
        'console_scripts': [
            'box = box.__main__:main'
        ]
    },
    keywords=['version', 'control', 'versioning', 'file'],
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
