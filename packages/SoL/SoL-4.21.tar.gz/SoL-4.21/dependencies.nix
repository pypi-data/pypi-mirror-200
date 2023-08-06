# -*- coding: utf-8 -*-
# :Project:   SoL -- Derivations for some non packaged dependencies
# :Created:   sab 04 ago 2018 22:57:25 CEST
# :Author:    Alberto Berti <alberto@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2018 Alberto Berti
# :Copyright: © 2020, 2021, 2022, 2023 Lele Gaifax
#

{ pkgs ? import <nixpkgs> {},
  pypkgs ? pkgs.python3Packages }: rec {

  calmjs_parse = pypkgs.buildPythonPackage rec {
    pname = "calmjs.parse";
    version = "1.3.0";
    format = "wheel";
    src = pypkgs.fetchPypi {
      inherit pname version format;
      python = "py3";
      sha256 = "11852c5d5adda5039e06d3fd4a8481113f6f56239d8d944b3eeae1610f520a7a";
    };
    doCheck = false;
    buildInputs = with pypkgs; [
      ply
    ];
  };

  mp_extjs_desktop =
    let
      extjs = pkgs.fetchzip {
        url = "http://cdn.sencha.com/ext/gpl/ext-4.2.1-gpl.zip";
        sha256 = "0lp9yrl4ply0xkfi0dx1vy381aj3l758vmfx2vpmfa90d7h7vgbd";
      };
    in
      pypkgs.buildPythonPackage rec {
        inherit extjs;
        pname = "metapensiero.extjs.desktop";
        version = "2.0";
        src = pypkgs.fetchPypi {
          inherit pname version;
          sha256 = "28fc173e8277b2519b6786a7cfd3621ab6590ef7c5b3e496bbd26a504c008773";
        };
        doCheck = false;
        buildInputs = with pypkgs; [
          setuptools
        ];
        preBuild = ''
          mkdir -p src/metapensiero/extjs/desktop/assets/extjs
          cp -a $extjs/resources $extjs/src $extjs/ext-dev.js src/metapensiero/extjs/desktop/assets/extjs
          substituteInPlace MANIFEST.in --replace "prune src/metapensiero/extjs/desktop/assets/extjs" "recursive-include src/metapensiero/extjs/desktop/assets/extjs *.gif *.png *.jpg *.js *.css"
          substituteAllInPlace src/metapensiero/extjs/desktop/scripts/minifier.py
        '';
        propagatedBuildInputs = [
          pypkgs.rcssmin
          pypkgs.rjsmin
          pypkgs.ply
        ];
      };

  mp_sa_dbloady = pypkgs.buildPythonPackage rec {
    pname = "metapensiero.sqlalchemy.dbloady";
    version = "2.10";
    src = pypkgs.fetchPypi {
      inherit pname version;
      sha256 = "c02f79f242bd196b20f24edf4d8150e05a461934e9dd6fd0c7d95cda007bbf64";
    };
    doCheck = false;
    buildInputs = with pypkgs; [
      setuptools
    ];
    propagatedBuildInputs = with pypkgs; [
      progressbar2
      ruamel_yaml
      sqlalchemy
    ];
  };

  mp_sa_proxy = pypkgs.buildPythonPackage rec {
    pname = "metapensiero.sqlalchemy.proxy";
    version = "5.14";
    src = pypkgs.fetchPypi {
      inherit pname version;
      sha256 = "38d6f13370807f786886c6013997c68b2494e2998feff70c2a3d336a7861db26";
    };
    doCheck = false;
    buildInputs = with pypkgs; [
      setuptools
    ];
    propagatedBuildInputs = with pypkgs; [
      sqlalchemy
    ];
  };

  pygal_maps_world = pypkgs.buildPythonPackage rec {
    pname = "pygal_maps_world";
    version = "1.0.2";
    src = pypkgs.fetchPypi {
      inherit pname version;
      sha256 = "8987fcf7f067b56f40f2f83b4f87baf9456164bbff0995715377020fc533db0f";
    };
    doCheck = false;
    buildInputs = with pypkgs; [
      setuptools
    ];
    propagatedBuildInputs = with pypkgs; [
      pygal
    ];
  };

  python_rapidjson = pypkgs.buildPythonPackage rec {
    pname = "python_rapidjson";
    version = "1.9";
    src = pypkgs.fetchPypi {
      inherit version;
      pname = "python-rapidjson";
      sha256 = "be7d351c7112dac608133a23f60e95395668d0981a07f4037f63e0e88afcf01a";
    };
    doCheck = false;
    buildInputs = with pypkgs; [
      pkgs.rapidjson
    ];
  };

  pyramid_tm = pypkgs.buildPythonPackage rec {
    pname = "pyramid_tm";
    version = "2.4";
    src = pypkgs.fetchPypi {
      inherit pname version;
      sha256 = "5fd6d4ac9181a65ec54e5b280229ed6d8b3ed6a8f5a0bcff05c572751f086533";
    };
    doCheck = false;
    buildInputs = with pypkgs; [
      setuptools
    ];
    propagatedBuildInputs = with pypkgs; [
      pyramid transaction
    ];
  };

  pyramid_mailer = pypkgs.buildPythonPackage rec {
    pname = "pyramid_mailer";
    version = "0.15.1";
    src = pypkgs.fetchPypi {
      inherit pname version;
      sha256 = "ec0aff54d9179b2aa2922ff82c2016a4dc8d1da5dc3408d6594f0e2096446f9b";
    };
    doCheck = false;
    buildInputs = with pypkgs; [
      setuptools
    ];
    propagatedBuildInputs = with pypkgs; [
      pyramid transaction repoze_sendmail
    ];
  };

  repoze_sendmail = pypkgs.buildPythonPackage rec {
    pname = "repoze.sendmail";
    version = "4.4.1";
    src = pypkgs.fetchPypi {
      inherit pname version;
      sha256 = "096ln02jr2afk7ab9j2czxqv2ryqq7m86ah572nqplx52iws73ks";
    };
    doCheck = false;
    buildInputs = with pypkgs; [
      setuptools
    ];
    propagatedBuildInputs = with pypkgs; [
      transaction zope_interface
    ];
  };

  zope_sqlalchemy = pypkgs.buildPythonPackage rec {
    pname = "zope.sqlalchemy";
    version = "1.6";
    src = pypkgs.fetchPypi {
      inherit pname version;
      sha256 = "9c53be9a57275566595ada79bdffcd624a12fcf6435f6e6807416541b912f5ab";
    };
    doCheck = false;
    buildInputs = with pypkgs; [
      setuptools
    ];
    propagatedBuildInputs = with pypkgs; [
      sqlalchemy
      transaction
      zope_interface
    ];
  };

  system_deps = with pypkgs; [
    Babel
    XlsxWriter
    alembic
    itsdangerous
    pillow
    pycountry
    pygal
    pynacl
    pyramid
    pyramid_mako
    reportlab
    ruamel_yaml
    setuptools
    sqlalchemy
    transaction
    waitress
  ];

  local_deps = [
    calmjs_parse
    mp_extjs_desktop
    mp_sa_proxy
    pygal_maps_world
    pyramid_mailer
    pyramid_tm
    python_rapidjson
    zope_sqlalchemy
  ];

  test_deps = [
    mp_sa_dbloady
    pypkgs.pytest
    pypkgs.pytestcov
    pypkgs.webtest
  ];

  all_deps = local_deps ++ system_deps ++ test_deps;
}
