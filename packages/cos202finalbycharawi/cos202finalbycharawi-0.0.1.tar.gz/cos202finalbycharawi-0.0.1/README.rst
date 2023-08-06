cos202finalbycharawi
====================

cos202finalbycharawi is a Python library for dealing with points and
vectors.

Installation
------------

Use the package manager `pip <https://pip.pypa.io/en/stable/>`__ to
install cos202finalbycharawi.

.. code:: bash

   pip install cos202finalbycharawi

Usage
-----

.. code:: python

   from cos202finalbycharawi import Vector

   v1 = Vector(1,2)
     v2 = Vector(3,4)
     print(v1)
     print(v2)
     v1.euclideandistance(v2)
     print(v1.lenght())
     print(v1.unit())
     print(v1.dotproduct(v2))
     #print(v1.crossproduct(v2))
     print(v1+v2)
     print(v1-v2)
     print(v1*v2)
     print(v1/v2)

Contributing
------------

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

Author
------

Charawi Detphumi

License
-------

`MIT <https://choosealicense.com/licenses/mit/>`__
