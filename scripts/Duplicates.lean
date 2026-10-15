import Lean
open Lean

/-- Lean's auto-generated helpers (equation lemmas, `congr_simp`, `noConfusion`, …). -/
def isGenerated (env : Environment) (n : Name) : Bool :=
  n.isInternalDetail || isAuxRecursor env n || isNoConfusion env n ||
  (match n with
   | .str _ s => s.startsWith "eq_" || s == "congr_simp" || s == "injEq" || s == "inj" ||
       s == "sizeOf_spec" || s == "ctorIdx" || s == "eq_def" || s == "ext_iff"
   | _ => false) ||
  (match env.find? n with
   | some (.ctorInfo _) | some (.recInfo _) | some (.inductInfo _) => true
   | _ => false)

/-- Rename universe parameters to `u0, u1, …` so equal statements compare equal. -/
def canon (ci : ConstantInfo) (e : Expr) : Expr :=
  e.instantiateLevelParams ci.levelParams
    ((List.range ci.levelParams.length).map fun i => .param (.mkSimple s!"u{i}"))

partial def stripLam : Expr → Expr
  | .lam _ _ b _ => stripLam b
  | .mdata _ e => stripLam e
  | e => e

/-- Usage: `lake env lean --run Duplicates.lean <Module>...`
Prints tab-separated lines:
  same-theorem  <a> <b>    two theorems of the modules with identical statements
  same-def      <a> <b>    two definitions with identical type and body
  in-library    <a> <b>    a theorem whose statement is already a library theorem `b`
  corollary     <a> <b>    a theorem whose whole proof is `b` applied to arguments -/
def main (args : List String) : IO Unit := do
  initSearchPath (← findSysroot)
  let mods := args.map (·.toName)
  let env ← importModules (mods.map ({ module := · })).toArray {}
  let idxs := mods.filterMap env.getModuleIdx?
  let ours (n : Name) : Bool := match env.getModuleIdxFor? n with
    | some i => idxs.contains i
    | none => false
  let mut thms : Std.HashMap Expr (Array Name) := {}
  let mut defs : Std.HashMap (Expr × Expr) (Array Name) := {}
  let mut ourThms : Array (Name × ConstantInfo) := #[]
  for i in idxs do
    for c in env.header.moduleData[i.toNat]!.constNames do
      if isGenerated env c then continue
      match env.find? c with
      | some ci@(.thmInfo _) =>
        thms := thms.alter (canon ci ci.type) (some <| ·.getD #[] |>.push c)
        ourThms := ourThms.push (c, ci)
      | some ci@(.defnInfo d) =>
        let key := (canon ci ci.type, canon ci d.value)
        defs := defs.alter key (some <| ·.getD #[] |>.push c)
      | _ => pure ()
  for (_, ns) in thms do
    for n in ns[1:] do IO.println s!"same-theorem\t{ns[0]!}\t{n}"
  for (_, ns) in defs do
    for n in ns[1:] do IO.println s!"same-def\t{ns[0]!}\t{n}"
  -- library theorems, indexed by statement
  let mut lib : Std.HashMap Expr Name := {}
  for (n, ci) in env.constants.map₁.toList do
    if let .thmInfo _ := ci then
      if !ours n && !isGenerated env n then lib := lib.insert (canon ci ci.type) n
  for (n, ci) in ourThms do
    if let some m := lib[canon ci ci.type]? then IO.println s!"in-library\t{n}\t{m}"
    if let .thmInfo { value := v, .. } := ci then
      if let .const b _ := (stripLam v).getAppFn then
        if b != n && !isGenerated env b then IO.println s!"corollary\t{n}\t{b}"
