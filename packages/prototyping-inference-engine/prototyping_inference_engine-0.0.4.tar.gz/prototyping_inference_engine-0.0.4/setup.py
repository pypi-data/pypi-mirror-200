from setuptools import setup, find_packages

setup(name='prototyping_inference_engine', version='0.0.4',
      packages=find_packages("prototyping_inference_engine", "prototyping_inference_engine"),
      entry_points={
                  'console_scripts': [
                     'disjunctive-rewriter = prototyping_inference_engine:apps.disjunctive_rewriter.main'
                  ]
               },
      install_requires=[
         'lark'
      ])




