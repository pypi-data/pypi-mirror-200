from setuptools import setup, find_packages

setup(name='pie', version='0.0.2', packages=find_packages(),
      entry_points={
                  'console_scripts': [
                     'disjunctive-rewriter = apps:disjunctive_rewriter.main'
                  ]
               },
      install_requires=[
         'lark'
      ])




