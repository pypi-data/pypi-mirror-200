from setuptools import setup, find_packages

setup(
    name='MouseMover',
    version='0.1.1',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Office/Business',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "PyAutoGUI==0.9.53",
        "click==8.1.3"
    ],
    entry_points={
        'console_scripts': [
            'shakemymouse = mouse:cli',
        ],
    },
)