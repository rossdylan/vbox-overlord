try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_package



setup(
    name='vboxoverlord',
    version='0.2',
    description="Overlord of all things virtualbox",
    long_description="Control multiple vbox instances at once",
    author='Ross Delinger',
    author_email='rossdylan@csh.rit.edu',
    url="https://github.com/rossdylan/vbox-overlord",
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 2"
    ],
    install_requires=[
        'SuperParamiko',
        ],
    packages=['vboxoverlord'],
    include_package_data=True,
    zip_safe=False,
    entry_points="""
    [console_scripts]
    vbo = vboxoverlord:rpel
    """
)
