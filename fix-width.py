#!/usr/bin/env fontforge
import os
import fontforge

for path in sys.argv[1:]:
    print(f"\033[1;31m{path}\033[m")
    f = fontforge.open(path)
    widths = {}
    max_count = 0
    target_width = 0
    f.selection.all()
    for g in f.selection.byGlyphs:
        cur = widths[g.width] = widths.get(g.width, 0) + 1
        if cur > max_count:
            max_count = cur
            target_width = g.width

    total = sum(widths.values())
    print(f"Setting all glyphs width to: {target_width}")
    print(f"Total glyphs: {total}")
    print(f"Glyphs to change: {total - max_count}")

    changelist = []
    for g in f.selection.byGlyphs:
        if g.width == target_width:
            continue
        changelist.append(g)
        print(f'\t{g.glyphname.ljust(16)}\tU+{g.unicode}\t{g.width}')

    for g in changelist:
        f.selection.select(g.glyphname)
        g.width = target_width

    if path.startswith('src/'):
        output = path.replace('src/', 'out/')
    else:
        output = 'new-' + path

    os.system(f"mkdir -p {os.path.dirname(output)}")
    print(f"\033[1;31m{output}\033[m")
    f.generate(output, flags=('opentype'))
    f.close()
