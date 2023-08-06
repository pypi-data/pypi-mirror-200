from setuptools import setup, find_packages


setup(
    name='psychoverse',
    version='1.0',
    license='MIT',
    author="KotlinTitus",
    author_email='no@no.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://replit.com/@kotlintitus/Psychoversum',
    keywords='Psychoversum',
    install_requires=[
          'requests',
      ],

)