import Lake
open Lake DSL

package "lean_project" where
  version := v!"0.1.0"

lean_lib «LeanProject» where
require mathlib from git
    "https://github.com/leanprover-community/mathlib4.git"
  -- add library configuration options here

@[default_target]
lean_exe "lean_project" where
  root := `Main
