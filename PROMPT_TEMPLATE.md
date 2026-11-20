# 角色 Emoji 生成规则与 Prompt 模板

适用于任意角色。把 `{占位符}` 换成目标角色后即可复用。
规则是从 Miku 这套 18 张图的返工里总结出来的，**每条都对应一次真实的失败**。

---

## 0. 先填这几个占位符

| 占位符 | 说明 | Miku 示例 |
|---|---|---|
| `{CHARACTER}` | 角色名 | chibi Hatsune Miku |
| `{SIGNATURE}` | **一眼认出角色的轮廓特征**（最重要） | two long teal twintails, pink-and-black headset, small ahoge |
| `{PALETTE}` | 主色 | teal #3ad2c2 hair, pink accents, black outlines |
| `{ACCESSORY}` | 跟身的小配件（可选，太多会糊） | one ear cup + short mic stub |
| `{STYLE}` | 画风 | flat vector, thick dark outlines, cel shading |

> `{SIGNATURE}` 是整套的命门。Miku 那次翻车就是 prompt 里写了「只露出马尾尖端」，
> 模型直接理解成「不要马尾」，整批变成短发，全部作废。

---

## 1. 硬性构图规则（写在每批 prompt 的最前面）

```
FRAMING RULES (all mandatory, verify before saving each file):
- Square 1:1, fully transparent background, nothing but the head (icons: the object only).
- Head centered, slightly above middle. The face (skin area) occupies 55-65% of the image
  height. The chin is fully inside the frame with a ~5% margin below it.
- {SIGNATURE} IS MANDATORY: it must be clearly visible and recognizable. If space is tight,
  make the face smaller - never remove, shrink to a stub, or hide the signature features.
  It may be drawn slightly BEHIND the head, but it must still read at a glance.
- Hair must not eat the frame: thin bangs, hairline ABOVE the eyebrows, no bangs over the eyes.
  Compress / flatten any ahoge or top spikes.
- Keep only {ACCESSORY}. No shoulders, no torso, no full body.
- EXPRESSIONS MUST BE HUGE AND OBVIOUS: eyes at least 20% of the image height in total,
  mouth at least 20% of the image width for open-mouth expressions, thick black outlines,
  big white highlights, no soft gradients.
- SYMBOL SIZE RULE: any distinguishing symbol (sweat drop, question mark, Zzz, anger mark,
  heart, sparkle) must be at least 25-30% of the image height, sit close to the head, and be
  fully inside the frame - never tiny, never pushed into a corner.
- Symbols go in the empty space OUTSIDE the face silhouette, never on top of the hair.
- No text, no watermark, no border, no drop shadow.
```


### 构图最终结论（Miku 版验证过，可直接套用）

```
- 紧贴脸部特写：脸占画面高 70~75%，下巴完整、下方留约 5% 余量。
- 双马尾「左右必须完整」：外侧轮廓在画面内，不从左右裁切。
- 头发「只从下方流出」：马尾自然垂到画面底边再被截断，画面内不画任何发梢/发尾。
- 头型略椭圆、下巴收窄，不要正圆脸。
- 五官可以压出脸的轮廓（大嘴越过下巴线、闭眼弧伸进头发），
  这样小尺寸才有剪影差异。
```

> 反面教材：让模型「把头发缩短」→ 变成短发；让头发「从左右流出」→ 马尾被切掉。
> 只允许「下方流出」，两侧必须留完整。

**为什么是 55~65% 而不是更大**：脸超过 70% 时，`{SIGNATURE}` 会被挤出画面。
实测 55~65% 是「表情够大」和「角色认得出」的平衡点。

---

## 2. 批量生成指令（prompt 后半部分）

```
Generate {N} images, one image_gen call each, saving each PNG to the exact absolute path
listed below (keep transparency, 1254x1254 or larger):

/abs/path/art/01_laugh.png - laughing hard: eyes squeezed shut as two sharp upward arcs,
    enormous open laughing mouth, tears of joy flying out beyond the outer eye corners
/abs/path/art/02_cry.png   - wailing: huge glossy eyes, thick tears running past the chin in
    two streams, wide wavy open mouth, inner brows raised

Never write outside /abs/path/art/.

Before saving each file, check: (1) {SIGNATURE} clearly visible, (2) chin fully visible with
margin, (3) expression readable at a glance, (4) symbol (if any) is big and close to the head.
If any check fails, regenerate that image instead of saving it.
```

