#!/usr/bin/env python3
"""
Lightweight TCP Proxy for API Statistics
只记录请求目标，不解密 SSL 内容
"""

import asyncio
import json
import sqlite3
import time
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import Optional
import logging

# 尝试使用 rich 库
try:
    from rich.console import Console
    from rich.table import Table
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class ConnectionRecord:
    """连接记录"""
    timestamp: str
    target_host: str
    target_port: int
    client_ip: str
    connect_time: float

    def to_dict(self):
        return {
            'timestamp': self.timestamp,
            'target_host': self.target_host,
            'target_port': self.target_port,
            'client_ip': self.client_ip,
            'connect_time': self.connect_time,
        }


class StatsDatabase:
    """统计数据库"""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS connections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                target_host TEXT NOT NULL,
                target_port INTEGER NOT NULL,
                client_ip TEXT,
                connect_time REAL
            )
        ''')
        c.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON connections(timestamp)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_host ON connections(target_host)')
        conn.commit()
        conn.close()

    def record(self, record: ConnectionRecord):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            INSERT INTO connections (timestamp, target_host, target_port, client_ip, connect_time)
            VALUES (?, ?, ?, ?, ?)
        ''', (record.timestamp, record.target_host, record.target_port,
              record.client_ip, record.connect_time))
        conn.commit()
        conn.close()

    def get_stats(self, since_hours: int = 24) -> dict:
        """获取统计数据"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        since_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

        # 按主机统计
        c.execute('''
            SELECT target_host, COUNT(*) as count
            FROM connections
            WHERE timestamp >= datetime('now', ?)
            GROUP BY target_host
            ORDER BY count DESC
        ''', (f'-{since_hours} hours',))

        host_stats = {}
        for row in c.fetchall():
            host_stats[row[0]] = {'count': row[1]}

        conn.close()
        return host_stats


class TCPProxy:
    """轻量 TCP 代理"""

    def __init__(self, listen_port: int = 8080, db_path: Path = None):
        self.listen_port = listen_port
        self.db = StatsDatabase(db_path or Path.home() / '.claude' / 'proxy_stats.db')
        self.running = False

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """处理客户端连接"""
        client_ip = writer.get_extra_info('peername')[0] if writer.get_extra_info('peername') else 'unknown'
        start_time = time.time()

        try:
            # 读取 CONNECT 请求（如果是 HTTPS 代理）
            first_line = await reader.readline()
            first_line_str = first_line.decode('utf-8', errors='ignore').strip()

            target_host = None
            target_port = None

            # 解析 CONNECT 请求
            if first_line_str.startswith('CONNECT'):
                parts = first_line_str.split()
                if len(parts) >= 2:
                    target = parts[1]
                    if ':' in target:
                        target_host, target_port = target.rsplit(':', 1)
                        target_port = int(target_port)

            if target_host and target_port:
                # 记录连接
                record = ConnectionRecord(
                    timestamp=datetime.now().isoformat(),
                    target_host=target_host,
                    target_port=target_port,
                    client_ip=client_ip,
                    connect_time=time.time() - start_time
                )
                self.db.record(record)
                logger.info(f"Connect: {target_host}:{target_port}")

                # 发送 200 Connection Established
                writer.write(b'HTTP/1.1 200 Connection Established\r\n\r\n')
                await writer.drain()

                # 连接到目标服务器
                try:
                    target_reader, target_writer = await asyncio.open_connection(
                        target_host, target_port
                    )

                    # 双向转发数据
                    async def forward(src, dst):
                        try:
                            while True:
                                data = await src.read(4096)
                                if not data:
                                    break
                                dst.write(data)
                                await dst.drain()
                        except (ConnectionResetError, BrokenPipeError):
                            pass
                        finally:
                            try:
                                dst.close()
                                await dst.wait_closed()
                            except:
                                pass

                    # 并行转发
                    await asyncio.gather(
                        forward(reader, target_reader),
                        forward(target_reader, writer),
                        return_exceptions=True
                    )
                except Exception as e:
                    logger.error(f"Target connection failed: {e}")
            else:
                # 不是 CONNECT 请求，返回错误
                writer.write(b'HTTP/1.1 400 Bad Request\r\n\r\nOnly CONNECT method supported')
                await writer.drain()

        except Exception as e:
            logger.error(f"Error handling client: {e}")
        finally:
            try:
                writer.close()
                await writer.wait_closed()
            except:
                pass

    async def start(self):
        """启动代理服务器"""
        self.running = True
        server = await asyncio.start_server(
            self.handle_client,
            '127.0.0.1',
            self.listen_port
        )

        addr = server.sockets[0].getsockname()
        logger.info(f"Proxy listening on {addr[0]}:{addr[1]}")
        logger.info(f"Set environment: export HTTPS_PROXY=http://{addr[0]}:{addr[1]}")

        async with server:
            while self.running:
                await asyncio.sleep(1)

    def stop(self):
        self.running = False


def print_stats(stats: dict, title: str = "Proxy Statistics"):
    """打印统计结果"""
    if not stats:
        print("No data yet.")
        return

    sorted_hosts = sorted(stats.items(), key=lambda x: x[1]['count'], reverse=True)
    total = sum(d['count'] for _, d in sorted_hosts)

    if HAS_RICH:
        console = Console()
        table = Table(title=title, show_header=True, header_style="bold cyan")
        table.add_column("Target Host", style="green", width=50)
        table.add_column("Requests", justify="right", style="yellow", width=12)

        for host, data in sorted_hosts:
            table.add_row(host, f"{data['count']:,}")

        table.add_row("[bold]TOTAL[/bold]", f"[bold]{total:,}[/bold]")
        console.print(table)
    else:
        print("=" * 65)
        print(f"{'Target Host':<50} {'Requests':>12}")
        print("=" * 65)

        for host, data in sorted_hosts:
            print(f"{host:<50} {data['count']:>12,}")

        print("=" * 65)
        print(f"{'TOTAL':<50} {total:>12,}")
        print("=" * 65)


async def main():
    import argparse

    parser = argparse.ArgumentParser(description='API Stats TCP Proxy')
    parser.add_argument('--start', action='store_true', help='Start proxy server')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    parser.add_argument('--port', type=int, default=8080, help='Proxy port')
    parser.add_argument('--hours', type=int, default=24, help='Stats: last N hours')

    args = parser.parse_args()

    db_path = Path.home() / '.claude' / 'proxy_stats.db'

    if args.stats:
        db = StatsDatabase(db_path)
        stats = db.get_stats(since_hours=args.hours)
        title = f"Proxy Statistics (Last {args.hours} hours)"
        print_stats(stats, title=title)
    elif args.start:
        proxy = TCPProxy(listen_port=args.port, db_path=db_path)
        try:
            await proxy.start()
        except KeyboardInterrupt:
            print("\nShutting down...")
    else:
        parser.print_help()


if __name__ == '__main__':
    asyncio.run(main())
