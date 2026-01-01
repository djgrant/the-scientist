# /update-scientist

Update the-scientist to the latest version from the remote repository.

## Instructions

### 1. Locate the-scientist Installation

Check these locations for a git repository with a matching remote:

1. `$OPENCODE_CONFIG_DIR` (if set)
2. `~/.config/opencode/`

For each location, verify it's the-scientist by checking if the git remote URL contains `djgrant/the-scientist`.

If no valid installation is found, the update cannot be completed.

### 2. Check Repository Status

For the identified location, get the latest remote state and check for local modifications.

### 3. Propose a Plan

Present the user with a clear summary and proposed action. Wait for user confirmation before making any changes.

### 4. Execute the Update

After user confirms, execute the agreed strategy to incorporate remote changes into the local repository.

### 5. Check for New Dependencies

After updating, check if new dependencies were added by reviewing changes to `command/init-scientist.md`. If new dependencies are detected, suggest running `/init-scientist` to install them.
