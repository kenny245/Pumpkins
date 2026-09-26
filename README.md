# GPT-6 Astra 南瓜挑战（Pumpkins）

本仓库保存 GPT-6 Astra 在《The Farmer Was Replaced》（编程农场）**Pumpkins 多无人机排行榜**中的最终打榜版本。

## 成绩

- **最终正式成绩：359.484 秒**
- **全球排名：#8**
- 项目：**Pumpkins（多无人机）**

这次优化过程并不是一次性生成一个“最终答案”，而是 Astra 在长期自主任务中持续进行 benchmark、比较、回滚和迭代后得到的结果。

已记录到的排名演化大致为：

```text
#162  467.083 s
  ↓
#20
  ↓
#16
  ↓
#15  367.941 s
  ↓
#8   359.484 s
```

从最初的 467.083 秒到 359.484 秒，总计减少 **107.599 秒**，整体用时下降约 **23%**。

---

## 这份代码解决的核心问题

南瓜榜真正困难的地方，并不只是“如何更快地种南瓜”。

如果让整张 32×32 农场作为一个巨大的同步区域，那么每一轮完成时间都会被最慢成熟的那几株南瓜拖住。也就是说，系统会越来越像：

```text
1024 株南瓜
↓
绝大多数已经成熟
↓
少数 straggler 仍未成熟
↓
所有无人机一起等待
```

最终版本的核心思想，是把这个问题重新建模成一个**并行调度 + 长尾控制**问题，而不是单纯的种植问题。

---

## 1. 把整张地图拆成 16 个独立 patch

最终代码没有让 32 个 drone 无结构地在整张地图上工作，而是预先定义了 16 个局部区域：

```python
drones = {
    (3, 3): 7,
    (11, 0): 8,
    (20, 0): 8,
    ...
}
```

patch 尺寸只使用：

- 6×6
- 7×7
- 8×8

每个 patch 自己完成：

```text
种植
↓
成熟检查
↓
只回访异常格
↓
局部同步
↓
收获
```

这样，一株特别慢的南瓜只会拖慢自己的局部区域，而不会拖住整张农场。

这相当于把一个巨大的全局 barrier 拆成多个更小的局部 barrier。

---

## 2. 16 个区域 × 每区 2 个 drone = 32 drone 并行

每个 patch 内部进一步拆成左右两部分。

父 drone 负责一侧，helper drone 负责另一侧：

```python
right_drone = spawn_drone(right_side)
left_side()
wait_merge(right_drone)
```

因此整体结构近似：

```text
16 个 patch
×
每个 patch 2 个 drone
=
32 个 drone
```

这正好吃满多无人机榜允许的并发能力。

每个 patch 只在自己内部做 join，不需要等待全局所有 worker。

---

## 3. 几何循环路径：减少无意义回程

代码中的 `CYCLE_STEPS`、`CYCLE_INDEX` 以及 7×7 专用的 `SEVEN_LEFT_*` / `SEVEN_RIGHT_*` 看起来非常“机器化”，但目的很明确：

> 预先把局部区域的遍历路线编译成固定几何循环。

无人机不需要每一轮都重新回到统一起点。

程序会根据当前坐标找到自己在 cycle 中的位置，然后从当前位置继续完成整圈：

```python
first = CYCLE_INDEX[key][local]
```

这减少了多轮 traversal 之间纯粹为了“回起点”产生的移动成本。

7×7 无法像偶数尺寸一样干净地一分为二，因此最终代码为它准备了非对称的专用路径表，并用 flags 区分“经过但不执行工作”的 movement-only 节点。

---

## 4. 不反复扫描整个区域，只追踪未成熟格

每个 worker 维护：

```python
unripes_in_stack = []
unripes_out_stack = []
```

并用两个 stack 模拟 queue。

第一遍检查以后：

- 已经正常成熟的格子不再处理
- 只有未成熟或异常的格子进入待处理队列

于是后续工作从：

```text
反复扫描整个 patch
```

变成：

```text
完整扫描一次
+
只回访越来越少的异常格
```

这非常适合南瓜任务，因为真正拖慢整体速度的往往只是极少数 straggler。

---

## 5. “最后一步不走”：提前判断是否已经合并

在回访异常格时，代码会故意停在目标的最后一步之前：

```python
last_d = move_to_without_last_move(dequeue())
```

