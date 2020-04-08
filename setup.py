import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-models-extensions",
    version="0.0.1",
    author="lampofearth",
    author_email="lampofearth@gmail.com",
    description="Models Extensions for Django.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        'Framework :: Django',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
    project_urls={
        'Documentation': 'https://github.com/lampofearth/django-models-extensions/wiki',
        'Source': 'https://github.com/lampofearth/django-models-extensions/',
        'Tracker': 'https://github.com/lampofearth/django-models-extensions/issues/',
    },
    python_requires=">=3.6",
    install_requires=[
       'django>=2.0.0',
    ]
)
