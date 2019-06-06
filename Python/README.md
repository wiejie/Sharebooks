# Python scripting programing language  #




## Python useful source link ##

*[Python 3.7.3 documentation](https://docs.python.org/3/)*

***

## Python packaging structure review ##
1. Packages are modules that contain other modules.
2. Packages are generally implemented as directories containing a special __init__.py file.
3. The __init__.py file is executed when the package is imported.
4. Packages can contain sub packages which themselves are implemented with __init__.py files in directories.
5. The module objects for packages have a __path__ attribute.

~~~
my_package/
  |--__init__.py
  |--a.py
  |--nested/
     |-- __init__.py
     |-- b.py
     |-- c.py

from ..a import A
from .b import B


two dot = parent directory
one dot = same directory
~~~

***

## Recommended project structure example ##
~~~

project_name
|__ __main__.py
|__  project_name
|  |__ __init__.py
|  |__ more_source.py
|  |__ subpackage1
|  |  |__ __init__.py
|  |
|  |__ test
|     |__ __init__.py
|     |__ test_code.py
|__ setup.py

~~~

