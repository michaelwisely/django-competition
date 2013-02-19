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
                        'django==1.4.3',
                        'PyYAML==3.10',
                        'factory_boy==1.2.0',
                        'django-guardian==1.0.4',
                        'django-crispy-forms==1.2.3',
                        ],
      )
