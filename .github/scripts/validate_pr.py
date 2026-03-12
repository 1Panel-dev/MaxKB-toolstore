import sys
import os
import yaml
import re

VALID_PREFIXES = ['tool_', 'app_', 'db_', 'kbwf_']
REQUIRED_YAML_FIELDS = ['name', 'tags', 'title', 'description']
VERSION_RE = re.compile(r'^\d+\.\d+\.\d+$')

# 每种前缀允许的文件扩展名
PREFIX_EXT = {
    'app_':  '.mk',
    'db_':   '.tool',
    'tool_': '.tool',
    'kbwf_': '.kbwf',
}

errors = []
warnings = []

def check(cond, msg, is_warn=False):
    if not cond:
        (warnings if is_warn else errors).append(msg)

def get_valid_tags():
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..')
    yaml_path = os.path.join(root, 'tools/data.yaml')
    if not os.path.isfile(yaml_path):
        print(f"⚠️  未找到 tools/data.yaml，跳过 tags 校验")
        return set()
    try:
        with open(yaml_path, encoding='utf-8') as f:
            data = yaml.safe_load(f)
        tags = data.get('additionalProperties', {}).get('tags', [])
        return {tag['name'] for tag in tags if 'name' in tag}
    except yaml.YAMLError as e:
        print(f"⚠️  tools/data.yaml 解析失败: {e}")
        return set()

def get_changed_tool_dirs(changed_files_path):
    dirs = set()
    with open(changed_files_path) as f:
        for line in f:
            parts = line.strip().split('/')
            if len(parts) >= 2 and parts[0] == 'tools':
                tool_dir = parts[1]
                if any(tool_dir.startswith(p) for p in VALID_PREFIXES):
                    dirs.add(os.path.join('tools', tool_dir))
    return dirs

def get_prefix(tool_name):
    for p in VALID_PREFIXES:
        if tool_name.startswith(p):
            return p
    return None

def validate_tool_dir(tool_path, valid_tags):
    tool_name = os.path.basename(tool_path)
    print(f"\n🔍 校验: {tool_path}")

    # 1. 目录前缀校验
    prefix = get_prefix(tool_name)
    check(prefix is not None,
          f"[{tool_name}] 目录名前缀无效，必须以 {VALID_PREFIXES} 之一开头")
    if prefix is None:
        return

    # 2. 根目录必要文件校验
    for fname in ['data.yaml', 'logo.png', 'README.md']:
        check(
            os.path.isfile(os.path.join(tool_path, fname)),
            f"[{tool_name}] 缺少必要文件: {fname}"
        )

    # 3. 至少一个版本目录
    if not os.path.isdir(tool_path):
        check(False, f"[{tool_name}] 工具目录不存在")
        return

    version_dirs = [
        d for d in os.listdir(tool_path)
        if os.path.isdir(os.path.join(tool_path, d)) and VERSION_RE.match(d)
    ]
    check(len(version_dirs) > 0, f"[{tool_name}] 缺少版本目录（如 1.0.0）")

    # 4. 每个版本目录校验
    expected_ext = PREFIX_EXT[prefix]
    for version in version_dirs:
        version_path = os.path.join(tool_path, version)
        files_in_version = os.listdir(version_path)

        # 4.1 只能有一个对应扩展名的文件
        matched = [f for f in files_in_version if f.endswith(expected_ext)]
        check(
            len(matched) == 1,
            f"[{tool_name}/{version}] 版本目录下应有且仅有 1 个 {expected_ext} 文件，"
            f"当前找到 {len(matched)} 个: {matched}"
        )

        # 4.2 版本目录下不应有其他多余文件
        extra = [f for f in files_in_version if not f.endswith(expected_ext)]
        check(
            len(extra) == 0,
            f"[{tool_name}/{version}] 版本目录下存在多余文件: {extra}",
            is_warn=True
        )

    # 5. data.yaml 内容校验
    yaml_path = os.path.join(tool_path, 'data.yaml')
    if os.path.isfile(yaml_path):
        try:
            with open(yaml_path, encoding='utf-8') as f:
                data = yaml.safe_load(f)
            for field in REQUIRED_YAML_FIELDS:
                check(
                    field in data and data[field],
                    f"[{tool_name}] data.yaml 缺少字段或为空: {field}"
                )
            if valid_tags and 'tags' in data and isinstance(data['tags'], list):
                for tag in data['tags']:
                    check(
                        tag in valid_tags,
                        f"[{tool_name}] data.yaml 中 tag '{tag}' 未在 tools/data.yaml 中定义，"
                        f"可选值: {sorted(valid_tags)}"
                    )
        except yaml.YAMLError as e:
            errors.append(f"[{tool_name}] data.yaml 解析失败: {e}")

    # 6. README.md 非空
    readme_path = os.path.join(tool_path, 'README.md')
    if os.path.isfile(readme_path):
        content = open(readme_path, encoding='utf-8').read().strip()
        check(len(content) > 50, f"[{tool_name}] README.md 内容过少，请补充工具说明")
        if tool_name.startswith('tool_') or tool_name.startswith('db_'):
            check(
                '参数' in content or 'parameter' in content.lower(),
                f"[{tool_name}] README.md 建议包含参数说明",
                is_warn=True
            )

    # 7. logo.png 大小
    logo_path = os.path.join(tool_path, 'logo.png')
    if os.path.isfile(logo_path):
        size_kb = os.path.getsize(logo_path) / 1024
        check(size_kb <= 500,
              f"[{tool_name}] logo.png 过大 ({size_kb:.1f}KB)，建议不超过 500KB",
              is_warn=True)

def main():
    changed_files_path = sys.argv[1]
    valid_tags = get_valid_tags()
    tool_dirs = get_changed_tool_dirs(changed_files_path)

    if not tool_dirs:
        print("ℹ️  本次 PR 未涉及 tools/ 目录下的工具，跳过校验。")
        sys.exit(0)

    print(f"本次 PR 涉及 {len(tool_dirs)} 个工具目录：")
    for d in sorted(tool_dirs):
        validate_tool_dir(d, valid_tags)

    print("\n" + "=" * 50)
    if warnings:
        print(f"⚠️  警告 ({len(warnings)} 条):")
        for w in warnings:
            print(f"  - {w}")

    if errors:
        print(f"\n❌ 错误 ({len(errors)} 条):")
        for e in errors:
            print(f"  - {e}")
        print("\n请修复以上问题后重新提交 PR。")
        sys.exit(1)
    else:
        print("✅ 所有校验通过！")
        sys.exit(0)

if __name__ == '__main__':
    main()
