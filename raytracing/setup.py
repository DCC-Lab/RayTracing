import setuptools

setuptools.setup(
    name="raytracing",
    version="1.0.0",
    url="https://github.com/DCC-Lab/RayTracing",
    author="Daniel Cote",
    author_email="dccote@cervo.ulaval.ca",
    description="An optical design tool based on ray matrices\
    (i.e. ABCD matrices) to model propagation and trace rays through\
    optical elements, with or without apertures.",
    long_description=open('README.md').read(),
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
)
