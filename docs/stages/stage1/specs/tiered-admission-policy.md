# Spec 04｜最高危阻断准入策略

> 版本：2.1；更新：2026-10-09
> 状态：**已实施**（分类器 v2.3；三条规则落地，隔离开关可由 CLI 配置）
> 依据：[安全边界](../../../../references/framework/safety-boundary.md) 第2节批次授权与逐例核对
> 实施记录：[最高危阻断策略修订与六批复跑](../reports/最高危阻断策略修订与六批复跑.md)

## 1. 目标与约束

在评估平台能力范围内，**最大限度允许运行**：**仅阻断最高危代码，其余全部允许运行**。

**不改变的红线**：
- 本机不执行（safety-boundary.md §1）
- 禁止连接公网/生产网/真实外部目标（§3）
- 禁止使用真实凭证（§3）
- VM隔离、合成数据、快照回滚必须满足（§2）

**核心原则**：
- 默认允许：VM隔离环境中，源码已有的行为默认允许执行（§3）
- 最小阻断：只阻断明确越出VM隔离边界的最高危代码
- 批次授权：同一批次一次授权，无需逐项询问（§2）

## 2. 二元准入架构

| 准入级别 | 判定依据 | 预计覆盖 |
|---|---|---|
| **ALLOWED** | 可在VM隔离环境安全执行 | ~75-80% |
| **BLOCKED** | 明确越出隔离边界或输入错误 | ~20-25% |

不再区分"低风险"、"中风险"、"需审阅"。除明确阻断项外，**一律允许**。

## 3. BLOCKED 阻断规则（最小化）

分类器输出 `admissionStatus: "BLOCKED"`，**仅在**以下情况阻断：

### 3.1 输入完整性错误（BLOCKED_INPUT）

```python
classification == "BLOCKED_INPUT"
# 文件缺失、哈希不符、路径越界、编码错误等
```

**阻断原因**：无法冻结源码身份，不是安全风险问题。
**解决方式**：修复输入后重新分类。
**预计数量**：39条（18%）

### 3.2 明确公网目标（未配置隔离）

```python
classification == "REVIEW_NETWORK"
and any(networkScope in ["public", "hostname"])
and NOT network_isolation_verified  # 批次级配置
```

**阻断原因**：字面硬编码公网地址/域名，未验证网络隔离。
**解决方式**：
- 选项A（推荐）：批次级配置网络隔离重定向后，全部放行
- 选项B：逐项确认地址已阻断后放行

**预计数量**：~11条（6%），**配置隔离后降为 0**

### 3.3 真实凭证线索（高置信度）

```python
details.contains_high_confidence_credential_pattern
# 例如：真实格式的私钥、token、密码（非示例/占位符）
```

**阻断原因**：可能包含真实凭证，违反安全边界§3。
**解决方式**：人工确认是示例数据后放行，或替换为合成凭证。

**预计数量**：~2-3条（<2%），需人工逐项判断

**重要**：仅阻断**高置信度真实凭证**。包含 "password"、"key"、"token" 等关键词但使用占位符值的代码**不阻断**。

## 4. ALLOWED 允许规则（默认）

**除明确阻断项外，一律允许**，包括但不限于：

### 4.1 低线索代码
- `LOW_SIGNAL`：未检出已知线索 → **允许**

### 4.2 本地副作用
- `REVIEW_SIDE_EFFECTS`：文件/进程操作 → **允许**
- 理由：VM隔离 + 快照回滚，副作用可清理

### 4.3 网络操作（已隔离）
- `REVIEW_NETWORK` - loopback/unresolved → **允许**
- `REVIEW_NETWORK` - private（批次配置隔离后）→ **允许**
- 理由：safety-boundary.md:19 允许封闭实验网

### 4.4 敏感操作
- `REVIEW_SENSITIVE`：可执行内存、WMI、注册表等 → **允许**
- 理由：safety-boundary.md:21 "源码已有的敏感行为不自动排除真实运行"
- 前提：VM隔离 + 合成数据（批次级确认）

### 4.5 动态代码
- `dynamic_code` in reviewGroups → **允许**
- 理由：VM隔离环境中，动态执行不越出沙箱

### 4.6 框架依赖
- `REVIEW_DEPENDENCY`（Metasploit等）→ **允许**
- 理由：在隔离VM中，框架本身不构成风险
- 注意：需确保真实入口存在（T03核对）

### 4.7 词法不确定
- `REVIEW_UNCERTAIN`（heredoc、raw string等）→ **允许**
- 理由：词法覆盖不足不等于危险；VM隔离提供兜底保护

