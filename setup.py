from setuptools import setup, find_packages

setup(name="django-klaus",
      version="1.0",
      url='http://github.com/michaelwisely/django-klaus',
      #    license='BSD',
      description="A Django port of Klaus: https://github.com/jonashaag/klaus",
      author='Michael Wisely',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      install_requires=['setuptools',
                        'django>=1.4',
                        'PyYAML',
                        'pygments',
                        'dulwich>=0.8.6',
                        'httpauth'
                        ],
      )
