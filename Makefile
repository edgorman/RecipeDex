.PHONY: help
help: ## prints this help output
	@if [ "$(MAKECMDGOALS)" = "help" ]; then \
		grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'; \
	fi

.PHONY: backend
backend: ## run backend commands
	@$(MAKE) --no-print-directory -C $(MAKECMDGOALS)

.PHONY: frontend
frontend: ## run frontend commands
	@$(MAKE) --no-print-directory -C $(MAKECMDGOALS)

.PHONY: infrastructure
infrastructure: ## run infrastructure commands
	@$(MAKE) --no-print-directory -C $(MAKECMDGOALS)`

# stops processing any additional commands
%:
	@:
