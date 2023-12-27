from dotenv import load_dotenv
from pathlib import Path


async def load_env():
    root_path = Path(__file__).parent.parent.parent
    env_path = root_path / "src" / ".env"
    try:
        load_dotenv(env_path)
    except:
        return
