# SNBT
###### Author: HellishBro

SNBT is a module that allows you to create SNBT objects in Minecraft.

# Examples
###### <sub>ok heres some examples</sub>

```python
import SNBT
print(SNBT.SNBTCompound({
    "direction": [-1, 3, 2],
    "Count": 1,
    "isGrounded": True,
    "motions": [
        [0.1, 21.2],
        [True, 1, False],
        [12917826836018, 1]
    ]
}).dump())
# prints:
# {"direction":[B;-1b,3b,2b],"Count":1b,"isGrounded":1b,"motions":[[0.1f,21.2f],[1b,1b,0b],[12917826836018l,1b]]}
```

# TODO
###### prob. wont be added
* [ ] Convert from SNBT to SNBT Compound
* [ ] Load / Dump to JSON