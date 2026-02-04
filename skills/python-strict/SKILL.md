---
name: python-strict
description: Modern Python strict practices - type safety, elegant code, engineering standards. AUTOMATICALLY USE when writing ANY Python code (.py files), creating Python projects, or reviewing Python code.
---

# Python Strict Development

严格的现代 Python 开发实践，聚焦类型安全、代码优雅、工程规范三大支柱。

## When to Activate

- 新项目初始化
- 配置严格类型检查
- 设计 API 或领域模型
- 代码审查时检查最佳实践

---

## 支柱一：类型安全

### mypy 严格配置

```toml
[tool.mypy]
python_version = "3.12"
strict = true

# strict = true 包含：
# disallow_any_generics = true
# disallow_subclassing_any = true
# disallow_untyped_calls = true
# disallow_untyped_defs = true
# disallow_incomplete_defs = true
# check_untyped_defs = true
# disallow_untyped_decorators = true
# warn_redundant_casts = true
# warn_unused_ignores = true
# warn_return_any = true
# no_implicit_reexport = true
# strict_equality = true
# strict_concatenate = true

# 额外推荐
warn_unreachable = true
enable_error_code = ["ignore-without-code", "redundant-expr", "truthy-bool"]
```

### 高级类型模式

#### TypedDict - 固定键字典

```python
from typing import TypedDict, NotRequired

class UserResponse(TypedDict):
    id: str
    name: str
    email: str
    avatar: NotRequired[str]  # 可选键

def get_user(id: str) -> UserResponse:
    return {"id": id, "name": "Alice", "email": "alice@example.com"}
```

#### Literal - 字面量约束

```python
from typing import Literal

Status = Literal["pending", "active", "completed", "failed"]

def update_status(id: str, status: Status) -> None:
    ...

update_status("123", "active")    # ✅
update_status("123", "unknown")   # ❌ mypy 报错
```

#### Final - 常量标注

```python
from typing import Final

MAX_RETRIES: Final = 3
API_VERSION: Final[str] = "v2"

MAX_RETRIES = 5  # ❌ mypy 报错：不能重新赋值
```

#### TypeGuard / TypeIs - 类型收窄

```python
from typing import TypeGuard, TypeIs

# TypeGuard: 返回 True 时，参数被收窄为指定类型
def is_string_list(val: list[object]) -> TypeGuard[list[str]]:
    return all(isinstance(x, str) for x in val)

# TypeIs (Python 3.13+): 更精确的收窄，保留原始类型信息
def is_not_none[T](val: T | None) -> TypeIs[T]:
    return val is not None

def process(items: list[object]) -> None:
    if is_string_list(items):
        # items 现在是 list[str]
        print(items[0].upper())
```

#### @overload - 函数重载

```python
from typing import overload

@overload
def parse(data: str) -> dict[str, object]: ...
@overload
def parse(data: bytes) -> dict[str, object]: ...
@overload
def parse(data: None) -> None: ...

def parse(data: str | bytes | None) -> dict[str, object] | None:
    if data is None:
        return None
    if isinstance(data, bytes):
        data = data.decode()
    return json.loads(data)
```

### Pydantic v2 严格模式

```python
from pydantic import BaseModel, ConfigDict, Field
from typing import Literal

class User(BaseModel):
    model_config = ConfigDict(
        strict=True,           # 禁止类型强制转换
        extra="forbid",        # 禁止额外字段
        frozen=True,           # 不可变
        validate_default=True, # 验证默认值
    )

    id: str
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=0, le=150)
    status: Literal["active", "inactive"] = "active"

# ✅ 正确
user = User(id="123", name="Alice", age=30)

# ❌ strict=True 禁止类型转换
user = User(id="123", name="Alice", age="30")  # ValidationError

# ❌ extra="forbid" 禁止额外字段
user = User(id="123", name="Alice", age=30, foo="bar")  # ValidationError
```

### 常见类型错误修复

```python
# ❌ 错误：使用 Any
def process(data: Any) -> Any: ...

# ✅ 修复：使用具体类型或泛型
from typing import TypeVar
T = TypeVar("T")
def process(data: T) -> T: ...

# ❌ 错误：Optional 未处理 None
def get_name(user: User | None) -> str:
    return user.name  # 可能是 None

# ✅ 修复：显式处理 None
def get_name(user: User | None) -> str:
    if user is None:
        return "Unknown"
    return user.name

# ❌ 错误：dict 键类型不明确
config: dict = {"key": "value"}

# ✅ 修复：明确键值类型
config: dict[str, str] = {"key": "value"}
```

