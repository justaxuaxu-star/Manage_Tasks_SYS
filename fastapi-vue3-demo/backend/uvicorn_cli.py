import os
import subprocess
import sys
from pathlib import Path


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _venv_python() -> Path | None:
    path = _project_root() / "venv" / "Scripts" / "python.exe"
    return path if path.is_file() else None


def _in_project_venv() -> bool:
    venv_python = _venv_python()
    if venv_python is None:
        return False
    try:
        return Path(sys.executable).resolve() == venv_python.resolve()
    except OSError:
        return False


def _load_port() -> str:
    env_file = _project_root() / ".env"
    if env_file.is_file():
        from dotenv import load_dotenv

        load_dotenv(env_file)
    return os.getenv("API_PORT", "8001")


def _with_default_port(argv: list[str]) -> list[str]:
    has_port = any(arg == "--port" or arg.startswith("--port=") for arg in argv)
    if has_port:
        return argv
    return ["--port", _load_port(), *argv]


def _run_uvicorn_in_current_python(argv: list[str]) -> None:
    sys.argv = ["uvicorn", *argv]
    try:
        from uvicorn.main import main as uvicorn_main
    except ModuleNotFoundError:
        print("当前 Python 环境未安装 uvicorn。")
        print("请确认 fastapi-vue3-demo/venv 已创建，并执行：")
        print(r"  .\venv\Scripts\python.exe -m pip install fastapi uvicorn sqlalchemy pydantic python-dotenv psycopg[binary]")
        raise SystemExit(1) from None
    uvicorn_main()


def main() -> None:
    argv = _with_default_port(sys.argv[1:])
    root = _project_root()

    if _in_project_venv() or os.getenv("VIRTUAL_ENV"):
        os.chdir(root)
        _run_uvicorn_in_current_python(argv)
        return

    venv_python = _venv_python()
    if venv_python is not None:
        raise SystemExit(
            subprocess.call(
                [str(venv_python), "-m", "uvicorn", *argv],
                cwd=root,
            )
        )

    print("未找到项目虚拟环境：fastapi-vue3-demo/venv")
    print("请先执行：")
    print("  python -m venv venv")
    print(r"  .\venv\Scripts\python.exe -m pip install fastapi uvicorn sqlalchemy pydantic python-dotenv psycopg[binary]")
    raise SystemExit(1)


if __name__ == "__main__":
    main()