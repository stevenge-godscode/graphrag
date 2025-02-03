import pytest
import os
from pathlib import Path
from dotenv import load_dotenv  # 用于加载 .env
from graphrag.cli.query import run_global_search

# 解析根目录
root_dir = Path("/Users/stevenge/repositories/genesis-graphrag/genesis-fintech-public-report")

# 加载 .env 文件
env_path = root_dir / ".env"
if env_path.exists():
    load_dotenv(env_path)
else:
    print(f"警告: {env_path} 文件不存在，可能会影响配置加载。")

@pytest.mark.timeout(3600)  # 设置 3000 秒超时
def test_run_global_search():
    # 设置测试参数
    config_filepath = root_dir / "settings.yaml"
    data_dir = root_dir / "output"
    community_level = 1
    dynamic_community_selection = True
    response_type = "Multi-Page Report"
    streaming = False
    query = "2025年，AI行业的投资机会有哪些？"

    # 调用搜索函数
    response, context_data = run_global_search(
        config_filepath=config_filepath,
        data_dir=data_dir,
        root_dir=root_dir,
        community_level=community_level,
        dynamic_community_selection=dynamic_community_selection,
        response_type=response_type,
        streaming=streaming,
        query=query,
    )

    # print(response)
    print(context_data)
    # 断言返回值是否符合预期
    assert response is not None
    assert isinstance(response, str)