---

## 支柱二：代码优雅

### SOLID 原则

| 原则 | Python 实现 |
|------|-------------|
| **S** 单一职责 | 小类、小函数，每个模块一个职责 |
| **O** 开闭原则 | Protocol + 组合，而非修改现有代码 |
| **L** 里氏替换 | Protocol 定义契约，实现类严格遵守 |
| **I** 接口隔离 | 多个小 Protocol，而非一个大接口 |
| **D** 依赖倒置 | 依赖 Protocol 抽象，不依赖具体实现 |

### Protocol 优于继承

```python
from typing import Protocol

# ✅ 用 Protocol 定义契约（鸭子类型）
class Repository(Protocol):
    def get(self, id: str) -> dict[str, object] | None: ...
    def save(self, data: dict[str, object]) -> str: ...

class Cache(Protocol):
    def get(self, key: str) -> object | None: ...
    def set(self, key: str, value: object, ttl: int = 300) -> None: ...

# 任何实现这些方法的类都自动满足 Protocol，无需显式继承
class PostgresRepo:
    def get(self, id: str) -> dict[str, object] | None:
        ...
    def save(self, data: dict[str, object]) -> str:
        ...

class RedisCache:
    def get(self, key: str) -> object | None:
        ...
    def set(self, key: str, value: object, ttl: int = 300) -> None:
        ...

# 依赖抽象，不依赖具体实现
def process(repo: Repository, cache: Cache) -> None:
    ...
```

### 依赖注入

```python
from dataclasses import dataclass

@dataclass
class UserService:
    repo: Repository
    cache: Cache

    def get_user(self, id: str) -> dict[str, object] | None:
        # 先查缓存
        if cached := self.cache.get(f"user:{id}"):
            return cached  # type: ignore[return-value]

        # 查数据库
        if user := self.repo.get(id):
            self.cache.set(f"user:{id}", user)
            return user

        return None

# 组装依赖
service = UserService(
    repo=PostgresRepo(connection_string="..."),
    cache=RedisCache(host="localhost"),
)

# 测试时注入 mock
service = UserService(
    repo=MockRepo(),
    cache=MockCache(),
)
```

### Result 类型（替代异常）

```python
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")
E = TypeVar("E")

@dataclass(frozen=True, slots=True)
class Ok(Generic[T]):
    value: T

    def is_ok(self) -> bool:
        return True

    def is_err(self) -> bool:
        return False

@dataclass(frozen=True, slots=True)
class Err(Generic[E]):
    error: E

    def is_ok(self) -> bool:
        return False

    def is_err(self) -> bool:
        return True

type Result[T, E] = Ok[T] | Err[E]

# 使用示例
def parse_int(s: str) -> Result[int, str]:
    try:
        return Ok(int(s))
    except ValueError:
        return Err(f"无法解析为整数: {s}")

def divide(a: int, b: int) -> Result[float, str]:
    if b == 0:
        return Err("除数不能为零")
    return Ok(a / b)

# 调用方显式处理错误
match parse_int("42"):
    case Ok(value):
        print(f"解析成功: {value}")
    case Err(error):
        print(f"解析失败: {error}")
```

### 接口隔离示例

```python
from typing import Protocol

# ❌ 错误：一个大接口
class Repository(Protocol):
    def get(self, id: str) -> dict | None: ...
    def save(self, data: dict) -> str: ...
    def delete(self, id: str) -> None: ...
    def list_all(self) -> list[dict]: ...
    def search(self, query: str) -> list[dict]: ...

# ✅ 正确：多个小接口
class Reader(Protocol):
    def get(self, id: str) -> dict[str, object] | None: ...

class Writer(Protocol):
    def save(self, data: dict[str, object]) -> str: ...

class Deleter(Protocol):
    def delete(self, id: str) -> None: ...

class Searcher(Protocol):
    def search(self, query: str) -> list[dict[str, object]]: ...

# 只依赖需要的接口
def read_only_operation(repo: Reader) -> None:
    ...

def write_operation(repo: Reader & Writer) -> None:  # 组合接口
    ...
```

