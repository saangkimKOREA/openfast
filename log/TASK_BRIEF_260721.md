# Task Brief — PISA/SubDyn — assigned 2026-07-21

You are acting as team lead for this task in tmux pane 0.1. Work autonomously,
verify everything before trusting docs (some are stale), report back clearly.

## Goal
Continue the OpenFAST SubDyn PISA nonlinear soil-spring implementation toward
Phase 9 (full offshore-model integration test), per the project plan.

## Known state (verify all of this — do not trust blindly)

1. **This repo** `~/Work/openfast/openfast-subdyn-dev` (branch `pisa_subdyn_experiment`,
   remote `origin` = saangkimKOREA/openfast, already has push credentials configured —
   do not touch remote config) already has:
   - `modules/subdyn/src/*.f90` with PISA modifications
   - a build tree at `build/` with `build/modules/subdyn/subdyn_driver` already compiled
   - `studies/pisa/5MW_OC3Mnpl_DLL_WTurb_WavesIrr.fst` — full 5MW OC3 monopile model
     with wind+wave (AeroDyn/HydroDyn/ElastoDyn/ServoDyn all present) — this is the
     realistic offshore model Phase 9 needs.
   - `PISA_DEV_LOG.md` (thin, outdated, ignore mostly)

2. **Canonical docs+snapshot repo** `~/Work/tipota/subDyn/` (git, pushed to
   `saangkimKOREA/tipota`) has the real phase history and docs:
   - `md/HANDOVER.md` and `md/PLAN.md` — read these FIRST, full architecture
     (Option B residual-force), data structures, output channels, phase table.
   - **BUG in these docs**: they say the working tree lives at `~/Work/openfast/pisa`.
     That path does not exist on this machine. The real working tree is
     `~/Work/openfast/openfast-subdyn-dev` (this repo). Fix the path references in
     HANDOVER.md/PLAN.md once you've confirmed which tree is authoritative (see
     step A below).
   - `src/*.f90` snapshot — **confirmed to differ** from this repo's
     `modules/subdyn/src/*.f90` (checked via `diff -rq`, all core PISA files differ:
     FEM.f90, SD_FEM.f90, SubDyn.f90, SubDyn_Driver.f90, SubDyn_Output.f90,
     SubDyn_Output_Params.f90, SubDyn_Registry.txt, SubDyn_Types.f90).
   - Per HANDOVER.md, phases 0-7 done, phase 8 (Newton iteration) implemented +
     targeted-tested, phase 9 (full integration test) is the open item.
   - `tests/pisa_snapshot_smoke.py` and `tests/pisa_am2_iteration_test.py` — existing
     validation scripts, portable (take a subdyn_driver path as arg).

3. Recent git history in this repo (`openfast-subdyn-dev`) has several low-info commit
   messages ("s1", "nl", "dl") — read the actual diffs, not just messages, to figure out
   what changed and when, since commit messages won't tell you.

## What to do

**A. Reconcile source of truth (do this before any new code work)**
   - Diff `~/Work/tipota/subDyn/src/*.f90` against
     `~/Work/openfast/openfast-subdyn-dev/modules/subdyn/src/*.f90` file by file.
   - Use `git log` dates/content on both sides to determine which is newer/more complete
     (this repo has real build history; tipota is a manually-copied snapshot that may be
     behind, per the sync instructions in HANDOVER.md §11 which nobody may have run recently).
   - Once determined, make `~/Work/tipota/subDyn/src/` match the authoritative version
     (copy + commit + push in tipota repo), and correct the path in HANDOVER.md/PLAN.md
     to point at `~/Work/openfast/openfast-subdyn-dev`.

**B. Verify build integrity**
   - Confirm `build/modules/subdyn/subdyn_driver` is built from the CURRENT source (check
     mtimes; rebuild if source is newer than the binary):
     `cmake --build build --target subdyn_driver -j$(nproc)`
   - Run `python3 ~/Work/tipota/subDyn/tests/pisa_snapshot_smoke.py <path-to-subdyn_driver>`
     — all checks must PASS before proceeding. If they don't, stop and diagnose — do not
     paper over a failing smoke test.

**C. Phase 9 — full integration test**
   - Use `studies/pisa/5MW_OC3Mnpl_DLL_WTurb_WavesIrr.fst` (5MW OC3 monopile, combined
     wave+wind) as the realistic model per HANDOVER.md's own definition of Phase 9.
   - Note there are `.v0`/`.v1` variants of `NRELOffshrBsline5MW_OC3Monopile_SubDyn.dat`
     in `studies/pisa/` — figure out which is the PISA-enabled version and which is
     baseline-linear, or whether you need to add the PISA section (format is documented
     in HANDOVER.md §6) to a clean copy.
   - Run baseline (no PISA / linear springs) vs PISA-enabled full-turbine simulation.
     Compare tower-base loads, foundation displacement, and reaction forces. Sanity-check
     against Phase 6 pushover results (Hu_total ≈ 2.034 MN, k0 ≈ 250 MN/m per the docs) —
     numbers should be in a physically reasonable range, not exact match (different model).
   - HANDOVER.md mentions comparing against SESAM/PLAXIS reference — if you don't have
     access to those, say so explicitly rather than fabricating a comparison; a
     baseline-vs-PISA physical sanity check is still valuable and is the minimum bar.
   - Document results in a new dated file under `~/Work/tipota/subDyn/reports/` or
     `log/`, following the existing style of `reports/subdyn_pisa_status_wiley_260710/`.

**D. Commit discipline**
   - Meaningful commit messages (not "s1"). Separate commits for: doc path fix, src sync,
     Phase 9 test setup, Phase 9 results.
   - Push both repos when done with a coherent state (ask before force-pushing anything,
     but these should all be normal fast-forward commits).

## Report back
When done (or if blocked), summarize: what was wrong in the docs, which source tree
won, smoke test result, Phase 9 setup/results, and anything that needs a human decision
(e.g. no SESAM/PLAXIS reference available).
