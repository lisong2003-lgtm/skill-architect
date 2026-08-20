# WorkBuddy 安装与使用

## 下载包

WorkBuddy 使用通用 Skill 包，不要使用 Codex 插件包：

- 通用版下载：https://github.com/lisong2003-lgtm/skill-architect/releases/download/v0.2.0/skill-architect-generic-0.2.0.zip

## 安装方法

### 方法一：设置页导入

1. 打开 WorkBuddy。
2. 进入设置或技能管理页。
3. 点击“Import Skill”或“导入技能”。
4. 选择 `skill-architect-generic-0.2.0.zip`。
5. 导入后重启 WorkBuddy 或新开对话。

### 方法二：复制到技能目录

1. 解压 `skill-architect-generic-0.2.0.zip`。
2. 将解压后的 `skill-architect-generic` 文件夹放入：
   - 项目级：`.codebuddy/skills/`
   - 用户级：`~/.workbuddy/skills/`（以 WorkBuddy 实际版本为准）
3. 重启 WorkBuddy 或新开对话。

## 安装后测试

```text
用 skill-architect 审计我的 SKILL.md
```

```text
帮我总结这个长对话
```

```text
快速导入已总结长对话
```

## 注意事项

- Skill Architect 脚本需要 Python 3.9+。
- WorkBuddy 安装前可能执行安全扫描；脚本若被拦截，先查看扫描报告。
- 如果触发语没有生效，使用更明确的调用：

```text
读取 skill-architect 的 SKILL.md，按其中的流程执行。
```

- 长对话快照和 Skill 包导出导入均可在 WorkBuddy 中使用，因为它不依赖 Codex 专属功能。