- **输出路径一定写绝对路径**。我们踩过：只写文件名，模型把新图覆盖到了旧的素材目录。
- 一批 **4~8 张**。一次 16 张会撞图片额度（Codex 5 小时窗口约 15~18 张）。

---

## 3. 参考图策略

- 首张图定风格，后续每批都把 **同一张** 作为 `-i` 参考图传进去。
- 参考图只负责「角色 + 画风」，构图规则由文字强制，**不要让模型照抄参考图的裁切**：

```
The attached image is the reference for the character and art style only.
Do NOT copy its framing.
```

- 需要修某一张时，用**同批里最好的一张**当参考（构图一致），不要用早期的半身图。

---

## 4. 常见失败模式与对策

| 失败 | 表现 | 对策 |
|---|---|---|
| 标志性轮廓消失 | 双马尾/呆毛/耳朵没了 | prompt 里写死「MANDATORY + 空间不够缩脸，不许删」 |
| 脸太大 | 下巴被切、只剩额头 | 明确 55~65% + 下巴留 5% 边距 |
| 头发占满画面 | 刘海压眼、顶部一坨 | 细刘海、发线在眉毛上、压平呆毛 |
| 符号太小 | 汗滴/问号缩到几乎看不见 | 符号 ≥25~30% 画面高 + 贴近头部 |
| 图标画成人脸 | 💚🎧 变成角色头像 | 单列 ICON RULE：「no character, no face, object only」 |
| 风格漂移 | 越跑越像别的角色 | 每批都用同一张参考图 + 同批风格描述 |
| 表情雷同 | 剪影一样，只有五官不同 | 允许歪头/仰头，符号超出轮廓做剪影差异 |

---

## 5. 表情清单（可扩展）

按「一图一码位」映射。**优先做脸**，其次手势，最后物品/图标。

| 文件 | 码位 | 表情要求 |
|---|---|---|
| 01_laugh | U+1F602 | 闭眼成上扬弧线、超大张口、笑泪飞出眼眶 |
| 02_cry | U+1F62D | 巨眼高光、两道泪流过下巴、波浪嘴 |
| 03_smile | U+1F60A | 睁眼、小嘴微笑、轻腮红 |
| 04_heart_eyes | U+1F60D | 爱心瞳孔占满眼窝、张口、**不要飘散爱心** |
| 05_loving | U+1F970 | 闭眼柔和弧、强腮红、头顶飘爱心 |
| 06_angry | U+1F621 | 压眉、瞪眼、龇牙、怒符在头发外 |
| 07_sleep | U+1F634 | 闭眼下垂弧、小圆嘴、Zzz 在右上方 |
| 08_think | U+1F914 | 一眉挑、斜视、平嘴、问号 30% 高贴头 |
| 09_sweat | U+1F605 | 眉下垂、尴尬张口、汗滴 10% 宽贴太阳穴 |
| 10_thumbs | U+1F44D | 大笑 + 点赞手占画面 1/3 |
| 11_pray | U+1F64F | 泪眼恳求 + 双手合十 |
| 12_green_heart | U+1F49A | 纯图标：大心形 |
| 13_headphones | U+1F3A7 | 纯图标：耳机 |
| 14_mic | U+1F3A4 | 闭眼唱歌 + 大麦克风 |
| 15_note | U+1F3B5 | 纯图标：音符 + 小闪光 |
| 16_sparkles | U+2728 | 纯图标：大四角星 + 小星 |

> 顺序建议：先 11 个「脸」，确认整套能读，再补图标。
> 图标没有表情，做多少都不影响「辨识度」的主体结论。

---

## 6. 出图后必做

1. 16/24/32/48px 四档渲染对比（PIL 即可），**只在 20px 下判断能不能读**。
2. 抽 3 张丢进真实场景：Omarchy 表情选择器、Chrome 页面、终端。
3. 大图好看但小图糊 = 构图问题，回第 1 节调比例，不要靠加细节硬救。
