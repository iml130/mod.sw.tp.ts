# FiwareObjectConverter (FOC)

This is a simple implementation to serialize Python2.7-Objects into a [Fiware-Entity](https://www.fiware.org/wp-content/uploads/2016/12/2_FIWARE-NGSI-Managing-Context-Information-at-large-scale.pdf) and back. The generated JSON-Strings can be POSTed to their API.

There is also the posibillity to ignore the Metadata while parsing back to the (specified) Python-Object.

For more Information about Fiwire-Orion visit the following [website](https://fiware-orion.readthedocs.io/en/master/)

## Fiware Entity
```python
Entity consits of
    - Id
    - Type
    - has n Attributes:
        - Name
        - Type
        - Value
        has n-Metadata:
            - Name
            - Type
            - Value
```

## Usage
Let's create a class which contains a unicode-string in Python via: 
```python
class FooBar(object):
    def __init__(self):
        self.myStr = u'Hi!'
```

### Object 2 FiwareEntity
This class can be simply serialized to Json with:
```python
from objectFiwareConverter import ObjectFiwareConverter

json = ObjectFiwareConverter.obj2Fiware(FooBar(), ind=4)
# indent is set to 4 for readability

```

The `str` `json` contains the following

```json
{
    "myStr": {
        "type": "string",
        "value": "Hi!",
        "metadata": {
            "python": {
                "type": "dataType",
                "value": "unicode"
            }
        }
    },
    "type": "FooBar",
    "id": "FooBarbc86c90d-6cca-41c3-878e-cbb58908056c"
}
```
This is a simple class for demonstration. The Data-Structure can be arbitrary complex.

The `"type"`- and `"id"`-values can be set manually. To do so, just add `self.type = "YOUR_TYPE"` and/or `self.id = "YOUR_ID"` to `FooBar`.

### FiwareEntity 2 Object
A (Representation-) Class is needed to convert it back. Let's set a Class and then parse the JSON-Object into it:

```python 
class MyVeryOwnFooBar(object): 
    def __init__(self):
        self.myStr = u' ' # Set Unicode DataType

mvofb = MyVeryOwnFooBar()
ObjectFiwareConverter.fiware2Obj(json, mvofb) # the json from above
print mvofb.myStr # prints "Hi!"
```
Missing variables which are defined by the JSON-String are ignored if not set in the class. If variables are defined which are not specified in the JSON-String then those variables are not touched.



## Further Information
#### Fiware Entity Information (Type/ID)
```
type = ClassName
id = ClassName + Universally Unique Identifier (UUID)
```
The `id` consist of the Class-Name `+` a random generated `uuid` by [uuid4()](https://docs.python.org/2/library/uuid.html) and the type is simply the Class-Name. Also: All Objects, which are converted back from json will contain an `id` and `type` Attribute. They can be accessed with `getattr`.

#### Ignoring Metadata
To ignore the metadata, do the following:
```python 
mvofb = MyVeryOwnFooBar()
ObjectFiwareConverter.fiware2Obj(json, mvofb, useMetadata=False) # the json from above
```
The conversion between a Python-Object and a JSON-String is not bidirectional by ignoring the `metadata`. 
By ignoring the `metadata` some Python-DataTypes are "converted into a simple type":
```text 
Complex, Tuple --> List
Unicode        --> String
```
---
NOTE:
The above example will throw an `TypeError`, because the class `MyVeryOwnFooBar` awaits an `unicode` but would be overwritten with a string, because the `metadata` is ignored. This behaviour can be turned off with the following: 
```python 
mvofb = MyVeryOwnFooBar()
ObjectFiwareConverter.fiware2Obj(json, mvofb, useMetadata=False, ignoreWrongDataType=True) # the json from above
```
---
It is also possible to give a Data-Type-Object-Structure while converting to json. Simply create a `dict` containing the concrete Data-Type for Data and the additional Information will be added into the Metadata.

Example:
```python 
class AFooBar(object): 
    def __init__(self):
        self.x = 32.123
        self.y = 42.123

myData = dict(y='float32', x='float32')
json = ObjectFiwareConverter.obj2Fiware(AFooBar(), ind=4, dataTypeDict=myData)

```
wolud result to:
```json
{
    "y": {
        "type": "number", 
        "value": 42.123, 
        "metadata": {
            "python": {
                "type": "dataType", 
                "value": "float"
            }, 
            "dataType": {
                "type": "dataType", 
                "value": "float32"
            }
        }
    }, 
    "x": {
        "type": "number", 
        "value": 32.123, 
        "metadata": {
            "python": {
                "type": "dataType", 
                "value": "float"
            }, 
            "dataType": {
                "type": "dataType", 
                "value": "float32"
            }
        }
    }, 
    "type": "AFooBar", 
    "id": "AFooBar703e581d-3068-4b62-bfa3-c713707e6929"
}

```
At last, if you simply cannot create a class which contains the needed values (or everything is dynamically), just use the `setAttr`- Parameter.


```python
class SomeTempObject(object):
    pass

sto = SomeTempObject()
ObjectFiwareConverter.fiware2Obj(json, sto, setAttr=True) # The json from above
```

The Values are added via `setattr` and can be accesed by `getattr`:
```python
print getattr(sto, 'myStr') # --> would print Hi!
```


