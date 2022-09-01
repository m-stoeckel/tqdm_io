from setuptools import find_packages, setup

setup(
    name='tqdm-io',
    version='0.0.3',
    description='A byte-based IO-wrapper using tqdm.',
    url='https://github.com/m-stoeckel/tqdm_io',
    author='Manuel Stoeckel',
    author_email='manuel.stoeckel@em.uni-frankfurt.de',
    classifiers=[
        # 3 - Alpha, 4 - Beta, 5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3 :: Only',
    ],
    package_dir={'': 'src'},  # Optional
    packages=find_packages(where='src'),  # Required
    python_requires='>=3.8, <4',
    install_requires=['tqdm'],
    extras_require={  # Optional
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    package_data={
    },
)
