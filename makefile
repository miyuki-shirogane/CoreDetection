MESSAGE ?= "checkpoint"
DATE := $(shell date '+%Y-%m-%dT%H:%M:%S%z')

checkpoint:
	@git add -A
	@git commit -m "$(MESSAGE) at $(DATE)"
	@git push
	@echo Checkpoint created and pushed to remote