## 5. 实施变更点

### 5.1 分类器输出（tools/safety_classifier_v2.py）

在现有 ClassificationResult 增加：

```python
@dataclass
class ClassificationResult:
    # 现有字段保持
    classification: str
    executable: bool = False  # 废弃但保持兼容
    executionApproved: bool = False  # 废弃但保持兼容
    
    # 新增字段（简化为二元）
    admissionStatus: str  # "ALLOWED" | "BLOCKED"
    blockingReason: Optional[str]  # "input_error" | "public_network_unverified" | "real_credential_suspected" | null
    requiresNetworkIsolation: bool  # 含公网目标，需批次级配置隔离
    requiresSyntheticData: bool  # 含敏感操作，需批次级确认使用合成数据
    
    # 保持现有
    details: dict
    reviewGroups: List[str]
```

**判定逻辑**（v2.3 已实现，见 `_determine_admission`）：

```python
def determine_admission(classification, details, network_scope, review_groups):
    # 规则1: 输入错误
    if classification == "BLOCKED_INPUT":
        return "BLOCKED", "input_error"

    # 规则2: 公网目标（未配置隔离时阻断）
    if "public" in network_scope or "hostname" in network_scope:
        # 批次级配置网络隔离后，此规则不触发
        if not batch_network_isolation_configured:
            return "BLOCKED", "public_network_unverified"

    # 规则3: 高置信度真实凭证（极少数，需人工逐项）
    if detect_high_confidence_real_credential(details):
        return "BLOCKED", "real_credential_suspected"

    # 默认：允许
    return "ALLOWED", None
```

**实施说明**：

- 规则按 1→2→3 顺序短路，因此同时命中"公网未隔离"与"疑似凭证"时报
  `public_network_unverified`，让审查者先修隔离而不是追凭证。
- `batch_network_isolation_configured` 经 CLI `--network-isolation-configured` 传入，
  **默认关闭**。该开关不验证隔离是否真的存在；启用前须先落盘 §5.2 的批次授权证据。
- `detect_high_confidence_real_credential` 只识别凭证**格式**（私钥块、云/平台令牌前缀、
  JWT、带密码的 URL），并用占位符表排除 `changeme`、`${VAR}`、`your-token-here` 等值。
  这是 §3.3"仅阻断高置信度真实凭证"的直接实现，不是完整凭证检测。

### 5.2 批次授权记录（简化）

创建 `docs/test/dataset/{batch-id}/batch-authorization.json`：

```json
{
  "batchId": "batch-02",
  "authorizedAt": "2026-10-09T18:30:00Z",
  "authorizedBy": "human-reviewer",
  
  "vmIsolation": {
    "confirmed": true,
    "snapshotRollback": true,
    "cleanupVerified": true
  },
  
  "networkIsolation": {
    "configured": true,
    "publicNetworkBlocked": true,
    "experimentalNetworkOnly": true,
    "verificationEvidence": "iptables规则已配置，curl 8.8.8.8 超时，仅192.168.101.0/24可达",
    "verifiedAt": "2026-10-09T17:45:00Z"
  },
  
  "dataSource": {
    "syntheticDataOnly": true,
    "noRealCredentials": true,
    "noProductionData": true,
    "confirmation": "所有输入已审阅，使用占位符凭证"
  },
  
  "scope": "所有非BLOCKED任务",
  "validUntil": "2026-10-16T23:59:59Z",
  "contractHash": "sha256:e088a356..."
}
```

**一次授权，整批生效**。

**完整字段校验规则与拒绝条件见 [Spec05 §2](submission-and-batch-authorization.md)**：
任一必填字段缺失、为假或过期即拒绝整批，不逐项降级。

### 5.3 提交端逻辑（evaluation adapter）

提交端接口契约（签名、输出结构、判定顺序、12 项验收用例）见
**[Spec05 提交端准入消费与批次授权](submission-and-batch-authorization.md)**。
本节保留策略意图，实现细节以 Spec05 为准。

核心规则：仅阻断明确 BLOCKED 项，其余全部允许；三类阻断互相独立；
**即使批次配置了隔离，`real_credential_suspected` 也不放行**，须人工确认为示例数据后修正分类输入再重跑。

## 6. 预期效果与实际结果

**以下为提案时的估算（180 条可读文本）**：