然后先用 `measure()` 判断目标是否已经与当前成熟南瓜组连通：

```python
group_id = measure()
if group_id != None and group_id == measure(last_d):
    continue
```

如果已经满足条件，就连最后一次 move 都不执行。

这能避免：

- 最后一步移动
- 多余的 harvestability 检查
- 额外的补种 / 浇水 / 施肥判断
- 再次离开该格子的移动

这里还修复了一个很容易漏掉的边界问题：

```python
None == None
```

本身为 True。

因此最终版明确要求：

```python
group_id != None
```

避免把“两边都没有有效 group id”错误地当成“已经属于同一个成熟组”。

---

## 6. 肥料只用来处理真正的尾部异常

最终版不是看到未成熟南瓜就立即使用 Fertilizer。

只有满足多个条件才会施肥：

- 本次确实发生了重新种植
- 当前 round 已经等待了一定时间
- 剩余异常格非常少
- 库存中确实还有肥料

核心思想是：

> **肥料不是拿来提高平均速度，而是拿来消灭最后几个 straggler。**

而且最终版还处理了一个重要边界情况：肥料可能让作物立即死亡。

因此：

```python
if use_item(Items.Fertilizer):
    if get_entity_type() == Entities.Dead_Pumpkin:
        plant(Entities.Pumpkin)
```

一旦肥料导致 Dead Pumpkin，立即重新种植，而不是等下一轮队列再次访问。

---

## 7. 浇水阈值按 patch 尺寸和运行阶段调整

旧版本使用统一浇水阈值。

最终版变成：

```python
target_water = {
    6: 0.8,
    7: 0.7,
    8: 0.6
}[size]
```

并且在启动阶段：

```python
if start_time < 90:
    target_water = 0.4
```

这意味着 Astra 已经开始区分：

- 启动阶段
- 稳态阶段
- 不同 patch 尺寸

前期尽量减少浇水操作带来的额外成本，后期再针对不同区域规模控制成熟长尾。

---

## 8. 热路径优化：目标检查从“每格一次”降到“每 4 步一次”

最终版本没有在每处理一个格子时都调用：

```python
num_items(Items.Pumpkin)
```

而是把 traversal 分成 4 步一个 chunk：

```python
for chunk in range(first, len(steps), 4):
    if num_items(Items.Pumpkin) >= 200000000:
        return
```

这样做接受了“最多多跑几个动作”的小风险，却显著减少了热循环中的全局状态查询。

这是非常典型的摊销优化。

---

## 9. 初始化路径与热路径分离

第一轮需要 `till()`：

```python
plant_pumpkin = plant_pumpkin_with_till
```

完成初始化以后，后面的稳定循环直接切换函数引用：

```python
plant_pumpkin = plant_pumpkin_no_till
```

后续不再重复判断土地状态，也不再执行无意义的 till。

---

## 为什么这份代码值得保留

最有意思的不是最终 #8 本身，而是算法思路的变化。

最初的问题可以描述成：

> “怎样更快地种满南瓜并等待成熟？”

最终版本解决的却变成：

> “怎样把随机成熟时间造成的尾部延迟限制在局部区域，并让 32 个 worker 尽可能持续做有效工作？”

这也是整个优化过程中最明显的变化：

```text
大范围同步
↓
局部分区
↓
双 drone 协作
↓
只追踪异常格
↓
尾部肥料策略
↓
几何热路径
↓
边界条件修复
↓
全球 #8
```

从 #162 到 #8，并不是简单调几个参数得到的结果，而是先改变并行结构，再逐渐进入热路径和边界条件级别的优化。

---

## 文件

- `pumpkins_rank8_final.py`：本次 Pumpkins 全球 #8 的最终打榜版本

---

## 来源与许可证

这份实现基于公开项目：

- `enihsyou/The-Farmer-Was-Replaced`
- Source commit: `37a97b58e15dc60bb6aff8829eeb58293be18b39`

原项目使用 **MIT License**。

本仓库保留了原始代码中的版权与 MIT License 声明，并记录了后续适配与优化版本。

---

## 说明

排行榜成绩会随着其他玩家提交新成绩而变化，因此这里记录的 **全球 #8** 指该版本正式提交并截图确认时的实时排名。

本仓库的目的主要是保存和分析这次 GPT-6 Astra 自主优化实验中的最终实现与算法演化结果。
