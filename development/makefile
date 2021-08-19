SHELL := /bin/bash

### GIT ###
.PHONY: git-hooks
git-hooks:
	chmod +x githooks/*
	mkdir -p ../.git/hooks
	ln -s -f ../../development/githooks/pre-commit ../.git/hooks/pre-commit