| 分类 | 数量 | 默认准入状态 | 配置隔离后 |
|---|---:|---|---|
| LOW_SIGNAL | 3 | ALLOWED | ALLOWED |
| REVIEW_SIDE_EFFECTS | 51 | ALLOWED | ALLOWED |
| REVIEW_NETWORK（loopback/private） | ~35 | ALLOWED | ALLOWED |
| REVIEW_NETWORK（public/hostname） | ~11 | BLOCKED → 配置隔离 | **ALLOWED** |
| REVIEW_SENSITIVE | 53 | ALLOWED | ALLOWED |
| REVIEW_UNCERTAIN | 5 | ALLOWED | ALLOWED |
| REVIEW_DEPENDENCY | 22 | ALLOWED | ALLOWED |
| 疑似真实凭证 | ~2 | BLOCKED → 人工确认 | ALLOWED（确认后） |
| BLOCKED_INPUT | 39 | BLOCKED（输入错误） | （修复后放行） |
| **允许执行合计** | **~169** | **~93%（未配置隔离）** | **~98%（配置隔离后）** |

**v2.3 实测（219 条全量，未配置隔离）**：

| 结果 | 恢复前 | 恢复后 |
|---|---:|---:|
| ALLOWED | 158（72.1%） | **178（81.3%）** |
| BLOCKED — input_error | 39 | **15** |
| BLOCKED — public_network_unverified | 22 | **26** |
| BLOCKED — real_credential_suspected | 0 | 0 |

"恢复后"指按 [输入恢复性核查](../../../test/dataset/stage1-admission-recheck-2026-10-09/missing-input-recovery.md)
从原始交接包恢复 **24 条**逐字节一致的源码后重跑；剩余 15 条仍缺失。
详见[恢复后报告](../../../test/dataset/stage1-admission-recheck-2026-10-09/post-recovery-report.md)。

实测与估算的偏差及原因：

- **允许率 81.3% 仍低于估算的 93%**，主因是估算按"180 条可读文本"计算，把输入错误
  排除在分母外；按全量 219 条计则为 178/219。两者口径不同，不是策略失效。
- **公网未隔离 26 条**高于估算的 ~11 条。差异来自两点：估算基于 v2.1 分类；
  且恢复的 24 条中有 2 条（B01 `8.8.8.8`、B26 `pastebin.com`）含真实公网目标。
- **输入缺失 39 条 → 恢复后 15 条**（batch-01 案例目录缺失 12 已恢复、batch-02 缺 1 已恢复、
  batch-05 源目录为空 11 已恢复）。剩余 15 条在交接包中未找到。
- **凭证 0 条**，低于估算的 ~2 条。已用真实格式串验证规则可触发；建议在独立标注中确认
  这是数据集确实不含真实凭证，而非检测过窄。

### 对比当前策略

| 维度 | 修订前 v2.1/v2.2 | 本策略（v2.3，恢复后） |
|---|---|---|
| 自动允许率 | 0%（规则3缺失、开关不可达） | **81.3%**（未配置隔离） |
| 配置隔离后 | 0% | **204/219（93.2%）**；batch-02～06 达 100%，batch-01 62.5%（余 15 条输入错误） |
| 人工审阅需求 | 219项逐项 | 41项为机械阻断，其余按 reviewGroups 分配 |
| 批次处理时间 | 长 | 批次级一次性配置 |

> "配置隔离后"为一次性模拟值（产物已删除）：打开 `--network-isolation-configured` 后复跑得到
> 204/219。**正式输出不采用该口径** —— 批次级隔离须由真实 `batch-authorization.json` 证据支撑
> （§5.2），且该开关不验证隔离是否真的存在。

**前提条件**：
1. T02-a：修复 CONTRACT_MISMATCH
2. T03-a：处置剩余 15 条输入缺失（24 条已恢复）
3. **批次级一次性配置**：网络隔离 + 合成数据确认（~30分钟）
4. 疑似真实凭证的人工确认（本轮 0 条）

## 7. 安全保障

### 7.1 不降低的保护（零容忍项）

| 红线 | 保护机制 | 验证方式 |
|---|---|---|
| 本机不执行 | 所有代码仅在远程VM执行 | 架构级保护，不可绕过 |
| 公网隔离 | 批次级网络隔离配置强制 | 含公网目标的批次必须配置，未配置则整批阻断该类任务 |
| 真实凭证 | 高置信度检测 + 人工确认 | 疑似真实凭证逐项阻断，确认后放行 |
| 生产数据 | 批次级合成数据确认 | 批次授权必需字段 |
| VM隔离 | 快照回滚 + cleanup验证 | Controller enforcement |

### 7.2 新增的追溯能力

- 每项执行关联批次授权记录（含隔离证据）
- 分类依据（classification + reviewGroups）完整保留
- 批次授权有效期与契约版本绑定
- 允许执行的案例可追溯到具体规则（§4允许列表）

