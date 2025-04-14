import json
import os
from pathlib import Path

def convert_rules():
    CONFIG = {
        "geoip": {
            "fields": ["ip_cidr", "cidrs"],
            "prefix": "IP-CIDR"
        },
        "geosite": {
            "fields": ["domains", "domain"],
            "prefix": "DOMAIN"
        }
    }

    # 修改路径配置：直接使用 geo 和 geo-lite 作为根目录
    base_dirs = {
        "geo": ["geoip", "geosite"],
        "geo-lite": ["geoip", "geosite"]
    }

    for category, data_types in base_dirs.items():
        for data_type in data_types:
            config = CONFIG.get(data_type, {})
            if not config:
                continue

            # 输入路径保持不变
            src_dir = Path(f"source-repo/{category}/{data_type}")
            if not src_dir.exists():
                print(f"⚠️ 源目录不存在: {src_dir}")
                continue

            # 调整输出路径：直接在根目录下生成 geo/ geo-lite/
            output_dir = Path(category) / data_type  # 关键修改点
            output_dir.mkdir(parents=True, exist_ok=True)

            for json_file in src_dir.glob("*.json"):
                list_file = output_dir / f"{json_file.stem}.list"
                print(f"🔄 转换 {data_type} 规则: {json_file.name}")

                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    entries = []
                    for rule in data.get("rules", []):
                        for field in config["fields"]:
                            entries.extend(rule.get(field, []))

                    # 添加去重和排序逻辑
                    unique_entries = sorted(list(set(entries)))

                    with open(list_file, 'w', encoding='utf-8') as f:
                        for entry in unique_entries:
                            f.write(f"{config['prefix']},{entry}\n")

                    print(f"✅ 生成 {len(unique_entries)} 条 {data_type.upper()} 规则")

                except Exception as e:
                    print(f"❌ 转换失败: {str(e)}")
                    if list_file.exists():
                        list_file.unlink()

if __name__ == "__main__":
    print("=== 开始转换规则 ===")
    convert_rules()
    print("=== 全部转换完成 ===")
