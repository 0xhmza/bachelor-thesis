#!/bin/sh
# Install the project's git hooks. Run once per clone:  sh scripts/hooks/install.sh
# Each installed hook is a one-line shim, so later changes to scripts/hooks/
# take effect without reinstalling.
set -e
cd "$(git rev-parse --show-toplevel)"
hooks=$(git rev-parse --git-path hooks)
for name in pre-commit; do
    target="$hooks/$name"
    if [ -e "$target" ] && ! grep -q 'scripts/hooks/' "$target"; then
        echo "skip $name: $target exists and is not ours" >&2
        continue
    fi
    printf '#!/bin/sh\nexec sh scripts/hooks/%s "$@"\n' "$name" > "$target"
    chmod +x "$target"
    echo "installed $target"
done
