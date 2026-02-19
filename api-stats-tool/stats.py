#!/usr/bin/env python3
"""
Claude Code API Usage Statistics Tool
从本地 session 文件中提取和分析 API 使用统计
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Optional
import argparse


class APIStatsAnalyzer:
    def __init__(self, claude_dir: Path = None):
        self.claude_dir = claude_dir or Path.home() / ".claude"
        self.projects_dir = self.claude_dir / "projects"

    def find_session_files(self, since_date: Optional[datetime] = None) -> List[Path]:
        """查找所有 session jsonl 文件"""
        files = []
        for jsonl_file in self.projects_dir.rglob("*.jsonl"):
            if since_date:
                mtime = datetime.fromtimestamp(jsonl_file.stat().st_mtime)
                if mtime < since_date:
                    continue
            files.append(jsonl_file)
        return files

    def parse_session_file(self, file_path: Path) -> List[Dict]:
        """解析单个 session 文件，提取 API 使用记录"""
        records = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        data = json.loads(line.strip())
                        if data.get('type') == 'assistant' and data.get('message', {}).get('usage'):
                            usage = data['message']['usage']
                            # 只统计有实际 token 消耗的请求
                            if usage.get('input_tokens', 0) > 0:
                                records.append({
                                    'model': data['message'].get('model', 'unknown'),
                                    'timestamp': data.get('timestamp'),
                                    'input_tokens': usage.get('input_tokens', 0),
                                    'output_tokens': usage.get('output_tokens', 0),
                                    'cache_read_tokens': usage.get('cache_read_input_tokens', 0),
                                    'cache_creation_tokens': usage.get('cache_creation_input_tokens', 0),
                                })
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            print(f"Error reading {file_path}: {e}", file=sys.stderr)
        return records

    def aggregate_stats(self, records: List[Dict]) -> Dict:
        """聚合统计数据"""
        stats = defaultdict(lambda: {
            'count': 0,
            'input_tokens': 0,
            'output_tokens': 0,
            'cache_read_tokens': 0,
            'cache_creation_tokens': 0,
        })

        for record in records:
            model = record['model']
            stats[model]['count'] += 1
            stats[model]['input_tokens'] += record['input_tokens']
            stats[model]['output_tokens'] += record['output_tokens']
            stats[model]['cache_read_tokens'] += record['cache_read_tokens']
            stats[model]['cache_creation_tokens'] += record['cache_creation_tokens']

        return dict(stats)

    def analyze(self, days: Optional[int] = None) -> Dict:
        """分析 API 使用统计"""
        since_date = None
        if days:
            since_date = datetime.now() - timedelta(days=days)

        print(f"Scanning session files...", file=sys.stderr)
        files = self.find_session_files(since_date)
        print(f"Found {len(files)} session files", file=sys.stderr)

        all_records = []
        for file_path in files:
            records = self.parse_session_file(file_path)
            all_records.extend(records)

        print(f"Extracted {len(all_records)} API records", file=sys.stderr)

        return self.aggregate_stats(all_records)


def format_number(n: int) -> str:
    """格式化数字，添加千位分隔符"""
    return f"{n:,}"


def print_stats_table(stats: Dict):
    """打印统计表格"""
    if not stats:
        print("No API usage data found.")
        return

    # 表头
    print("=" * 100)
    print(f"{'Model':<30} {'Requests':>10} {'Input Tokens':>15} {'Output Tokens':>15} {'Cache Read':>15}")
    print("=" * 100)

    # 按请求次数排序
    sorted_models = sorted(stats.items(), key=lambda x: x[1]['count'], reverse=True)

    total_count = 0
    total_input = 0
    total_output = 0
    total_cache = 0

    for model, data in sorted_models:
        print(f"{model:<30} {data['count']:>10} {format_number(data['input_tokens']):>15} "
              f"{format_number(data['output_tokens']):>15} {format_number(data['cache_read_tokens']):>15}")
        total_count += data['count']
        total_input += data['input_tokens']
        total_output += data['output_tokens']
        total_cache += data['cache_read_tokens']

    print("=" * 100)
    print(f"{'TOTAL':<30} {total_count:>10} {format_number(total_input):>15} "
          f"{format_number(total_output):>15} {format_number(total_cache):>15}")
    print("=" * 100)


def main():
    parser = argparse.ArgumentParser(description='Claude Code API Usage Statistics')
    parser.add_argument('--days', type=int, help='Only analyze last N days')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--model', type=str, help='Filter by model name')

    args = parser.parse_args()

    analyzer = APIStatsAnalyzer()
    stats = analyzer.analyze(days=args.days)

    # 按模型过滤
    if args.model:
        stats = {k: v for k, v in stats.items() if args.model.lower() in k.lower()}

    if args.json:
        print(json.dumps(stats, indent=2))
    else:
        if args.days:
            print(f"\nAPI Usage Statistics (Last {args.days} days)\n")
        else:
            print(f"\nAPI Usage Statistics (All Time)\n")
        print_stats_table(stats)


if __name__ == '__main__':
    main()
