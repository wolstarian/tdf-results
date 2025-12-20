from pathlib import Path
from dateutil import parser

# the full resolved path of this folder this file is in
# print(Path(__file__).resolve().parent)

resultspath = f'{Path(__file__).resolve().parent}/results'
stagespath = f'{Path(__file__).resolve().parent}/stages'
datapath = f'{Path(__file__).resolve().parent}/data_files'
full_file = f'{Path(__file__).resolve().parent}/full_file.txt'

#print(resultspath)

def read_results_file(year: int):
    reslines = []
    with open(f'{resultspath}/TdF_results_{str(year)}.md', 'r') as resfile:
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
    with open(f'{stagespath}/TdF_stages_{str(year)}.md', 'r') as resfile:
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

def merge_and_output(year: int):
    r_table = read_results_file(year)
    s_table = read_stages_file(year)

    # Merge results into stages; goes into s_table
    for sk in s_table:
        for rk in r_table:
            if rk == f"Stage {s_table[sk]['tdf-stage']}":
                s_table[sk].update(r_table[rk])
                break
            if rk == 'Prologue' and s_table[sk]['tdf-stage'] == 'Prologue':
                s_table[sk].update(r_table[rk])
                break

    content = ""
    for sk in s_table:
        if s_table[sk]['tdf-stage-type'] in ('Rest Day', 'Travel Day'):
            is_stage = ""
        else:
            is_stage = "Stage "
        #print(f"{sk}: {s_table[sk]}")
        datamdfile = f"{datapath}/TdF {year} {is_stage}{s_table[sk]['tdf-stage']}.md"
        lines = [
            "---",
            f"tdf-year: {year}",
            f"tdf-stage-date: {sk}",
            f"tdf-stage-type: {s_table[sk]['tdf-stage-type']}",
            f"tdf-stage-start: {s_table[sk]['tdf-stage-start']}",
            f"tdf-stage-finish: {s_table[sk]['tdf-stage-finish']}",
        ]
        if s_table[sk]['tdf-stage-type'] not in ('Rest Day', 'Travel Day'):
            lines.extend([
                f"tdf-stage: {s_table[sk]['tdf-stage']}",
                f"tdf-stage-distance(km): {s_table[sk]['tdf-stage-distance']}",
                f"tdf-stage-winner: {s_table[sk]['tdf-stage-winner']}",
                f"tdf-yellow: {s_table[sk]['tdf-yellow']}",
                f"tdf-green: {s_table[sk]['tdf-green']}",
                f"tdf-polkadot: {s_table[sk]['tdf-polkadot']}",
                f"tdf-white: {s_table[sk]['tdf-white']}",
            ])
        lines.append("---")
        content += "\n".join(lines) + "\n"   # trailing newline is optional but common
        #print(content)
        #print(datamdfile)
        with open(datamdfile, 'w') as outfile:
            outfile.write("\n".join(lines) + "\n")

    return content

for y in range(2012, 2025):
    print(y)
    merge_and_output(y)
