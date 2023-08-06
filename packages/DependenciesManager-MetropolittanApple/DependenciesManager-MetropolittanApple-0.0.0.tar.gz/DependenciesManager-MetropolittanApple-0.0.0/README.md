# DEPENDENCIES MANAGER
#### Created by Pau Cava 

Dependencies Manager is a python library that will help yours install it's dependencies on it's guest user.

---

## How to use the library

Please note that this library uses the module colorama to work, you should have it installed in your computer.

- First step: import the library to your project. 
```python
import dependencies_manager
```
- Second step: create a data list with all your dependencies:

```python
data = ['library', 'library2']
```
- Third step: inizialice the module by putting:
```python
dependencies_manager._init(data, 'PRODUCT NAME')
```

### And you're good to go!