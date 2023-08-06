# -*- coding: utf-8 -*-
# :Project:   SoL -- nix environment
# :Created:   sab 04 ago 2018 22:57:25 CEST
# :Author:    Alberto Berti <alberto@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2018 Alberto Berti
# :Copyright: © 2020, 2021 Lele Gaifax
#

let
  # nixos-21.05-small Released on 2021-09-10
  pkgs_hash = "8b0b81dab17753ab344a44c04be90a61dc55badf";
  pkgs_url = "https://github.com/NixOs/nixpkgs/archive/${pkgs_hash}.tar.gz";
  pkgs = import (fetchTarball {url = pkgs_url;}) {};
  sol = import ./release.nix { inherit pkgs; };
  deps = import ./dependencies.nix { inherit pkgs; };
in
  pkgs.mkShell {
    inputsFrom = [ sol ];
    venvDir = "./.venv";
    buildInputs = deps.all_deps ++ (with pkgs; [ python3Packages.venvShellHook ]);
    postVenvCreation = ''
      unset SOURCE_DATE_EPOCH
      pip install -e .
    '';
    postShellHook = ''
      export XDG_DATA_HOME="${pkgs.dejavu_fonts}/share";
    '';
  }
