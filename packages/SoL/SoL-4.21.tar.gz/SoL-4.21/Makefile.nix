# -*- coding: utf-8 -*-
# :Project:   SoL -- Nix targets
# :Created:   sab 21 set 2019 00:01:21 CEST
# :Author:    Alberto Berti <alberto@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2019 Alberto Berti
# :Copyright: © 2021 Lele Gaifax
#

RUNVM_TOKEN := .runvm-created
NREBUILD := nixos-rebuild


$(RUNVM_TOKEN): $(PWD)/nixos/vmtest.nix
	NIXOS_CONFIG=$< ${NREBUILD} build-vm
	touch $(@)

.PHONY: run-vm
run-vm: $(RUNVM_TOKEN)
	result/bin/run-vmhost-vm

.PHONY: clean
clean::
	rm -f $(RUNVM_TOKEN)
	rm -rf result*
	rm -f vmhost.qcow2

.PHONY: nix-release
nix-release:
	nix-build release.nix

.PHONY: nix-build-pygal
nix-build-pygal:
	nix-build --keep-failed -A pygal dependencies.nix
