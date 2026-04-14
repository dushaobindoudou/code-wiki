#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

FAILED=0

check_file() {
  local path="$1"
  if [[ -f "$path" ]]; then
    echo "[PASS] 文件存在: $path"
  else
    echo "[FAIL] 文件缺失: $path"
    FAILED=1
  fi
}

check_contains() {
  local path="$1"
  local pattern="$2"
  local label="$3"
  if rg -q "$pattern" "$path"; then
    echo "[PASS] $label"
  else
    echo "[FAIL] $label"
    FAILED=1
  fi
}

echo "== Code Wiki Release Gate =="

# 1) 核心文件完整性
check_file "README.md"
check_file "README_CN.md"
check_file "AGENT.md"
check_file "CLAUDE.md"
check_file "skills/wiki/SKILL.md"
check_file "skills/wiki-init/SKILL.md"
check_file "skills/wiki-ingest/SKILL.md"
check_file "skills/wiki-query/SKILL.md"
check_file "skills/wiki-lint/SKILL.md"
check_file "skills/wiki-insight/SKILL.md"
check_file "skills/wiki-schema/SKILL.md"

# 2) 对外文档关键能力声明
check_contains "README.md" "/wiki init" "README 包含 init 命令"
check_contains "README.md" "/wiki ingest" "README 包含 ingest 命令"
check_contains "README.md" "/wiki query" "README 包含 query 命令"
check_contains "README.md" "/wiki lint" "README 包含 lint 命令"
check_contains "README.md" "/wiki insight" "README 包含 insight 命令"
check_contains "README_CN.md" "/wiki 初始化|/wiki init" "README_CN 包含初始化命令"
check_contains "README_CN.md" "/wiki 摄取|/wiki ingest" "README_CN 包含摄取命令"
check_contains "README_CN.md" "/wiki 查询|/wiki query" "README_CN 包含查询命令"

# 3) 主技能路由能力
check_contains "skills/wiki/SKILL.md" "wiki:init" "主 Skill 路由 init"
check_contains "skills/wiki/SKILL.md" "wiki:ingest" "主 Skill 路由 ingest"
check_contains "skills/wiki/SKILL.md" "wiki:query" "主 Skill 路由 query"
check_contains "skills/wiki/SKILL.md" "wiki:lint" "主 Skill 路由 lint"
check_contains "skills/wiki/SKILL.md" "wiki:insight" "主 Skill 路由 insight"

if [[ "$FAILED" -eq 1 ]]; then
  echo
  echo "Release Gate: FAILED"
  exit 1
fi

echo
echo "Release Gate: PASSED"
