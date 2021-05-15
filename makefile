SHELL := /bin/bash

### GIT ###
.PHONY: git-hooks
git-hooks:
	chmod +x githooks/*
	mkdir -p .git/hooks
	cd .git/hooks && ln -sf ../../githooks/* .