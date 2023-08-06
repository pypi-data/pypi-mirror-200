# Usage

simple_json_flatten_py is a Python library for flattening complex JSONs

From

```JSON
{
"a": [ {"b":37},{"c":64}],
"g": 26
}
```
To

```
{
  "a_b":37,
  "a_c":64,
  "g":26
}
```

```Python
from simple_flatten_json_py import flatten_json

# Sample JSON data
data={
  "cat": [
    {
      "fish": "tuna"
    },
    {
      "chicken": 3
    },
    {
      "medicine": {
        "pills": 20
      }
    }
  ]
}
# returns a flattened json 
# {"_cat_0_fish": "tuna",  "_cat_1_chicken": 3,"_cat_2_medicine_pills": 20}
'''
print(flatten_json.flatten_json(data))
```
