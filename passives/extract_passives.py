"""FP5: median passive parameters of AMI C5 from MOSIS lot reports (sheet R, contact R, width variation, capacitances)."""
import os, re, html, glob, statistics as st, collections
W = os.environ.get('FP5_MOSIS_PARAMS', os.path.expanduser('~/ext/mosis_cards/wayback_params'))
if not os.path.isdir(W):
    raise SystemExit(f'FP5_MOSIS_PARAMS not found: {W}\nThis is a build-time input, not needed to use the checked-in passives.')

acc = collections.defaultdict(list)
def table(t, title):
    out = []
    for m in re.finditer(title + r'\s+([^\n]*)\n((?:[^\n]*\n){1,14})', t):
        cols = m.group(1).split()
        for line in m.group(2).splitlines():
            if not line.strip() or re.match(r'\s*(COMMENTS|[A-Z ]+PARAMETERS)', line): break
            name = re.match(r'\s*([A-Za-z][A-Za-z \(\)\+/_\-\.]*?)\s{2,}', line)
            if not name: continue
            vals = line[name.end():]
            # align numbers to columns by character position of header tokens
            out.append((name.group(1).strip(), cols, vals))
    return out
seen = set()
for f in sorted(glob.glob(f'{W}/ami-c5*__*.txt')):
    t = html.unescape(re.sub(r'<[^>]+>', '', open(f, errors='replace').read())).replace('\r', '')
    run = (re.search(r'RUN:\s*(\S+)', t) or [0, ''])[1]
    if not run or run in seen or 'SCN05' not in t: continue
    seen.add(run)
    for title in ('PROCESS PARAMETERS', 'CAPACITANCE PARAMETERS'):
        for m in re.finditer(title + r'([^\n]*)\n((?:[^\n]*\n){1,14})', t):
            hdr = m.group(1); cols = [(x.group(0), x.start()) for x in re.finditer(r'\S+', hdr)]
            if not cols: continue
            for line in m.group(2).splitlines():
                if re.match(r'\s*(COMMENTS|[A-Z ]{6,}PARAMETERS)', line) or not line.strip(): break
                nm = re.match(r'\s*(.*?)\s{2,}', line)
                if not nm: continue
                for x in re.finditer(r'-?\d+\.?\d*', line[nm.end():]):
                    pos = nm.end() + x.start() + len(x.group(0))   # right edge of number
                    col = min(cols, key=lambda c: abs((c[1] + len(c[0])) - pos))[0]
                    acc[(title[:4], nm.group(1).strip(), col)].append(float(x.group(0)))
print(f'{len(seen)} C5 lots')
for k, v in sorted(acc.items()):
    if len(v) >= 20: print(f'{k[0]} | {k[1]:28s} | {k[2]:8s} | n {len(v):3d} median {st.median(v):9.3f} sd {st.pstdev(v):7.3f}')
