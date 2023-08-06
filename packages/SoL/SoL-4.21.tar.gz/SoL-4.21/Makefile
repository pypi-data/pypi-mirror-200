# -*- coding: utf-8 -*-
# :Project:   SoL -- Main makefile
# :Created:   sab 08 nov 2008 21:16:39 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2008, 2009, 2010, 2013, 2014, 2015, 2016, 2018, 2019, 2020, 2021 Lele Gaifax
#

include Makefile.defs

.PHONY: clean
clean::
	$(MAKE) -C docs clean
	rm -rf build $(SOLSRC)/static/manual
	rm -f $(PACKED_CSS) $(PACKED_JS)
	-@find docs src -name '*~' -print0 | xargs -r0 rm

.PHONY: distclean
distclean:: clean
	rm -f development.db

development.db:
	$(SOLADMIN) initialize-db development.ini
	$(SOLADMIN) restore development.ini

.PHONY: generate-db-migration
generate-db-migration:
	read -p "Enter migration description: " MDESC && \
	  $(ALEMBIC) revision --autogenerate -m "$$MDESC"

.PHONY: upgrade-db
upgrade-db:
	$(SOLADMIN) upgrade-db development.ini

.PHONY: serve
serve: development.db compile-catalogs
	pserve --reload development.ini

.PHONY: test
test: compile-catalogs
	@$(PYTEST)
	-@$(COVERAGE) json -o $(COVERAGE_JSON)

.PHONY: test-slow
test-slow: compile-catalogs
	@$(PYTEST) --runslow

.PHONY: test-fail-soon
test-fail-soon: compile-catalogs
	@$(PYTEST) -x


include Makefile.i18n
include Makefile.manual
include Makefile.release
include Makefile.docker
