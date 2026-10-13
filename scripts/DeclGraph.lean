import Lean
open Lean

/-- Fold auxiliary constants (`foo._proof_1`, `foo.match_1`, constructors, recursors, …)
into the user-facing declaration they belong to. -/
partial def rep (env : Environment) (n : Name) : Name :=
  match env.find? n with
  | some (.ctorInfo c) => c.induct
  | some (.recInfo _) => n.getPrefix
  | _ =>
    if n.isInternalDetail || isAuxRecursor env n then
      if n.getPrefix.isAnonymous then n else rep env n.getPrefix
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

/-- Usage: `lake env lean --run DeclGraph.lean <Module> [<root declaration>] [--decls <out.tsv>]`.
Prints a DOT graph of the declarations of `<Module>`, with an edge `a -> b` when `b` uses `a`.
With a root, only the declarations the root transitively depends on are kept.
With `--decls`, also writes one line per constant of the module:
name, graph node it is folded into, kind, first and last source line (0 if unknown). -/
def main (args : List String) : IO Unit := do
  let (args, declsOut) := match args.span (· != "--decls") with
    | (pre, _ :: path :: post) => (pre ++ post, some path)
    | (pre, _) => (pre, none)
  let mod := args[0]!.toName
  initSearchPath (← findSysroot)
  let env ← importModules #[{ module := mod }] {}
  let some idx := env.getModuleIdx? mod | throw <| IO.userError s!"unknown module {mod}"
  let inMod (n : Name) : Bool := env.getModuleIdxFor? n == some idx
  let mut deps : Std.HashMap Name NameSet := {}
  let mut rows : Array String := #[]
  for c in env.header.moduleData[idx.toNat]!.constNames do
    let some ci := env.find? c | continue
    let src := rep env c
    if declsOut.isSome then
      let r := (declRangeExt.find? (level := .exported) env c <|>
        declRangeExt.find? (level := .server) env c <|>
        declRangeExt.find? (level := .private) env c).map (·.range)
      let (a, b) := r.elim (0, 0) fun r => (r.pos.line, r.endPos.line)
      rows := rows.push s!"{c}\t{src}\t{kindOf ci}\t{a}\t{b}"
    let mut s := deps.getD src {}
    for u in ci.getUsedConstantsAsSet do
      let tgt := rep env u
      if inMod u && tgt != src then s := s.insert tgt
    deps := deps.insert src s
  if let some path := declsOut then
    IO.FS.writeFile path ("\n".intercalate rows.toList ++ "\n")
  let mut keep : NameSet := {}
  if let some r := args[1]? then
    let mut todo := [r.toName]
    while !todo.isEmpty do
      let n := todo.head!
      todo := todo.tail!
      if keep.contains n then continue
      keep := keep.insert n
      todo := (deps.getD n {}).toList ++ todo
  else
    keep := deps.fold (fun s n _ => s.insert n) {}
  IO.println "digraph G {\n  rankdir=TB;\n  node [fontname=Helvetica, style=filled];"
  for n in keep do
    let (shape, color) := match env.find? n with
      | some (.thmInfo _) => ("ellipse", "#cfe8ff")
      | _ => ("box", "#d9f2d0")
    IO.println s!"  \"{n}\" [shape={shape}, fillcolor=\"{color}\"];"
  for n in keep do
    for d in deps.getD n {} do
      if keep.contains d then IO.println s!"  \"{d}\" -> \"{n}\";"
  IO.println "}"
