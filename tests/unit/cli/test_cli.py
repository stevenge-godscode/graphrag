import pytest
from pathlib import Path
from dotenv import load_dotenv  # 用于加载 .env
from graphrag.cli.prompt_tune import prompt_tune
from graphrag.cli.main import  _prompt_tune_cli, _index_cli

# 解析根目录
root_dir = Path("/Users/stevenge/repositories/genesis-graphrag/projects/deepseek")
config_filepath = root_dir / "settings.yaml"

# 加载 .env 文件
env_path = root_dir / ".env"
if env_path.exists():
    load_dotenv(env_path)
else:
    print(f"警告: {env_path} 文件不存在，可能会影响配置加载。")

@pytest.mark.timeout(3600)  # 设置 3000 秒超时
def test_run_prompt_tune():
    # 设置测试参数
    output_path = root_dir / "prompts"


    _prompt_tune_cli(
       root=root_dir, output=output_path
    )

@pytest.mark.timeout(3600)  # 设置 3000 秒超时
def test_run_index():
    # 设置测试参数
    output_path = root_dir / "output"


    _index_cli(
       root=root_dir, output=output_path, cache=False
    )