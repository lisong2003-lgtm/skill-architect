# Token 节省估算

## 参考案例

### 案例一：第一轮外移

- 主 `SKILL.md`：2034 行 / 71,224 字符 → 836 行 / 42,400 字符。
- 常驻行数减少：1198 行，约 59%。
- Token 估算节省：约 40%。
- 估算节省：约 17,300-23,100 tokens。

### 案例二：第二轮外移

- 主 `SKILL.md`：836 行 / 42,400 字符 → 586 行 / 28,389 字符。
- 常驻行数减少：250 行，约 30%。
- Token 估算节省：约 33%。
- 估算节省：约 8,400-11,200 tokens。

### 累计两轮

- 2034 → 586 行，减少 1448 行，约 71%。
- Token 估算节省：约 60%。
- 估算节省：约 25,700-34,300 tokens。

详细脱敏案例见 `CASE_STUDIES.md`。

## 为什么不是固定数字

- 不同模型的 tokenizer 不同。
- 外移技能包只在被调用时加载，实际节省取决于使用频率。
- 如果每轮都加载全部外移包，节省会减少。
- 这里的数字是估算，不是计费承诺。

## 自行计算

```bash
python3 scripts/estimate_tokens.py --original 原始SKILL.md --slimmed 瘦身后的SKILL.md --tokens-per-char 0.6
python3 scripts/estimate_tokens.py --original 原始SKILL.md --slimmed 瘦身后的SKILL.md --tokens-per-char 0.8
```
