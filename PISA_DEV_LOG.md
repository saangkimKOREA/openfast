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