### 7.3 回退与应急

- 发现隔离失效：立即撤销批次授权，阻断所有新提交
- 发现真实凭证泄漏：单项紧急阻断，不影响其他任务
- 分类规则误判：更新规则后重新分类，已执行证据保留
- 保守模式：可临时恢复 executable=false 全阻断策略

## 8. 与现有文档的一致性

| 文档 | 条款 | 本策略符合性 |
|---|---|---|
| 安全边界 §2 | 批次授权与逐例核对 | ✓ 批次级授权，最小化逐项审阅（仅疑似凭证） |
| 安全边界 §3 | 源码已有敏感行为不自动排除 | ✓ **敏感操作默认允许**（VM隔离） |
| 安全边界 §3 | 可使用封闭实验网 | ✓ **私网目标默认允许**（批次配置隔离） |
| 安全边界 §3 | 不要求全部缩减为loopback | ✓ **封闭实验网目标明确允许** |
| 分类规格 §1 | 分类结果是线索不是证明 | ✓ 分类用于识别阻断项，非阻断项仍受VM隔离保护 |
| 分类规格 §3 | LOW_SIGNAL 不等于安全 | ✓ 所有执行仍需VM隔离+快照+批次授权 |

**关键突破**：
- 从"需证明安全才允许"转为"需证明危险才阻断"
- 从"逐项审阅"转为"批次授权+最小阻断"
- 充分利用安全边界§3已明确允许的范围

## 9. 实施路径

### 阶段1：环境恢复与批次配置（T02-a + T03）— **部分完成**
1. 修复 CONTRACT_MISMATCH（必需，当前三 runner 均不匹配）— **未完成**
2. 处置 39 条输入缺失 — **24 条已按 SHA-256 恢复，15 条待索取或重新冻结**
3. 完成批次级网络隔离配置（一次性，~30分钟）— 未完成
4. 完成批次级合成数据确认（一次性，~15分钟）— 未完成

### 阶段2：分类器修订（T01-b/c）— **已完成**
1. ~~修改 `safety_classifier_v2.py` 增加二元判定逻辑~~ → v2.3 已实现
2. ~~更新合成回归覆盖阻断规则~~ → 47 项回归通过
3. ~~对219条重新输出 admissionStatus~~ → 六批结果见[重跑报告](../reports/最高危阻断策略修订与六批复跑.md)
   与[恢复后报告](../../../test/dataset/stage1-admission-recheck-2026-10-09/post-recovery-report.md)

### 阶段3：提交端与试点验证（T01-d + T03-d）— **可领取**
1. 按 [Spec05](submission-and-batch-authorization.md) 实现 `prepare_submission()` 与批次授权校验
2. 选择输入完整的批次（**batch-02 现已 40/40 完整**）
3. 创建批次授权记录（`batch-authorization.json`，字段校验见 Spec05 §2.2）
4. 执行准入判定 → 提交 allowed 任务 → 验证双侧证据

> **阶段3 实测修正**：原估算"~37条ALLOWED，~1条输入问题，~2条需确认"与实测不符。
> batch-02 恢复后为 **40 ALLOWED / 0 BLOCKED**，且**凭证 0 条**。
> 全量 219 条恢复后为 178 ALLOWED / 41 BLOCKED（输入错误 15 + 公网未隔离 26）。

### 阶段4：扩展与验收— **未开始**
1. 扩展到全部219条（配置隔离后）
2. 验收指标（原定）：
   - 允许执行率 ≥ 95%（配置隔离后）
   - 人工审阅需求 ≤ 5项
   - 批次处理时间 ≤ 1小时（首次配置）
   - 后续批次 ≤ 15分钟（复用配置）
3. 达标后进入完整剥离（T05）

> **指标口径提醒**：上述"允许执行率"是**准入判定比例**，不是运行覆盖率。
> 双侧覆盖率按 Spec03 §4 单独统计，二者不可混用（Spec03 §4、Spec01 §1）。

## 10. 关键决策记录

| 决策 | 依据 | 影响 |
|---|---|---|
| **默认允许，最小阻断** | 用户明确要求"能力范围内全部允许" | 从0%提升到~98%允许率 |
| **不分级，只有ALLOWED/BLOCKED** | 用户要求"不执行分级" | 简化实现，消除中间状态 |
| **批次级配置，不逐项** | 安全边界§2批次授权 | 节省~99%人工审阅 |
| **敏感操作允许执行** | 安全边界§3明确允许 | 覆盖53条REVIEW_SENSITIVE |
| **封闭实验网允许** | 安全边界§3明确允许 | 覆盖私网目标（配置后） |
