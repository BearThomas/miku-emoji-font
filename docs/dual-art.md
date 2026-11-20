# 画风说明（v3.0 起）

从 v3.0 开始，**所有字号统一使用贴近 Crypton 官方设定的还原画风**：
81 张表情脸均以官方角色立绘为参考重绘（冷白肤色、正常眼型、准确的耳机与刘海、细描边），
手势 / 图标 / 心形 / 怪物沿用原有的独立图标。

## ⚠️ 小字号可能认不清

这是已知且刻意的取舍：

- 还原风格依赖**细描边、淡肤色、小眼睛**，这些特征在 16~20px 下物理上没有足够像素表达。
- v2.0 曾做过「小字高辨识 / 大字还原」的双版本，但按反馈已取消——现在所有字号都用还原版。
- 如果你在聊天窗口觉得某些表情变淡、不好认，这是预期行为，不是 bug。

建议：在 48px 以上观看能获得最佳效果；需要小字高辨识的场景请退回 v2.0.0。

## 构建

源码包里的 `art/` 就是最终使用的图（不再有 `art_hybrid/`）。构建命令：

```bash
.venv/bin/python scripts/check_art.py
.venv/bin/python scripts/build_font_seq.py \
  --art art --manifest art/manifest.json --sequences art/sequences.json \
  --subset <CBDT 容器> --family "Miku Emoji" --out MikuEmoji.ttf
```
