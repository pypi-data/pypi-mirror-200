from setuptools import setup, find_packages

setup(
    name='fnbot',
    version='1.2.6',
    description="yoshino bot",
    # long_description=open('README.md').read(),
    include_package_data=True,
    author='mrhblfx',
    author_email='mrhblfx@gmail.com',
    license='MIT License',
    url='https://github.com/mrhblfx/fnbot',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.8',
    install_requires=['requests','toml'],
)


