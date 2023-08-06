class Style:
    """`Style` has 6 class variables: `BOLD`, `DIM`, `ITALICS`, `UNDERLINE`, `STRIKETHROUGH`, and `RESET`. To use them, just concatenate them to a string like so:

```python
print(f"{Style.BOLD}This text is bold.{Style.RESET}")
```"""
    BOLD           = "\033[1m"
    DIM            = "\033[2m"
    ITALICS        = "\033[3m"
    UNDERLINE      = "\033[4m"
    STRIKETHROUGH  = "\033[9m"
    RESET          = "\033[22m"
