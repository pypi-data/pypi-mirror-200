from setuptools import setup, find_packages
 
classifiers=[
"Programming Language :: Python :: 3",
"License :: OSI Approved :: MIT License",
"Operating System :: OS Independent",
]
 
setup(
  name='QtMkEditor',
  version='1.0.0',
  description='Markdown Editor.',
  long_description= open('README.md').read() + '\n\n',
  url='',  
  author='Moussa JAMOR',
  author_email='moussajamorsup@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Markdown, Html, Editor, PyQt5', 
  packages=find_packages(),
  package_data={'QtMkEditor': ['core/view/icons/*.png',
                              'core/view/style/*.qss',
                              'core/view/style/*.css',
                              'core/view/ui/*.ui'
                              ]},
  install_requires=['PyQt5', 'markdown', 'bs4'] 
)