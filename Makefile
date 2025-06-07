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
	@python -m pip install -r backend/requirements.txt
	@python -m pip install -e backend/.

.PHONY: backend-lint
backend-lint: ## lint the backend
	@python -m flake8 backend/. --exclude .venv

.PHONY: backend-test
backend-test: ## test the backend
	@python -m pytest backend/tests -svv

.PHONY: backend-run-agent
backend-run-agent: ## run the backend agents
	@adk web backend/internal
