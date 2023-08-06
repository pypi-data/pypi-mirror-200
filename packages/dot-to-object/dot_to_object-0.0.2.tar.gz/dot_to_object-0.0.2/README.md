# Dot to Object

This module is for converting dot notation strings like 'class.object.object' to actual Python objects. To use this module just initialize the class with your variables, usally locals(), then use the get method to obtain the object.
Note that the get function will not raise an error if property is not found, it will just return ```None```. 


## Installation
```pip install dot_to_object```

## Usage
```python
from dot_to_object import DottoObject

dotto = DottoObject(locals())

my_prop = dotto.get('my_class.my_prop')
```


## TODO
- [ ] Make a setter function.
- [ ] Write unit tests