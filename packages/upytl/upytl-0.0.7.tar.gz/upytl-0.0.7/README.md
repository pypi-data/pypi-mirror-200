# UPYTL
Ultra Pythonic Template Language (inspired by Vue.js)

## Installation And Usage
`python -m pip install upytl`


```python
from upytl import UPYTL, html as h

t = {
  h.Div(): 'Hello [[ which_world ]] world!'
}

upytl = UPYTL()

rendered = upytl.render(t, ctx={'which_world':'Python'}, doctype=None)
print(rendered)
```

```html
<div>
  Hello Python world!
</div>
```

## Features Supported:

- for-loop
- if-elif-else
- custom components with slots
- generic components

## About
Default render-behaviour for attributes is `str.format`, so you can
```python
h.Div(Class='{header_class}'): 'Header'

# or even
h.Div(Class='{class_map[header]}'): 'Header'

# note that `key` must be is unquoted - see `str.format` doc

```
If you don't want any processing just pass `bytes`

```python
h.Div(Class=b'no-{processing}'): 'Header'
```

To evaluate python expression pass string wrapped in `set` 

```python
h.Button(disabled={'not allow_submit'}): 'Submit'
```

There are special attributes: `For`, `If`, `Elif`, `Else`, their values are always treated as python expressions except for `Else` (its value is ignored) 
Also note that `For`-syntax is a bit trimmed compared to pure python.
```python
t = {
    h.Template(For='k in range(5)'):{
        h.Div(If='k != 3'): 'This is #[[ k ]]  div',
        h.Div(Else=''): 'Here should be div #3',
    }
}

```













