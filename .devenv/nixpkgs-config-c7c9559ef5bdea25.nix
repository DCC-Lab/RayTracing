let cfg = {}; in cfg // {
  allowUnfreePredicate =
    if cfg.allowUnfree or false then
      (_: true)
    else if (cfg.permittedUnfreePackages or []) != [] then
      (pkg: builtins.elem ((builtins.parseDrvName (pkg.name or pkg.pname or pkg)).name) (cfg.permittedUnfreePackages or []))
    else
      (_: false);
}