PDK_ROOT ?= $(CURDIR)/pdk_root
PDK       ?= fp5A

.PHONY: help install check smoke clean

help:
	@echo "make install PDK_ROOT=/path   install fp5A into a PDK root"
	@echo "make check                    run local DRC/LVS/model checks"
	@echo "make smoke                    run the LibreLane cnt8 example"
	@echo "make clean                    remove example run directories"

install:
	mkdir -p $(PDK_ROOT)
	rm -rf $(PDK_ROOT)/$(PDK)
	cp -a $(PDK) $(PDK_ROOT)/$(PDK)
	cp LICENSE NOTICE SOURCES $(PDK_ROOT)/$(PDK)/
	@echo "Installed $(PDK) -> $(PDK_ROOT)/$(PDK)"

check:
	./tools/check_pdk.sh

smoke:
	./tools/run_librelane.sh examples/librelane/cnt8/config.yaml

clean:
	rm -rf examples/librelane/cnt8/runs
