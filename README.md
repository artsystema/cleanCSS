# cleanCSS

`cleanCSS.py` is a small utility for tidying up CSS files. It removes duplicate properties for each selector while respecting `!important` rules, and it can optionally replace every `font-family` declaration with a font name you provide. The resulting CSS is then beautified using `cssbeautifier` if the package is available.

## Usage

The main entry point is the `deduplicate_css` function:

```python
from cleanCSS import deduplicate_css

deduplicate_css('style.css', 'style-clean.css', font_name='monospace')
```

Run the script directly to be prompted for a font name:

```bash
python cleanCSS.py
```

The cleaned style sheet will be written to `style-clean.css`.


