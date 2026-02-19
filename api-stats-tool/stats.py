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

# 尝试使用 rich 库，如果不可用则使用简单表格
try:
    from rich.console import Console
    from rich.table import Table
    from rich import print as rprint
    HAS_RICH = True
except ImportError:
    HAS_RICH = False


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


def format_tokens(n: int) -> str:
    """格式化 token 数量为易读格式"""
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    elif n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(n)


def print_stats_table(stats: Dict, title: str = "API Usage Statistics"):
    """打印统计表格"""
    if not stats:
        print("No API usage data found.")
        return

    # 按请求次数排序
    sorted_models = sorted(stats.items(), key=lambda x: x[1]['count'], reverse=True)

    total_count = 0
    total_input = 0
    total_output = 0
    total_cache = 0

    if HAS_RICH:
        console = Console()
        table = Table(title=title, show_header=True, header_style="bold cyan")
        table.add_column("Model", style="green", width=30)
        table.add_column("Requests", justify="right", style="yellow")
        table.add_column("Input", justify="right", style="blue")
        table.add_column("Output", justify="right", style="magenta")
        table.add_column("Cache Read", justify="right", style="cyan")

        for model, data in sorted_models:
            table.add_row(
                model,
                format_number(data['count']),
                format_tokens(data['input_tokens']),
                format_tokens(data['output_tokens']),
                format_tokens(data['cache_read_tokens'])
            )
            total_count += data['count']
            total_input += data['input_tokens']
            total_output += data['output_tokens']
            total_cache += data['cache_read_tokens']

        # 添加总计行
        table.add_row(
            "[bold]TOTAL[/bold]",
            f"[bold]{format_number(total_count)}[/bold]",
            f"[bold]{format_tokens(total_input)}[/bold]",
            f"[bold]{format_tokens(total_output)}[/bold]",
            f"[bold]{format_tokens(total_cache)}[/bold]"
        )

        console.print(table)
    else:
        # 简单表格格式
        print("=" * 90)
        print(f"{'Model':<30} {'Requests':>10} {'Input':>12} {'Output':>12} {'Cache':>12}")
        print("=" * 90)

        for model, data in sorted_models:
            print(f"{model:<30} {data['count']:>10} {format_tokens(data['input_tokens']):>12} "
                  f"{format_tokens(data['output_tokens']):>12} {format_tokens(data['cache_read_tokens']):>12}")
            total_count += data['count']
            total_input += data['input_tokens']
            total_output += data['output_tokens']
            total_cache += data['cache_read_tokens']

        print("=" * 90)
        print(f"{'TOTAL':<30} {total_count:>10} {format_tokens(total_input):>12} "
              f"{format_tokens(total_output):>12} {format_tokens(total_cache):>12}")
        print("=" * 90)


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
            title = f"API Usage Statistics (Last {args.days} days)"
        else:
            title = "API Usage Statistics (All Time)"
        print_stats_table(stats, title=title)


if __name__ == '__main__':
    main()
