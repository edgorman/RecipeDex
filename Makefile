.PHONY: help
help: ## prints this help output
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: frontend-install
frontend-install: ## install the frontend
	@npm --prefix frontend install

.PHONY: frontend-clean
frontend-clean: ## clean the frontend
	@npm --prefix frontend cache clean --force

.PHONY: frontend-lint
frontend-lint: ## lint the frontend
	@npm --prefix frontend run lint

.PHONY: frontend-test
frontend-test: ## test the frontend
	@npm --prefix frontend run test

.PHONY: frontend-build
frontend-build: ## build the frontend
	@npm --prefix frontend run build

.PHONY: frontend-run
frontend-run: ## run the frontend
	@npm --prefix frontend run start

.PHONY: backend-install
backend-install: ## install the backend
	@if [ ! -n "$(VIRTUAL_ENV)" == ""]; then \
		if [ ! -n "backend/.venv"]; then \
			uv venv .venv --python 3.13; \
		fi; \
		source backend/.venv/bin/activate; \
	fi
	@uv pip install -r backend/pyproject.toml
	@uv pip install -e backend/.

.PHONY: backend-lint
backend-lint: ## lint the backend
	@python -m flake8 backend --exclude .venv --max-line-length 120

.PHONY: backend-test
backend-test: ## test the backend
	@python -m pytest backend/tests -svv

.PHONY: backend-run-agent
backend-run-agent: ## run the backend agents in adk web ui
	@adk web backend/internal/agents/vertex/subagents

.PHONY: backend-run-service
backend-run-service: ## run the backend service
	@python backend/commands/service.py run

.PHONY: backend-build-service
backend-build-service: ## build the backend service, optionally save as a .tar
	@docker build $(BUILD_ARGS) -t backend ./backend
	@if [ -n "$(OUTPUT)" ]; then \
		docker save backend -o $(OUTPUT); \
	fi

# TODO: Might just be an issue with my local machine, but unable to run `gcloud` directly
.PHONY: backend-proxy-service
backend-proxy-service: ## run a proxy to the backend service
	@~/google-cloud-sdk/bin/gcloud run services proxy backend --project $(GCP_PROJECT_ID) --region $(GCP_PROJECT_REGION)
