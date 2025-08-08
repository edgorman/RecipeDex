include .env

.PHONY: help
help: ## prints this help output
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | sort | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install: ## install the backend
	@uv sync

.PHONY: lint
lint: ## lint the backend
	@uv run -- flake8 . --exclude .venv --max-line-length 120

.PHONY: test
test: ## test the backend
	@uv run -- pytest tests -svv

.PHONY: run-agent
run-agent: ## run the backend agents in adk web ui
	@adk web internal/agents/vertex/subagents

.PHONY: run-service
run-service: ## run the backend service
	@uv run -- commands/service.py run

.PHONY: build-service
build-service: ## build the backend service, optionally save as a .tar
	@docker build $(BUILD_ARGS) -t backend .
	@if [ -n "$(OUTPUT)" ]; then \
		docker save backend -o $(OUTPUT); \
	fi

# TODO: Might just be an issue with my local machine, but unable to run `gcloud` directly
.PHONY: proxy-service
proxy-service: ## run a proxy to the backend service
	@~/google-cloud-sdk/bin/gcloud run services proxy backend --project $(GCP_PROJECT_ID) --region $(GCP_PROJECT_REGION)
