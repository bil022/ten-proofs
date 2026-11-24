import Lean
open Lean

/-! Read a batch of compiled riemann-hypothesis modules and print their
constants and what each one uses. Step 1 of `rh_graph.sh`; `rh_cone.py` joins
the batches.

Usage: lake env lean --run RHRead.lean <file listing .olean paths> > out.tsv

A process maps three files per module and never unmaps them, so a batch must
stay well below `vm.max_map_count` / 3 modules (about 20,000 by default).

Output, one line per folded declaration:
  name  name-without-private-prefix  kind  module  used constants (space separated)
  first line  last line
The lines are where the declaration is in its source file (0 when the .olean
does not record it; it records them only for declarations it exports).
Auxiliary constants (`foo._proof_1`, `foo.match_1`, constructors, recursors, …)
are folded into the declaration they belong to, as in `../DeclGraph.lean`. -/

def auxSuffixes : List String :=
  ["casesOn", "recOn", "brecOn", "binductionOn", "below", "ibelow"]

/-- The declaration a constant is folded into, using only the constants of its
own module (a constructor or recursor lives in the module of its inductive). -/
partial def rep (find? : Name → Option ConstantInfo) (n : Name) : Name :=
  match find? n with
  | some (.ctorInfo c) => c.induct
  | some (.recInfo _) => n.getPrefix
  | _ =>
    let aux := match n with
      | .str _ s => auxSuffixes.contains s
      | _ => false
    if n.isInternalDetail || aux then
      if n.getPrefix.isAnonymous then n else rep find? n.getPrefix
    else n

def kindOf : ConstantInfo → String
  | .thmInfo _ => "theorem"
  | .defnInfo _ => "def"
  | .inductInfo _ => "inductive"
  | .ctorInfo _ => "ctor"
  | .recInfo _ => "rec"
  | .opaqueInfo _ => "opaque"
  | .axiomInfo _ => "axiom"
  | .quotInfo _ => "quot"

/-- The entries of `Lean.declRangeExt` stored in a module: (declaration, ranges). -/
unsafe def castRanges (e : Array EnvExtensionEntry) : Array (Name × DeclarationRanges) :=
  e.map unsafeCast

def main (args : List String) : IO Unit := do
  let out ← IO.getStdout
  for line in (← IO.FS.lines args[0]!) do
    let f : System.FilePath := line
    let mod := ((line.splitOn "/lib/lean/").getLast!.dropEnd ".olean".length).toString.replace "/" "."
    let priv := f.addExtension "private"
    let parts ← if ← priv.pathExists then
        readModuleDataParts #[f, f.addExtension "server", priv]
      else pure #[← readModuleData f]
    -- Later parts carry more (the private part has the proofs); keep the last copy.
    let mut consts : Std.HashMap Name ConstantInfo := {}
    for (d, _) in parts do
      for c in d.constants do consts := consts.insert c.name c
    let mut ranges : Std.HashMap Name (Nat × Nat) := {}
    for (d, _) in parts do
      for (ext, es) in d.entries do
        if ext == `Lean.declRangeExt then
          for (c, r) in unsafe castRanges es do
            ranges := ranges.insert c (r.range.pos.line, r.range.endPos.line)
    let mut used : Std.HashMap Name NameSet := {}
    for (n, ci) in consts do
      let r := rep consts.get? n
      used := used.insert r ((used.getD r {}).append ci.getUsedConstantsAsSet)
    for (r, s) in used do
      let kind := (consts.get? r).elim "?" kindOf
      let us := " ".intercalate (s.toList.filter (· != r) |>.map toString)
      let (a, b) := ranges.getD r (0, 0)
      out.putStrLn s!"{r}\t{privateToUserName r}\t{kind}\t{mod}\t{us}\t{a}\t{b}"
