import re
try:
    import cssbeautifier
except ImportError:
    cssbeautifier = None

from collections import OrderedDict

def parse_properties(props_str):
    props = {}
    for line in props_str.split(';'):
        line = line.strip()
        if not line:
            continue
        if ':' not in line:
            continue
        name, value = line.split(':', 1)
        name = name.strip()
        value = value.strip()
        important = '!important' in value
        props[name] = (value, important)
    return props

def replace_font_family(selector_props, font_name):
    for props in selector_props.values():
        if 'font-family' in props:
            props['font-family'] = (font_name, False)

# Usage: deduplicate_css('style.css', 'style-clean.css', font_name=None)
def deduplicate_css(input_path, output_path, font_name=None):
    with open(input_path, 'r', encoding='utf-8') as f:
        css = f.read()

    # Remove all comments
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)

    pattern = re.compile(r'([^{]+)\{([^}]*)\}', re.DOTALL)
    matches = list(pattern.finditer(css))

    selector_props = OrderedDict()

    # Top to bottom, update each property for each selector
    for match in matches:
        selectors = match.group(1).strip()
        props_str = match.group(2).strip()
        selector_list = [s.strip() for s in selectors.split(',')]
        props = parse_properties(props_str)
        for sel in selector_list:
            if sel not in selector_props:
                selector_props[sel] = OrderedDict()
            for pname, (pval, pimportant) in props.items():
                if pname not in selector_props[sel]:
                    selector_props[sel][pname] = (pval, pimportant)
                else:
                    old_val, old_important = selector_props[sel][pname]
                    if pimportant:
                        selector_props[sel][pname] = (pval, pimportant)
                    elif not old_important:
                        selector_props[sel][pname] = (pval, pimportant)
                    # If old is important and new is not, keep old

    if font_name:
        replace_font_family(selector_props, font_name)

    # Build clean CSS, preserving selector order
    clean_blocks = []
    for sel, props in selector_props.items():
        block = sel + ' {\n'
        for pname, (pval, _) in props.items():
            block += f'  {pname}: {pval};\n'
        block += '}'
        clean_blocks.append(block)

    combined_css = '\n\n'.join(clean_blocks)
    if cssbeautifier:
        combined_css = cssbeautifier.beautify(combined_css)
    else:
        print('cssbeautifier not installed. Output will not be beautified.')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(combined_css)

# Usage example:
# deduplicate_css('style.css', 'style-clean.css', font_name='monospace')
if __name__ == '__main__':
    answer = input('Replace all font-family? Type font name or leave blank to skip: ').strip()
    font_name = answer if answer else None
    deduplicate_css('style.css', 'style-clean.css', font_name=font_name)