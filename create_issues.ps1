# Script to create GitHub issues for lisa-agentic
# Run this script in a terminal where 'gh' is installed and authenticated.

Write-Host "Creating Issue 1: Implement Docker Sandboxing..."
gh issue create --title "[Security] Implement Docker Sandboxing for Code Execution" --body "### Description`nCurrently, tools/executor.py executes generated Python code directly on the host machine using subprocess.run. This poses a significant security risk.`n`n### Proposed Solution`nRefactor executor.py to run code inside an isolated Docker container.`n`n### Acceptance Criteria`n- [ ] Code execution happens inside a container.`n- [ ] Host file system is inaccessible." --label "security,enhancement"

Write-Host "Creating Issue 2: Consolidate Frontend Strategy..."
gh issue create --title "[Architecture] Consolidate Frontend Strategy" --body "### Description`nThe project contains two frontends: Streamlit (app.py) and Next.js (frontend/). This creates confusion.`n`n### Proposed Solution`nDecide on a single frontend. Deprecate the other.`n`n### Acceptance Criteria`n- [ ] One frontend direction is chosen.`n- [ ] Unused code is archived/removed." --label "architecture,discussion"

Write-Host "Creating Issue 3: Implement Robust Database Layer..."
gh issue create --title "[Backend] Implement Robust Database Layer" --body "### Description`nCurrent persistence is ad-hoc SQLite. Needs an ORM for robustness and migrations.`n`n### Proposed Solution`nIntegrate SQLAlchemy or Prisma.`n`n### Acceptance Criteria`n- [ ] ORM installed and configured.`n- [ ] Schema allows for migrations." --label "backend,enhancement"

Write-Host "Creating Issue 4: Add Comprehensive Tests..."
gh issue create --title "[Quality] Add Comprehensive Unit & Integration Tests" --body "### Description`nTest coverage is minimal.`n`n### Proposed Solution`nAdd unit tests for tools and integration tests for agent flows.`n`n### Acceptance Criteria`n- [ ] pytest runs with high coverage.`n- [ ] Critical paths covered." --label "testing,quality"

Write-Host "All issues created successfully!"
