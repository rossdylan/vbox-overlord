try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_package



setup(
    name='vboxoverlord',
    version='0.1.0',
    description="Overlord of all things virtualbox",
    long_description="Control multiple vbox instances at once",
    author='Ross Delinger',
    author_email='rossdylan@csh.rit.edu',
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT",
        "Programming Lnaguage :: Python :: 2"
    ],
    install_requires=[
        'paramiko',
        ],
    packages=['vboxoverlord'],
    include_package_data=True,
    zip_safe=False,
    entry_points="""
    [console_scripts]
    vbox_overlord = vboxoverlord:rpel
    """
)
