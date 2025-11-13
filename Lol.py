#!/usr/bin/env python3
import os
import re
import sys
import argparse

ALLOWED_REPO_MODES = {"local", "remote"}

def is_url(s: str) -> bool:
    return bool(re.match(r"^(https?://|git@[\w\.-]+:).+", s or ""))

def validate_repo(repo: str, mode: str) -> None:
    if mode not in ALLOWED_REPO_MODES:
        raise ValueError(f"repo_mode: must be one of {sorted(ALLOWED_REPO_MODES)}")
    if mode == "remote":
        if not is_url(repo):
            raise ValueError("repo: expected URL (http(s):// or git@...) for repo_mode=remote")
    else:  # local
        if is_url(repo):
            raise ValueError("repo: got URL but repo_mode=local expects filesystem path")
        if not os.path.exists(repo):
            raise ValueError(f"repo: path does not exist: {repo}")

def parse_args():
    parser = argparse.ArgumentParser(description="Dependency graph visualizer prototype")

    parser.add_argument("--package", required=True, help="Имя анализируемого пакета")
    parser.add_argument("--repo", required=True, help="URL-адрес или путь к тестовому репозиторию")
    parser.add_argument("--repo_mode", required=True, choices=ALLOWED_REPO_MODES,
                        help="Режим работы с тестовым репозиторием: local или remote")
    parser.add_argument("--output", required=True, help="Имя файла с изображением графа")
    parser.add_argument("--filter", required=False, default="", help="Подстрока для фильтрации пакетов")

    return parser.parse_args()

def main():
    try:
        args = parse_args()
        validate_repo(args.repo, args.repo_mode)

        # Вывод всех параметров в формате ключ=значение
        params = {
            "package": args.package,
            "repo": args.repo,
            "repo_mode": args.repo_mode,
            "output": args.output,
            "filter": args.filter,
        }
        for k, v in params.items():
            print(f"{k}={v}")

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
