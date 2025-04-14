import json
import os
from pathlib import Path

def convert_json(input_path, output_root, source_type):
    """将 JSON 转换为 .list 格式，并保留目录结构"""
    with open(input_path, 'r') as f:
        data = json.load(f)
    
    lines = []
    for rule in data.get("rules", []):
        for domain in rule.get("domain", []):
            lines.append(f"DOMAIN,{domain}")
        for suffix in rule.get("domain_suffix", []):
            lines.append(f"DOMAIN-SUFFIX,{suffix}")
    
    # 构建输出路径（保留源目录结构）
    relative_path = input_path.relative_to(f"source-repo/{source_type}/geosite")
    output_path = output_root / source_type / relative_path.with_suffix(".list")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        f.write("\n".join(lines))

def main():
    repo_dir = Path("source-repo")
    output_dir = Path("processed-rules")
    
    # 定义需要处理的路径映射
    process_paths = {
        "geo": repo_dir / "geo/geosite",
        "geo-lite": repo_dir / "geo-lite/geosite"
    }

    for source_type, source_path in process_paths.items():
        for json_file in source_path.glob("**/*.json"):
            convert_json(json_file, output_dir, source_type)
            print(f"Converted [{source_type}]: {json_file}")

if __name__ == "__main__":
    main()
