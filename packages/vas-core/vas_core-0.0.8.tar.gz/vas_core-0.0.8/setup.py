from setuptools import setup, find_packages

VERSION = '0.0.8'
DESCRIPTION = 'VAS Orchestra core package'
LONG_DESCRIPTION = 'Package that holds all models and common ' \
                   'functions/classes of VAS Orchestra project'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="vas_core",
    version=VERSION,
    author="Phourxx",
    author_email="<phourxx0001@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    include_package_data=True,
    install_requires=["django", "djangorestframework",
                      "djangorestframework-simplejwt", "drf-yasg",
                      "python-dotenv", "django-safedelete",
                      "django-cors-headers", "redis"],
    # add any
    # additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'vas'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",

    ]
)
