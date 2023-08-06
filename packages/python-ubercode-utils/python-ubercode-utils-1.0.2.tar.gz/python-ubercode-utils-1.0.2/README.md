# python-ubercode-utils
Extracting common python utilities re-used between all projects.  The intent is to have minimal dependencies
so the library can be used by django settings without circular references.  I also have color logging class for
jupyter notebooks.  I will have a couple of libraries that will extend this functionality.  Scan the test cases in the 
tests folder for common use cases.

python-utils-core:
- basic conversion helper utilities
- color logging without dependencies
- manipulating urls and their parameters
- helper classes to make working with xml and json data easier
- minimal helper classes to convert database cursor results to dictionaries or tuples
