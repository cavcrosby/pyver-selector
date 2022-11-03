include base.mk

# include other generic makefiles
include python.mk
include yamllint.mk
YAML_SRC = \
	./.github/workflows

# simply expanded variables
executables := \
	${python_executables}

_check_executables := $(foreach exec,${executables},$(if $(shell command -v ${exec}),pass,$(error "No ${exec} in PATH")))

.PHONY: ${HELP}
${HELP}:
	# inspired by the makefiles of the Linux kernel and Mercurial
>	@echo 'Common make targets:'
>	@echo '  ${SETUP}        - installs the distro-independent dependencies for this'
>	@echo '                 project'
>	@echo '  ${LINT}         - performs linting on the yaml configuration files'
>	@echo '  ${TEST}         - runs test suite for the project'

.PHONY: ${SETUP}
${SETUP}:
>	${PYTHON} -m pip install "setuptools>=61.0.0" --editable ".[dev]"

.PHONY: ${LINT}
${LINT}: ${YAMLLINT}

.PHONY: ${TEST}
${TEST}:
>	${PYTHON} -m unittest --verbose
