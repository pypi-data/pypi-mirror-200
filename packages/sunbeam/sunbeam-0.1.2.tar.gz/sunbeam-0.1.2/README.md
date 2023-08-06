# Sunbeam Types

Python helper classes for [sunbeam](https://pomdtr.github.io/sunbeam)

## Example

```python
import List, ListItem, CopyAction from sunbeam

page = List(items=[
    ListItem(title="list item 1"), actions=[
        CopyAction(text="Copy this")
    ]
])

print(page.json())
```
