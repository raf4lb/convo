import subprocess
import sys


def main():
    try:
        subprocess.run(
            ["uv", "run", "uvicorn", "src.web.framework.app:app", "--reload"],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        sys.exit(1)


if __name__ == "__main__":
    main()
