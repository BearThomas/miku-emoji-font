# 源文件与构建

仓库本体只放「轻量」文件。`art/` 下的 120 张原始 PNG（约 158 MB）作为
**源码包**放在 [Releases](https://github.com/BearThomas/miku-emoji-font/releases)
里：`miku-emoji-src-<版本>.tar.gz`。

源码包内容：

```
miku-emoji-src-X.Y.Z/
├── art/                    高辨识版 120 张 PNG + manifests
├── art_hybrid/             官方还原版 81 张 PNG（人脸用）
├── scripts/
│   ├── build_font_dual.py  双 strike 字体（小字高辨识 / 大字还原）
│   ├── build_font_seq.py   单画风构建脚本
│   ├── check_art.py        构建前校验（重复内容 / 重复码位 / 文件缺失）
│   ├── install.sh          安装（默认不启用）
│   └── uninstall.sh        卸载
├── MikuEmoji.ttf            已构建的字体（直接安装用）
├── LICENSE                 Piapro 非商业授权
├── PROMPT_TEMPLATE.md       生成提示词模板（换角色可复用）
└── emoji-list.md            120 个字符总表
```

从源码重建（Arch 示例）：

```bash
tar xf miku-emoji-src-2.0.0.tar.gz
cd miku-emoji-src-1.7.0
python -m venv .venv && .venv/bin/pip install fonttools pillow
.venv/bin/python scripts/check_art.py
.venv/bin/python scripts/build_font_dual.py \
  --art art --art-large art_hybrid \
  --manifest art/manifest.json --sequences art/sequences.json \
  --subset <CBDT 容器> --family "Miku Emoji" --out MikuEmoji.ttf
```

> `--subset` 需要一个合法的 CBDT 容器（本项目用 Apple Color Emoji 的 subset）。
> 不想折腾就直接用源码包里已经构建好的 `MikuEmoji.ttf`。

**注意：字体装好后不会自动接管表情。** 想启用请运行 `./install.sh --enable`，
或按 `install.sh` 打印的命令手动建 fontconfig 符号链接。
