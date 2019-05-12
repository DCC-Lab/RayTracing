import setuptools

""" 
To document:
===========
pydoc -w raytracing.ray
pydoc -w raytracing.gaussianbeam
pydoc -w raytracing.matrix
pydoc -w raytracing.matrixgroup
pydoc -w raytracing.imagingpath
pydoc -w raytracing.laserpath

pydoc -w raytracing.specialtylenses
pydoc -w raytracing.materials
pydoc -w raytracing.thorlabs
pydoc -w raytracing.eo
pydoc -w raytracing.olympus

To distribute:
=============
rm dist/*; python setup.py sdist bdist_wheel; python -m twine upload dist/* 

"""

 

setuptools.setup(
    name="raytracing",
    version="1.1.8",
    url="https://github.com/DCC-Lab/RayTracing",
    author="Daniel Cote",
    author_email="dccote@cervo.ulaval.ca",
    description="Simple optical ray tracing library \
    to validate the design of an optical system\
    (lenses positions and sizes, focal lengths).",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    keywords='optics lenses ray matrices aperture field stop',
    packages=setuptools.find_packages(),
    install_requires=['matplotlib'],
    python_requires='>=3',
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.png'],
        "doc": ['*.html']
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Education',

        # Pick your license as you wish (should match "license" above)
         'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',

        'Operating System :: OS Independent'
    ],
)
