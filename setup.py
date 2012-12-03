from setuptools import setup, find_packages

setup(name='django-competition',
      version='1.0',
      url='http://github.com/michaelwisely/django-competition',
      license='BSD',
      description='A reusable Django app for hosting various competitions',
      author='Michael Wisely',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      install_requires=['setuptools',
                        'django>=1.4',
                        'PyYAML',
                        ],
      )
