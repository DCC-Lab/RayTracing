import setuptools

""" 
To distribute:
=============
rm dist/*; python setup.py sdist bdist_wheel; python -m twine upload dist/* 

"""


setuptools.setup(
    name="raytracing",
    version="1.2.11",
    url="https://github.com/DCC-Lab/RayTracing",
    author="Daniel Cote",
    author_email="dccote@cervo.ulaval.ca",
    description="Simple optical ray tracing library \
    to validate the design of an optical system\
    (lenses positions and sizes, focal lengths,\
    aperture and field stops). Some support for Monte Carlo\
    raytracing to estimate transmission efficiency and powers.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    keywords='optics optical lens ray tracing matrix matrices aperture field stop\
    monte carlo design raytracing',
    packages=setuptools.find_packages(),
    install_requires=['matplotlib', 'numpy'],
    python_requires='>=3.6',
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
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',

        'Operating System :: OS Independent'
    ],
)
