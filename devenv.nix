{ pkgs, lib, ... }:

let
  python = pkgs.python312;
  pythonPackages = python.pkgs;
in
{
  packages = [
    python
    pythonPackages.tkinter
    pkgs.tk
    pkgs.tcl
    pkgs.stdenv.cc.cc.lib
    pkgs.zlib
    pkgs.libGL
    pkgs.xorg.libX11
    pkgs.xorg.libXext
    pkgs.xorg.libXrender
    pkgs.xorg.libSM
    pkgs.xorg.libICE
  ];

  env = {
    VENV_DIR = ".devenv/state/venv";
    PIP_DISABLE_PIP_VERSION_CHECK = "1";
    PYTHONNOUSERSITE = "1";
    TCL_LIBRARY = "${pkgs.tcl}/lib/tcl${pkgs.tcl.version}";
    TK_LIBRARY = "${pkgs.tk}/lib/tk${pkgs.tk.version}";
    LD_LIBRARY_PATH = lib.makeLibraryPath [
      pkgs.stdenv.cc.cc.lib
      pkgs.zlib
      pkgs.libGL
      pkgs.xorg.libX11
      pkgs.xorg.libXext
      pkgs.xorg.libXrender
      pkgs.xorg.libSM
      pkgs.xorg.libICE
    ];
  };

  enterShell = ''
    echo "RayTracing devenv"
    echo "Python $(${python}/bin/python --version | cut -d' ' -f2)"

    if [ ! -x "$VENV_DIR/bin/python" ]; then
      ${python}/bin/python -m venv --system-site-packages "$VENV_DIR"
    fi

    . "$VENV_DIR/bin/activate"

    python -m ensurepip --upgrade >/dev/null 2>&1 || true
    python -m pip install --upgrade pip setuptools wheel build >/dev/null
    python -m pip install --upgrade -e ".[gui]" pillow basedpyright ruff >/dev/null

    export PATH="$PWD/$VENV_DIR/bin:$PATH"
  '';
}
