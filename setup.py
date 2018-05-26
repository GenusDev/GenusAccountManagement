import setuptools

setuptools.setup(
    name="GenusAccountManagement",
    version="0.0.1",
    author="Matt Steele",
    author_email="msteele@genusdev.com",
    description="account management scripts for Genus",
    long_description= "",
    entry_points={
        'console_scripts' : [
            'mycommand = mymodule.script:main',
        ]
    },
    install_requires=[
        'requests',
    ]
    long_description_content_type="text/markdown",
    url="https://github.com/matsteele/genusaccountmanagement",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Mac OS",
    ),
)

print(setuptools.find_packages())
