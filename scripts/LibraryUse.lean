import Lean
open Lean

/-- Usage: `lake env lean --run LibraryUse.lean <Module>...`
For every library constant used by a declaration of the given modules, prints
  <module of the user>  <library constant>  <library module>  <number of declarations using it>  <kind>
"Library" means anything outside the given modules (Mathlib, Lean core, …). -/
def main (args : List String) : IO Unit := do
  initSearchPath (← findSysroot)
  let mods := args.map (·.toName)
  let env ← importModules (mods.map ({ module := · })).toArray {}
  let idxs := mods.filterMap env.getModuleIdx?
  for i in idxs do
    let mut count : Std.HashMap Name Nat := {}
    for c in env.header.moduleData[i.toNat]!.constNames do
      let some ci := env.find? c | continue
      for u in ci.getUsedConstantsAsSet do
        match env.getModuleIdxFor? u with
        | some j => if !idxs.contains j then count := count.alter u (some <| ·.getD 0 + 1)
        | none => pure ()
    let modName := env.header.moduleNames[i.toNat]!
    for (u, n) in count do
      let src := (env.getModuleIdxFor? u).map (env.header.moduleNames[·.toNat]!) |>.getD .anonymous
      let kind := match env.find? u with
        | some (.thmInfo _) => "theorem"
        | some (.defnInfo _) => "def"
        | some (.inductInfo _) => "type"
        | some (.ctorInfo _) => "ctor"
        | _ => "other"
      IO.println s!"{modName}\t{u}\t{src}\t{n}\t{kind}"
