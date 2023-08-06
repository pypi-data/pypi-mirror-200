from distutils.core import setup
setup(
  name = 'Tclab_Pi',         # How you named your package folder (MyLib)
  packages = ['Tclab_Pi'],   # Chose the same as "name"
  version = '0.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'a tclab python package for pi',   # Give a short description about your library
  author = 'VaderG',                   # Type in your name
  author_email = 'gwd0451@163.com',      # Type in your E-Mail
  keywords = ['Pi', 'Tclab'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'spidev',       # 可以加上版本号，如validators=1.5.1   
          'numpy',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
  ],
)
