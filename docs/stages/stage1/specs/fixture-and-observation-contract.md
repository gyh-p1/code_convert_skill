# Spec 03｜Synthetic Fixture、Controlled Target 与行为观察契约

## 1. 目标

把“不能安全真实执行”转成可验证的受控观察面，但不把替代验证扩大解释为真实系统等价。每个 fixture 必须回答四个问题：

1. 替代了源码中的哪条行为义务？
2. 保留了哪些输入、状态转移、错误路径和副作用语义？
3. 明确不覆盖哪些真实环境因素？
4. 如何生成、观察、清理和复现？

## 2. Fixture 分类

### 2.1 `SYNTHETIC_DATA`

适用于凭据、浏览器 profile、API token、配置和密钥读取类 case：

- 所有内容由 fixture generator 生成，使用固定版本和种子；
- 内容只在一次性工作区和显式目录中出现；
- 日志中记录 fixture ID/hash，不记录秘密明文；
- 观察读取路径、字段存在性、解析结果、错误分支和输出摘要；
- 不访问真实用户目录、真实浏览器 profile、SSH 目录、云凭据目录或宿主密钥链。

### 2.2 `TRANSACTIONAL_LOCAL_SURFACE`

适用于文件、注册表/配置、临时持久化等行为：

- 将真实系统表面替换为可回滚、可枚举、版本化的测试表面；
- 记录前后状态差异、操作顺序、错误和清理结果；
- 不能把“测试表面写入成功”报告为真实系统持久化成功；
- 真实服务、启动项、系统策略、内核对象和防火墙配置仍属于禁止面，除非另有独立批准的靶标。

### 2.3 `LOOPBACK_SERVICE`

适用于 HTTP/TCP/DNS/协议处理：

- 服务只绑定 loopback 或封闭实验网地址；
- 使用固定响应、错误响应、超时和断连场景；
- 记录 method/path/headers 摘要、连接目标、重试/超时和返回状态；
- 禁止把真实 URL、真实下载源、生产服务或 C2 作为 fallback；
- 对硬编码外部地址，优先由网络层重定向到专用 stub；不能只修改样本配置而忽略源码入口。

### 2.4 `BENIGN_PROCESS_TREE`

适用于子进程和命令执行：

- 只允许登记过的 benign child fixture；
- 记录父子关系、启动参数摘要、退出码、信号/超时、资源峰值；
- 子进程不能访问 VM 外真实资源或未声明目录；
- 子进程树未收束、存在脱离根进程的进程或命令超时，结果为 `INCONCLUSIVE`/`BLOCKED_ENV`。

### 2.5 `CONTROLLED_TARGET_SIMULATOR`

适用于注入、漏洞利用、协议状态机或复杂目标交互：

- 靶标是专门构造、无真实数据、无公网入口、可回滚的 simulator；
- 只暴露要验证的状态机/输入边界，不复刻真实产品的可利用路径；
- 只记录输入构造、状态变化、目标响应、异常类别和清理；
- 结果名使用 `CONTROLLED_TARGET_BEHAVIOR_OBSERVED`，不能使用 `EXPLOIT_SUCCEEDED`。

## 3. Fixture Manifest

```json
{
  "fixtureSchemaVersion": "stage1.fixture.v1",
  "fixtureId": "loopback-http.v1",
  "fixtureVersion": "1.0.0",
  "imageOrPackageSha256": "sha256:...",
  "generator": { "name": "...", "version": "...", "seed": "..." },
  "providedSurfaces": ["http", "filesystem"],
  "inputFiles": [{ "path": "...", "sha256": "...", "synthetic": true }],
  "allowedTargets": [{ "kind": "loopback", "host": "127.0.0.1", "port": 0 }],
  "observationAdapters": ["network-events.v1", "fs-diff.v1"],
  "forbiddenSurfaces": ["public-network", "real-credentials", "host-user-profile"],
  "cleanup": { "transactional": true, "revertRequired": true },
  "limitations": ["does not model real DNS caching"]
}
```

Fixture 版本必须进入 Permit 的 hash 绑定；fixture 变更必须产生新 run，不得覆盖旧证据。

## 4. Oracle 契约

```json
{
  "oracleSchemaVersion": "stage1.oracle.v1",
  "oracleId": "case-123.oracle.v1",
  "obligations": [
    {
      "id": "OBL-NET-001",
      "sourceEvidence": ["source/foo.c:42-61"],
      "expectedObservations": ["tcp.connect", "request.sent", "response.status=200"],
      "negativeObservations": ["public-egress", "real-secret-emitted"],
      "comparison": "ordered-events-with-normalized-values",
      "tolerance": { "timestamps": "ignore", "temp-path-prefix": "normalize" }
    }
  ],
  "uncoveredBehavior": ["real-network-latency", "kernel-specific-scheduling"]
}
```

要求：

- oracle 必须按行为义务索引，不能只比较 stdout；
- `not-observed` 不得自动转成 `preserved`；
- 环境差异、fixture 限制和代码差异分别标注；
- oracle 没有覆盖的行为保持 `UNVERIFIED`。

## 5. 危险类别处理

| 类别 | 默认路径 | 可升级条件 |
|---|---|---|
| 凭据读取 | `FIXTURE_EQUIVALENCE` | 合成 profile 和字段级观察面通过；禁止真实凭据 |
| 持久化 | `TRANSACTIONAL_LOCAL_SURFACE` 或 `STATIC_ONLY` | 有可回滚、无宿主副作用的专用表面 |
| 子进程 | `RESTRICTED_PROCESS_RUN` | benign child allowlist、资源和树取证可用 |
| 注入 | `CONTROLLED_TARGET_SIMULATOR` 或 `STATIC_ONLY` | 专用受控靶标和最小状态机；不触发真实目标 |
| 漏洞利用 | 默认 `BLOCKED_UNMODELED` | 只有另行批准的安全 simulator，且不报告真实利用成功 |
| 服务/内核/防火墙改写 | 默认 `STATIC_ONLY` | 独立平台授权的虚拟表面；不能直接改真实 VM 基线 |

## 6. 质量门

Fixture 只有在以下全部满足时才可成为正式证据：

- 版本、hash、生成方式和输入可复现；
- 运行边界由 Agent/Controller 强制执行，不仅写在说明里；
- 有正向、错误、超时、空输入等最小观察集；
- 结束后可验证清理/revert；
- 输出不含真实凭据、未脱敏个人信息或未声明二进制；
- 证据报告明确 fixture 覆盖和未覆盖范围。
