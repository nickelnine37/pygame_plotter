from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='pygame_plotter',
    version='0.0.0',
    author='Edward Antonian',
    author_email='edward.antonian1@gmail.com',
    license='MIT',
    packages=['PG_plotter'],
    description='A plotting program based on pygame',
    long_description='my package long description',
    keywords='chemistry machine learning cheminformatics',
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.5.5',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Pharmacokinetic',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=requirements,
    zip_safe=False
)