from pathlib import Path
from dateutil import parser

# the full resolved path of this folder this file is in
# print(Path(__file__).resolve().parent)

resultspath = f'{Path(__file__).resolve().parent}/results'
stagespath = f'{Path(__file__).resolve().parent}/stages'

#print(resultspath)

def read_results_file(year: int):
    reslines = []
    with open(f'{resultspath}/TdF_results_20{str(year)}.md', 'r') as resfile:
        for line in resfile:
            if line.startswith('|'):
                reslines.append(line)

    del reslines[0]  # remove header line
    del reslines[0]  # remove separator line

    res_table = {}
    for line in reslines:
        #print(line)
        parts = [p.strip() for p in line.split('|')[1:-1]]
        #print(parts)
        key, *cols = parts
        res_table[key] = {
            'tdf-stage-winner': cols[0],
            'tdf-yellow': cols[1],
            'tdf-green': cols[2],
            'tdf-polkadot': cols[3],
            'tdf-white': cols[4],
        }
    return res_table

def read_stages_file(year: int):
    reslines = []
    with open(f'{stagespath}/TdF_stages_20{str(year)}.md', 'r') as resfile:
        for line in resfile:
            if line.startswith('|'):
                reslines.append(line)

    del reslines[0]  # remove header line
    del reslines[0]  # remove separator line

    res_table = {}
    for line in reslines:
        #print(line)
        parts = [p.strip() for p in line.split('|')[1:-1]]
        #print(parts)
        #*cols = parts
        dt = parser.parse(parts[2])          # → datetime.datetime(2025, 12, 7, 14, 30)
        key = dt.strftime("%Y-%m-%d") 
        res_table[key] = {
            'tdf-stage': parts[0].removeprefix('Stage '),
            'tdf-stage-type': parts[1],
            'tdf-stage-start': parts[3],
            'tdf-stage-finish': parts[4],
            'tdf-stage-distance': parts[5].removesuffix(' km'),
        }
    return res_table

year = 20
r_table = read_results_file(year)
#for k in r_table:
#    print(f"{k}: {r_table[k]}")

s_table = read_stages_file(year)
#for k in s_table:
#    print(f"{k}: {s_table[k]}")

for sk in s_table:
    for rk in r_table:
        if rk == f"Stage {s_table[sk]['tdf-stage']}":
            #print(f"Merging {rk} into {sk}")
            s_table[sk].update(r_table[rk])
            #print(f"After merge: {sk}: {s_table[sk]}\n")
            break

for sk in s_table:
    print(f"{sk}: {s_table[sk]}\n")



