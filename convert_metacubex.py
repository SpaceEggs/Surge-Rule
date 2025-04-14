import json
import os
from pathlib import Path

def convert_geoip_rules():
    # 配置路径参数
    base_dirs = {
        "geo": "source-repo/geo/geoip",
        "geo-lite": "source-repo/geo-lite/geoip"
    }
    output_root = Path("processed-rules")

    # 遍历所有源目录
    for category, src_dir in base_dirs.items():
        src_path = Path(src_dir)
        if not src_path.exists():
            print(f"⚠️ 源目录不存在: {src_path}")
            continue

        # 创建输出目录 processed-rules/[category]/geoip
        output_dir = output_root / category / "geoip"
        output_dir.mkdir(parents=True, exist_ok=True)

        # 处理所有 JSON 文件
        for json_file in src_path.glob("*.json"):
            # 生成对应的 .list 输出路径
            list_file = output_dir / f"{json_file.stem}.list"
            
            print(f"🔄 转换中: {json_file} → {list_file}")
            
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 提取所有 CIDR 规则
                cidrs = []
                for rule in data.get("rules", []):
                    cidrs.extend(rule.get("ip_cidr", []))
                
                # 写入 .list 文件
                with open(list_file, 'w', encoding='utf-8') as f:
                    for cidr in cidrs:
                        f.write(f"IP-CIDR,{cidr}\n")
                
                print(f"✅ 生成 {len(cidrs)} 条规则")
                
            except Exception as e:
                print(f"❌ 处理失败: {json_file} - {str(e)}")

if __name__ == "__main__":
    print("=== 开始转换 GeoIP 规则 ===")
    convert_geoip_rules()
    print("=== 转换完成 ===")