---

## 支柱三：工程规范

### uv 项目管理

```bash
# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 初始化项目
uv init myproject
cd myproject

# 添加依赖
uv add fastapi pydantic uvicorn
uv add --dev pytest pytest-cov ruff mypy pre-commit

# 同步依赖（创建 venv 并安装）
uv sync

# 运行命令
uv run python -m myproject
uv run pytest
uv run mypy .
uv run ruff check .

# 锁定依赖
uv lock
```

### ruff 完整配置

```toml
[tool.ruff]
line-length = 88
target-version = "py312"
src = ["src"]

[tool.ruff.lint]
select = [
    "E", "W",     # pycodestyle errors/warnings
    "F",          # pyflakes
    "I",          # isort
    "N",          # pep8-naming
    "UP",         # pyupgrade
    "B",          # flake8-bugbear
    "C4",         # flake8-comprehensions
    "SIM",        # flake8-simplify
    "TCH",        # flake8-type-checking
    "PTH",        # flake8-use-pathlib
    "RUF",        # ruff 特有规则
    "ASYNC",      # flake8-async
    "S",          # flake8-bandit (安全)
]
ignore = [
    "S101",       # 允许 assert（测试中常用）
]

[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = ["S101"]  # 测试文件允许 assert

[tool.ruff.lint.isort]
known-first-party = ["myproject"]
force-single-line = true

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

### pre-commit 配置

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.13.0
    hooks:
      - id: mypy
        additional_dependencies:
          - pydantic>=2.0
          - types-requests

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
```

```bash
# 安装 hooks
uv run pre-commit install

# 手动运行
uv run pre-commit run --all-files
```

### 项目结构

```
myproject/
├── src/
│   └── myproject/
│       ├── __init__.py
│       ├── main.py           # 入口
│       ├── domain/           # 领域模型和业务逻辑
│       │   ├── __init__.py
│       │   ├── models.py     # Pydantic 模型
│       │   └── services.py   # 业务服务
│       ├── ports/            # Protocol 定义（抽象）
│       │   ├── __init__.py
│       │   └── repositories.py
│       └── adapters/         # 具体实现
│           ├── __init__.py
│           ├── postgres.py
│           └── redis.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # pytest fixtures
│   ├── test_domain.py
│   └── test_adapters.py
├── pyproject.toml
├── uv.lock
├── .pre-commit-config.yaml
└── .gitignore
```

### pyproject.toml 完整示例

```toml
[project]
name = "myproject"
version = "0.1.0"
description = "My strict Python project"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.115.0",
    "pydantic>=2.10.0",
    "uvicorn>=0.32.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.3.0",
    "pytest-cov>=6.0.0",
    "ruff>=0.8.0",
    "mypy>=1.13.0",
    "pre-commit>=4.0.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/myproject"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=myproject --cov-report=term-missing --cov-fail-under=80"

[tool.mypy]
python_version = "3.12"
strict = true
warn_unreachable = true
enable_error_code = ["ignore-without-code", "redundant-expr", "truthy-bool"]

[tool.ruff]
line-length = 88
target-version = "py312"
src = ["src"]

[tool.ruff.lint]
select = ["E", "W", "F", "I", "N", "UP", "B", "C4", "SIM", "TCH", "PTH", "RUF"]

[tool.ruff.lint.isort]
known-first-party = ["myproject"]
```

---

## Quick Reference

| 工具 | 命令 |
|------|------|
| 初始化 | `uv init myproject` |
| 添加依赖 | `uv add <package>` |
| 开发依赖 | `uv add --dev <package>` |
| 运行 | `uv run <command>` |
| 类型检查 | `uv run mypy .` |
| Lint | `uv run ruff check .` |
| 格式化 | `uv run ruff format .` |
| 测试 | `uv run pytest` |
| Pre-commit | `uv run pre-commit run --all-files` |

---

## Checklist

新项目启动时：

- [ ] `uv init` 初始化项目
- [ ] 配置 `pyproject.toml`（mypy strict、ruff、pytest）
- [ ] 创建 `.pre-commit-config.yaml`
- [ ] 创建 `src/` 目录结构
- [ ] 定义 Protocol（ports/）
- [ ] 实现适配器（adapters/）
- [ ] 编写测试（80%+ 覆盖率）
- [ ] `uv run pre-commit install`
