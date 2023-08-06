# Colors And Styles

A basic package that makes it easy to add color and styles to your terminal.

## How to use
First go to the terminal and run `pip install ColorsAndStyles`. Then create a Python file and paste this code in it:

```python
from ColorsAndStyles import Color, Style, RESET_ALL
```

`RESET_ALL` is a string with the ANSI color code to reset all colors and styles.

### Color
`Color` has 3 classes: `RGB`, `Foreground`, and `Background`.

- `RGB` requires 4 arguments:

| Parameter      | Description                                                                                           |
|----------------|-------------------------------------------------------------------------------------------------------|
| `red`          | The red value of the RGB.                                                                             |
| `green`        | The green value of the RGB.                                                                           |
| `blue`         | The blue value of the RGB.                                                                            |
| `isForeground` | Returns a foreground ANSI color code if `True`. Else returns a background ANSI color code. (Optional) |

As a string, an `RGB` value returns an ANSI color code.

- `Foreground` has 8 class variables: `BLACK`, `RED`, `GREEN`, `YELLOW`, `BLUE`, `MAGENTA`, `CYAN`, and `RESET`. They are assigned to their respective ANSI color codes. To use these color codes, simply concatenate them with a string like so:

```python
print(f"{Color.Foreground.RED}This text is red.{Color.Foreground.RESET}")
```

- `Background` has 9 class variables: `BLACK`, `RED`, `GREEN`, `YELLOW`, `BLUE`, `MAGENTA`, `CYAN`, `WHITE` and `RESET`. To use them, just concatenate them to a string just like `Foreground`'s class variables:

```python
print(f"{Color.Background.GREEN}This text is green.{Color.Background.RESET}")
```

### Style
`Style` has 6 class variables: `BOLD`, `DIM`, `ITALICS`, `UNDERLINE`, `STRIKETHROUGH`, and `RESET`. Like the classes in `Color`, they are assigned to their respective ANSI color codes. Concatenate them to strings to use them:

```python
print(f"{Style.BOLD}This text is bold.{Style.RESET}")
```
