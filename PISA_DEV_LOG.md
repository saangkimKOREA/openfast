# PISA Development Log

## Date


## Git branch


## OpenFAST commit hash


## Objective


## Files modified


## Design decisions


## Numerical issues


## Validation results


## Next steps

<<<<<<< HEAD
5. 2nd step
Task: Refactor my SubDyn "PISA macro-element prototype" so it is controlled by the SubDyn input file, not hard-coded.

Constraints:
- Only edit SubDyn.f90 (and SubDyn_Types.f90 if needed). Do not touch other OpenFAST modules.
- Keep behavior identical to current: Fpisa(1:6) = -PISA_K(1:6)*u_TP(1:6) - PISA_C(1:6)*udot_TP(1:6) and add it to Y1(1:6) inside SD_CalcOutput.
- Remove the hard-coded initialization block in SD_Init that sets UsePISA=.true. and assigns example stiffness values.

Implementation details:
- Add new input parameters in the SubDyn input-file reader section (near GuyanLoadCorrection / before "FEA and CRAIG-BAMPTON PARAMETERS"):
  * UsePISA (logical)
  * PISA_K(6) (ReKi array)
  * PISA_C(6) (ReKi array)
- Set defaults: UsePISA=.false., arrays = 0.0.
- Update any echo/validation needed.
- Ensure code compiles (declare Fpisa if not already declared where used).

Deliver:
- Show the exact new input-file lines expected (with comments).
- Provide a minimal diff-style summary of changes.

=======
5.
    surge motion (PtfmSurge_[m])
        PISA_K(1) (surge / x-translation)
    sway motion (PtfmSway_[m])
        PISA_K(2) (sway / y-translation)
    checking fore-aft bending / pitch-type response
        PISA_K(5) (pitch / rotation about y)
    side-side bending / roll-type response
        PISA_K(4) (roll / rotation about x)
>>>>>>> 048f7dd095b37469ac7fe933ec878e8380562339

4. 1st step
    - a mudline 6-DOF macro-element (not distributed springs)
        1)
        Add a new derived type for PISA parameters + state to SubDyn_Types.f90
            PISA_Par (curves, coefficients, limits)
            PISA_State (history variables, last displacement, plastic vars, etc.)
            Add them into the main SubDyn parameter/state containers (whatever SubDyn uses: typically p, x, m style).
        2) Physics routines
            PISA_Init(Par, State, ErrStat, ErrMsg)
            PISA_Calc( u6, udot6, dt, State, F6, Kt6 )
                u6 = [x,y,z,rx,ry,rz] at the interface point (mudline/TP depending on your chosen coupling)
                F6 = [Fx,Fy,Fz,Mx,My,Mz]
                Kt6 = tangent stiffness 6×6 (optional at first)
            Keep this independent so you can test it from SubDyn_Driver.f90.

3. files
    1) given
        SubDyn_Output.f90
        SubDyn.f90 = the module wrapper that OpenFAST calls every time step (Init/CalcOutput/UpdateStates/End)
        SD_FEM.f90 + FEM.f90 = the structural solver machinery (matrices, modal/CB reduction, assembly, stepping)
        SubDyn_Types.f90 = data structures (where you store new parameters + state variables).
        SubDyn_Output*.f90 = only for writing outputs (don’t put physics here)
        SubDyn_Registry.txt = how types/IO get auto-generated.

        SubDyn_Driver.f90 = standalone driver/testing harness (very useful for unit tests of your PISA element)
        SubDyn_Tests.f90 = tests

2.  inside SubDyn

    PISA_UpdateState( x, xdot, dt, state ) -> F, dFdx,

    Pattern 1:
        Within each global time step,
        soil as providing a nonlinear restoring force at a boundary DOF set (mudline / distributed)
        run a few Newton (or quasi-Newton) iterations:
            build residual,
            compute tangent (analytical or secant),
            update q, dq
    Pattern 2:
        At each time step:
            evaluate current nonlinear soil state,
            compute tangent stiffness 
        often stabilizes things without a full Newton solve

1.
    mamba activate pyfast
    (pyfast) sbkim@DESKTOP-NT9FR83:~/openfast$ git checkout -b pisa_subdyn_experiment
# FINE