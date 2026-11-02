# 来源、许可与发布范围

## 原创技能与代码

本仓库的原创方法说明、提示配方、制作记录与可移植工具代码采用根目录 MIT 许可，署名 cooperchx。MIT 不覆盖下列第三方内容，也不授予人物肖像或品牌权利。

## 示例人物、图片与视频

示例照片由用户提供，部分照片带有原平台/品牌标记，作者与权利未独立核实。原始输入保留在 `assets/references/`，索引为 `sources.json`。照片不被重新声明为本项目原创，也不被重新授权为MIT。

人物与城市贴图由本次工作流中的内置 image_gen 生成或从生成图裁切；对应提示在各项目、制作记录和清单内。它们用于展示制作方法。图像的生成不消除原输入涉及的肖像、商标或来源限制；商业再用请采用自己的授权输入并重新生成。城市贴图主要为生成的场所表达，不作为建筑形制、地址或历史事实的证据。

`assets/catalog.json` 包含全部去重图片及来源别名；其中还包括作品检查联系表、参考片分析小图，类别需结合 alias 识别。用于分析的原参考来自用户提供的“虎小象-服装片或者其他片子想剪下面这个效果…”片段。现按用户明确要求收录原参考完整MP4及GIF预览，单独放在 `media/reference/` 并记录哈希；未发布全量逐帧缓存。原参考不属于本项目原创视频，亦不适用MIT重新授权。无法从成片确认其作者使用的软件/模型。

`media/videos/` 为本次制作中已交付的原始输出，GIF为同一视频完整时长的预览转换。音轨为本地合成，源码随各工程保存；已检查输出长度、电平等，未把测量声称为试听。

## 字体

- 得意黑 Smiley Sans：atelierAnchor，SIL Open Font License1.1。来源 [atelier-anchor/smiley-sans](https://github.com/atelier-anchor/smiley-sans)，许可随包保留在 [third-party/SmileySans-OFL.txt](third-party/SmileySans-OFL.txt)。
- 原机器上的其他系统字体（包括部分 .ttc/.ttf）未重新分发。公开工程移除对应本机字体加载声明，采用浏览器字体回退。因此再渲染排版可能有差异；历史成片不受影响。需要严格复现时由使用者选择并提供适当授权的字体。

## 可选第三方运行库

历史工程的 `assets/gsap.min.js` 保留原版权头与标准许可链接。GSAP 属于 GreenSock；适用 [GSAP Standard License](https://gsap.com/standard-license/)，不被MIT重新许可。它只用于原始可编辑工程；独立 `templates/player.html` 不依赖GSAP。

HyperFrames 是历史项目可选渲染器，不是本skill必备依赖。Puppeteer/Chromium 与 FFmpeg 按各自项目许可由用户安装，未把其二进制纳入本仓库。

## 未发布内容

不包含凭证、账户配置、缓存、绝对个人文件路径、逐帧解码缓存或本机专有字体。已去重的PNG保留一个canonical文件和所有原文件别名，项目引用处可另有同内容副本。没有找到的伦敦v2成片不补造；其阶段工程完整保留。
