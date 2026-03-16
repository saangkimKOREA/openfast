1. objective:
openfast: i want to modify subDyn to implement pisa model on it.

2. project folder:
/home/sbkim/Work/openfast/openfast-subdyn-dev

it is a forked git from OpenFAST/openfast

3. sub folders:
0) original sub folders from OpenFAST/openfast v4.2.2 (?? or v4.2.0)

1) modules/subDyn/src
modifications will be done here

2) studies 
main example is based on 5MW_OC3Mnpl_DLL_WTurb_WavesIrr of r-test

3) post
python files for post process

4) results
outputb files

5) log
log files of porject development

4. main management file
PISA_DEV_LOG.md (this file)

5. plan
1) 1st modification
modules/subDyn/src/
SubDyn.f90.v0: original file
SubDyn.f90

please compare two files.

studies/pisa/5MW_OC3Mnpl_DLL_WTurb_WavesIrr.fst
it worked 