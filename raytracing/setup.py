import setuptools

setuptools.setup(
    name="raytracing",
    version="1.0.0",
    url="https://github.com/DCC-Lab/RayTracing",
    author="Daniel Cote",
    author_email="dccote@cervo.ulaval.ca",
    description="Simple optical ray tracing library \
    to validate the design of an optical system\
    (lenses positions and sizes, focal lengths).",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=['abcd', 'objectives', 'axicon'],
    install_requires=[],
    license='MIT',
    keywords='optics lenses ray matrices aperture field stop',
    py_modules=['abcd', 'objectives', 'axicon'],
    install_requires=['matplotlib'],
    python_requires='>=3',
    classifiers=[
        'Development Status :: 4 - Beta',
        # Indicate who your project is intended for
        'Intended Audience :: Scientists',
        'Topic :: Optics :: Design Tools',

        # Pick your license as you wish (should match "license" above)
         'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
)
