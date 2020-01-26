"""
	Build dlig feature code from "*.code" glyph names.

	Works best to run on a UFO in a varfontprep folder, so it doesn't generate code for nonexisting glyphs.

	USAGE:

	python <path>/make-dlig-fea-code.py "<path>/<source-font>.ufo"
"""

import sys
from fontParts.world import *

try:
    sourceUFO = sys.argv[1]
except IndexError:
    print("At least one arg required: path of UFO with code ligature glyphs")

font = OpenFont(sourceUFO, showInterface=False)

codeLigs = []

dligCode = ""

def makeDligBlock(ligName):
	feaName = ligName.replace(".code","")
	ligSequence = feaName.replace("_","' ") + "'"
	firstChar = feaName.split("_")[0]
	lastChar = feaName.split("_")[-1]
	block = f"""\
	lookup {feaName} {{
		ignore sub {firstChar} {ligSequence};
		ignore sub {ligSequence} {lastChar};
		sub {ligSequence} by {ligName};
	}} {feaName};
	"""
	return block

for g in font:
	if ".code" in g.name and "_" in g.name and g.name not in font.lib["public.skipExportGlyphs"]:
		codeLigs.append(g.name)

font.close()

codeLigsSorted = sorted(codeLigs,key=lambda x: x.count('_'),reverse=True)

dligBlocks = ""
for lig in codeLigsSorted:
	dligBlocks += makeDligBlock(lig) + "\n"

dligCode = f"""\
# generated by src/01-shell-scripts-for-sources/features/make-dlig-fea-code.py
feature dlig {{
	{dligBlocks}\
}} dlig;
"""

feaPath = "src/features/features/dlig-generated.fea"
with open(feaPath, "w") as f:
	f.write(dligCode)

print(f"→ dligCode saved to {feaPath}")
