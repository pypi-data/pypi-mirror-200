
# Features:

## **clip**
-------------
`clip` contains the following function:

***.clip***
-------------
Puts a string into the user's clipboard Notice: currently only the win32 platform is supported for this.

**Possible Arguments:**

- **`content`** The String that should be put in the users clipboard. _This string cannot be empty or only contain whitespace/spaces_ 
    - Type: `str`
- `no_os_error` Tells the function to not raise a `OSError` when the operating system is not`win32` 
    - Type: `bool` 
    - Default: `False`

**Use**:
```python
from einfach import clip
    
clip.clip(content="Hello World") 
# this wont ignore the OSError that is raised when not run on win32
    
clip.clip(content="Hi! :D", no_os_error=True) 
# this will ignore the OSError if run on a non win32 platform. This will result in the clipboard not changing on the non-win32 os. 
```

---
## **pathdialog**
-------------
`pathdialog` contains the following functions:

***.open_file***
-------------
***.save_file***
-------------
***.open_dir***
-------------