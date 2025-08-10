include .env

.PHONY: help
help: ## prints this help output
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | sort | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install: ## install the frontend
	@npm install

.PHONY: clean
clean: ## clean the frontend
	@npm cache clean --force

.PHONY: lint
lint: ## lint the frontend
	@npm run lint

.PHONY: test
test: ## test the frontend
	@npm run test

.PHONY: build
build: ## build the frontend
	@npm run build

.PHONY: run
run: ## run the frontend
	@npm run start
