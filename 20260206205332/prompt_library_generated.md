# 提示词模板库 - 自动生成
> 生成时间: 2026-02-11 17:27

## 文案生成
- `setup_check.py:45`  
  ("agents/writer.py", "文案智能体"),
- `xiaohongshu_publisher.py:65`  
  # 2. 文案生成阶段
- `xiaohongshu_publisher.py:66`  
  print("✍️  文案智能体正在生成文案...")
- `xiaohongshu_publisher.py:69`  
  print(f"✓ 文案生成完成（{len(copy)}字）\n")
- `xiaohongshu_publisher.py:131`  
  "2. 修改文案\n"
- `xiaohongshu_publisher.py:161`  
  print("\n✍️  文案内容：")
- `xiaohongshu_publisher.py:191`  
  """修改文案"""
- `xiaohongshu_publisher.py:192`  
  print("\n当前文案：")
- `xiaohongshu_publisher.py:196`  
  print("1. 手动修改文案")
- `xiaohongshu_publisher.py:203`  
  new_copy = input("\n请输入新文案（直接回车保持原样）: ").strip()
- `xiaohongshu_publisher.py:206`  
  print("✓ 文案已更新")
- `xiaohongshu_publisher.py:218`  
  print("✓ 文案已重新生成")
- `agents\designer.py:9`  
  """图片智能体：生成符合文案的图片"""
- `agents\designer.py:25`  
  copywriting: 文案内容
- `agents\designer.py:34`  
  为主题"{theme}"的文案生成2-3张配图的AI绘画提示词。
- `agents\designer.py:36`  
  文案内容：
- `agents\planner.py:32`  
  3. 关键词：生成8-10个相关话题标签，包括主标签和长尾标签
- `agents\planner.py:33`  
  4. 文案风格：确定语调风格（亲切自然、专业严谨、活泼可爱等）
- `agents\reviewer.py:78`  
  # 检查文案长度
- `agents\reviewer.py:80`  
  issues.append("文案过短，建议至少100字")
- `agents\reviewer.py:82`  
  issues.append("文案过长，建议控制在1000字以内")
- `agents\reviewer.py:122`  
  文案：
- `agents\wechat_writer.py:32`  
  # 生成标题
- `agents\wechat_writer.py:35`  
  # 生成正文
- `agents\wechat_writer.py:53`  
  """生成文章标题"""
- `agents\wechat_writer.py:58`  
  作为微信公众号标题专家，请为以下内容生成5个吸引人的标题：
- `agents\wechat_writer.py:94`  
  logger.error("生成标题超时")
- `agents\wechat_writer.py:97`  
  logger.error(f"生成标题失败: {str(e)}")
- `agents\wechat_writer.py:101`  
  """生成文章正文（HTML格式）"""
- `agents\wechat_writer.py:152`  
  logger.error("生成正文超时")
- `agents\wechat_writer.py:155`  
  logger.error(f"生成正文失败: {str(e)}")
- `agents\writer.py:6`  
  """文案智能体：根据策略生成小红书风格文案"""
- `agents\writer.py:14`  
  根据主题和策略生成小红书文案
- `agents\writer.py:21`  
  str: 生成的文案内容
- `agents\writer.py:23`  
  logger.info(f"文案智能体开始生成文案，主题: {theme}")
- `agents\writer.py:26`  
  作为一个小红书爆款文案写手，请根据以下信息创作一篇吸引人的笔记文案：
- `agents\writer.py:34`  
  - 文案风格：{strategy.get('tone', '亲切自然，带emoji')}
- `agents\writer.py:37`  
  文案要求：
- `agents\writer.py:45`  
  请直接输出文案内容，不要添加其他说明文字。
- `agents\writer.py:51`  
  {"role": "system", "content": "你是一个擅长创作小红书爆款文案的专家，深谙用户心理和平台算法。"},
- `agents\writer.py:59`  
  logger.info(f"文案生成成功，长度: {len(copywriting)}")
- `agents\writer.py:63`  
  logger.error(f"文案生成失败: {str(e)}")
- `agents\writer.py:67`  
  """获取默认文案模板"""
- `agents\writer.py:91`  
  根据用户反馈重写文案
- `agents\writer.py:94`  
  original_copy: 原始文案
- `agents\writer.py:99`  
  str: 重写后的文案
- `agents\writer.py:101`  
  logger.info(f"根据反馈重写文案: {feedback}")
- `agents\writer.py:104`  
  请根据以下反馈重写文案：
- `agents\writer.py:106`  
  原始文案：
- `agents\writer.py:111`  
  保持小红书风格，优化内容后直接输出文案。
- `agents\writer.py:117`  
  {"role": "system", "content": "你是一个小红书文案编辑专家。"},
- `agents\writer.py:125`  
  logger.info(f"文案重写成功")
- `agents\writer.py:129`  
  logger.error(f"文案重写失败: {str(e)}")
- `agents\writer.py:134`  
  生成多个标题选项
- `agents\writer.py:144`  
  为主题"{theme}"生成{count}个吸引人的小红书标题。
- `agents\writer.py:169`  
  logger.error(f"标题生成失败: {str(e)}")
- `API_SETUP_GUIDE.md:317`  
  A: 不是必须。如果配置了DALL-E 3或Stable Diffusion会生成图片，否则只生成文案。
- `auto_generated_documentation.md:8`  
  - 🟡 架构风格: 多智能体流水线（策划→文案→设计→审核→发布）
- `auto_generated_documentation.md:20`  
  - 🟢 文案智能体: 标题+正文生成，带 emoji/标签
- `auto_generated_documentation.md:21`  
  - 🟢 设计智能体: 根据文案调用 SD 生成配图
- `project_requirements_generated.md:17`  
  - **三级功能点**：文案智能体
- `project_requirements_generated.md:18`  
  **需求描述**：生成标题与正文
- `project_requirements_generated.md:22`  
  **需求描述**：根据文案生成配图
- `project_requirements_generated.md:24`  
  **数据来源**：文案文本、模型权重
- `PROJECT_STATUS.md:18`  
  - [x] 文案智能体 (agents/writer.py)
- `PROJECT_STATUS.md:74`  
  │   ├── writer.py               # 文案智能体
- `PROJECT_STATUS.md:120`  
  - [ ] Stable Diffusion（图片生成，如不安装则只生成文案）
- `PROJECT_STATUS.md:170`  
  ✅ 小红书风格文案
- `prompt_library_generated.md:4`  
  ## 文案生成
- `prompt_library_generated.md:6`  
  ("agents/writer.py", "文案智能体"),
- `prompt_library_generated.md:8`  
  # 2. 文案生成阶段
- `prompt_library_generated.md:10`  
  print("✍️  文案智能体正在生成文案...")
- `prompt_library_generated.md:12`  
  print(f"✓ 文案生成完成（{len(copy)}字）\n")
- `prompt_library_generated.md:14`  
  "2. 修改文案\n"
- `prompt_library_generated.md:16`  
  print("\n✍️  文案内容：")
- `prompt_library_generated.md:18`  
  """修改文案"""
- `prompt_library_generated.md:20`  
  print("\n当前文案：")
- `prompt_library_generated.md:22`  
  print("1. 手动修改文案")
- `prompt_library_generated.md:24`  
  new_copy = input("\n请输入新文案（直接回车保持原样）: ").strip()
- `prompt_library_generated.md:26`  
  print("✓ 文案已更新")
- `prompt_library_generated.md:28`  
  print("✓ 文案已重新生成")
- `prompt_library_generated.md:30`  
  """图片智能体：生成符合文案的图片"""
- `prompt_library_generated.md:32`  
  copywriting: 文案内容
- `prompt_library_generated.md:34`  
  为主题"{theme}"的文案生成2-3张配图的AI绘画提示词。
- `prompt_library_generated.md:36`  
  文案内容：
- `prompt_library_generated.md:38`  
  3. 关键词：生成8-10个相关话题标签，包括主标签和长尾标签
- `prompt_library_generated.md:40`  
  4. 文案风格：确定语调风格（亲切自然、专业严谨、活泼可爱等）
- `prompt_library_generated.md:42`  
  # 检查文案长度
- `prompt_library_generated.md:44`  
  issues.append("文案过短，建议至少100字")
- `prompt_library_generated.md:46`  
  issues.append("文案过长，建议控制在1000字以内")
- `prompt_library_generated.md:48`  
  文案：
- `prompt_library_generated.md:50`  
  # 生成标题
- `prompt_library_generated.md:52`  
  # 生成正文
- `prompt_library_generated.md:54`  
  """生成文章标题"""
- `prompt_library_generated.md:56`  
  作为微信公众号标题专家，请为以下内容生成5个吸引人的标题：
- `prompt_library_generated.md:58`  
  logger.error("生成标题超时")
- `prompt_library_generated.md:60`  
  logger.error(f"生成标题失败: {str(e)}")
- `prompt_library_generated.md:62`  
  """生成文章正文（HTML格式）"""
- `prompt_library_generated.md:64`  
  logger.error("生成正文超时")
- `prompt_library_generated.md:66`  
  logger.error(f"生成正文失败: {str(e)}")
- `prompt_library_generated.md:68`  
  """文案智能体：根据策略生成小红书风格文案"""
- `prompt_library_generated.md:70`  
  根据主题和策略生成小红书文案
- `prompt_library_generated.md:72`  
  str: 生成的文案内容
- `prompt_library_generated.md:74`  
  logger.info(f"文案智能体开始生成文案，主题: {theme}")
- `prompt_library_generated.md:76`  
  作为一个小红书爆款文案写手，请根据以下信息创作一篇吸引人的笔记文案：
- `prompt_library_generated.md:78`  
  - 文案风格：{strategy.get('tone', '亲切自然，带emoji')}
- `prompt_library_generated.md:80`  
  文案要求：
- `prompt_library_generated.md:82`  
  请直接输出文案内容，不要添加其他说明文字。
- `prompt_library_generated.md:84`  
  {"role": "system", "content": "你是一个擅长创作小红书爆款文案的专家，深谙用户心理和平台算法。"},
- `prompt_library_generated.md:86`  
  logger.info(f"文案生成成功，长度: {len(copywriting)}")
- `prompt_library_generated.md:88`  
  logger.error(f"文案生成失败: {str(e)}")
- `prompt_library_generated.md:90`  
  """获取默认文案模板"""
- `prompt_library_generated.md:92`  
  根据用户反馈重写文案
- `prompt_library_generated.md:94`  
  original_copy: 原始文案
- `prompt_library_generated.md:96`  
  str: 重写后的文案
- `prompt_library_generated.md:98`  
  logger.info(f"根据反馈重写文案: {feedback}")
- `prompt_library_generated.md:100`  
  请根据以下反馈重写文案：
- `prompt_library_generated.md:102`  
  原始文案：
- `prompt_library_generated.md:104`  
  保持小红书风格，优化内容后直接输出文案。
- `prompt_library_generated.md:106`  
  {"role": "system", "content": "你是一个小红书文案编辑专家。"},
- `prompt_library_generated.md:108`  
  logger.info(f"文案重写成功")
- `prompt_library_generated.md:110`  
  logger.error(f"文案重写失败: {str(e)}")
- `prompt_library_generated.md:112`  
  生成多个标题选项
- `prompt_library_generated.md:114`  
  为主题"{theme}"生成{count}个吸引人的小红书标题。
- `prompt_library_generated.md:116`  
  logger.error(f"标题生成失败: {str(e)}")
- `prompt_library_generated.md:118`  
  A: 不是必须。如果配置了DALL-E 3或Stable Diffusion会生成图片，否则只生成文案。
- `prompt_library_generated.md:120`  
  - 🟡 架构风格: 多智能体流水线（策划→文案→设计→审核→发布）
- `prompt_library_generated.md:122`  
  - 🟢 文案智能体: 标题+正文生成，带 emoji/标签
- `prompt_library_generated.md:124`  
  - 🟢 设计智能体: 根据文案调用 SD 生成配图
- `prompt_library_generated.md:126`  
  - **三级功能点**：文案智能体
- `prompt_library_generated.md:128`  
  **需求描述**：生成标题与正文
- `prompt_library_generated.md:130`  
  **需求描述**：根据文案生成配图
- `prompt_library_generated.md:132`  
  **数据来源**：文案文本、模型权重
- `prompt_library_generated.md:134`  
  - [x] 文案智能体 (agents/writer.py)
- `prompt_library_generated.md:136`  
  │   ├── writer.py               # 文案智能体
- `prompt_library_generated.md:138`  
  - [ ] Stable Diffusion（图片生成，如不安装则只生成文案）
- `prompt_library_generated.md:140`  
  ✅ 小红书风格文案
- `prompt_library_generated.md:142`  
  ## 文案生成
- `prompt_library_generated.md:144`  
  ("agents/writer.py", "文案智能体"),
- `prompt_library_generated.md:146`  
  # 2. 文案生成阶段
- `prompt_library_generated.md:148`  
  print("✍️  文案智能体正在生成文案...")
- `prompt_library_generated.md:150`  
  print(f"✓ 文案生成完成（{len(copy)}字）\n")
- `prompt_library_generated.md:152`  
  "2. 修改文案\n"
- `prompt_library_generated.md:154`  
  print("\n✍️  文案内容：")
- `prompt_library_generated.md:156`  
  """修改文案"""
- `prompt_library_generated.md:158`  
  print("\n当前文案：")
- `prompt_library_generated.md:160`  
  print("1. 手动修改文案")
- `prompt_library_generated.md:162`  
  new_copy = input("\n请输入新文案（直接回车保持原样）: ").strip()
- `prompt_library_generated.md:164`  
  print("✓ 文案已更新")
- `prompt_library_generated.md:166`  
  print("✓ 文案已重新生成")
- `prompt_library_generated.md:168`  
  """图片智能体：生成符合文案的图片"""
- `prompt_library_generated.md:170`  
  copywriting: 文案内容
- `prompt_library_generated.md:172`  
  为主题"{theme}"的文案生成2-3张配图的AI绘画提示词。
- `prompt_library_generated.md:174`  
  文案内容：
- `prompt_library_generated.md:176`  
  3. 关键词：生成8-10个相关话题标签，包括主标签和长尾标签
- `prompt_library_generated.md:178`  
  4. 文案风格：确定语调风格（亲切自然、专业严谨、活泼可爱等）
- `prompt_library_generated.md:180`  
  # 检查文案长度
- `prompt_library_generated.md:182`  
  issues.append("文案过短，建议至少100字")
- `prompt_library_generated.md:184`  
  issues.append("文案过长，建议控制在1000字以内")
- `prompt_library_generated.md:186`  
  文案：
- `prompt_library_generated.md:188`  
  # 生成标题
- `prompt_library_generated.md:190`  
  # 生成正文
- `prompt_library_generated.md:192`  
  """生成文章标题"""
- `prompt_library_generated.md:194`  
  作为微信公众号标题专家，请为以下内容生成5个吸引人的标题：
- `prompt_library_generated.md:196`  
  logger.error("生成标题超时")
- `prompt_library_generated.md:198`  
  logger.error(f"生成标题失败: {str(e)}")
- `prompt_library_generated.md:200`  
  """生成文章正文（HTML格式）"""
- `prompt_library_generated.md:202`  
  logger.error("生成正文超时")
- `prompt_library_generated.md:204`  
  logger.error(f"生成正文失败: {str(e)}")
- `prompt_library_generated.md:206`  
  """文案智能体：根据策略生成小红书风格文案"""
- `prompt_library_generated.md:208`  
  根据主题和策略生成小红书文案
- `prompt_library_generated.md:210`  
  str: 生成的文案内容
- `prompt_library_generated.md:212`  
  logger.info(f"文案智能体开始生成文案，主题: {theme}")
- `prompt_library_generated.md:214`  
  作为一个小红书爆款文案写手，请根据以下信息创作一篇吸引人的笔记文案：
- `prompt_library_generated.md:216`  
  - 文案风格：{strategy.get('tone', '亲切自然，带emoji')}
- `prompt_library_generated.md:218`  
  文案要求：
- `prompt_library_generated.md:220`  
  请直接输出文案内容，不要添加其他说明文字。
- `prompt_library_generated.md:222`  
  {"role": "system", "content": "你是一个擅长创作小红书爆款文案的专家，深谙用户心理和平台算法。"},
- `prompt_library_generated.md:224`  
  logger.info(f"文案生成成功，长度: {len(copywriting)}")
- `prompt_library_generated.md:226`  
  logger.error(f"文案生成失败: {str(e)}")
- `prompt_library_generated.md:228`  
  """获取默认文案模板"""
- `prompt_library_generated.md:230`  
  根据用户反馈重写文案
- `prompt_library_generated.md:232`  
  original_copy: 原始文案
- `prompt_library_generated.md:234`  
  str: 重写后的文案
- `prompt_library_generated.md:236`  
  logger.info(f"根据反馈重写文案: {feedback}")
- `prompt_library_generated.md:238`  
  请根据以下反馈重写文案：
- `prompt_library_generated.md:240`  
  原始文案：
- `prompt_library_generated.md:242`  
  保持小红书风格，优化内容后直接输出文案。
- `prompt_library_generated.md:244`  
  {"role": "system", "content": "你是一个小红书文案编辑专家。"},
- `prompt_library_generated.md:246`  
  logger.info(f"文案重写成功")
- `prompt_library_generated.md:248`  
  logger.error(f"文案重写失败: {str(e)}")
- `prompt_library_generated.md:250`  
  生成多个标题选项
- `prompt_library_generated.md:252`  
  为主题"{theme}"生成{count}个吸引人的小红书标题。
- `prompt_library_generated.md:254`  
  logger.error(f"标题生成失败: {str(e)}")
- `prompt_library_generated.md:256`  
  A: 不是必须。如果配置了DALL-E 3或Stable Diffusion会生成图片，否则只生成文案。
- `prompt_library_generated.md:258`  
  - 🟡 架构风格: 多智能体流水线（策划→文案→设计→审核→发布）
- `prompt_library_generated.md:260`  
  - 🟢 文案智能体: 标题+正文生成，带 emoji/标签
- `prompt_library_generated.md:262`  
  - 🟢 设计智能体: 根据文案调用 SD 生成配图
- `prompt_library_generated.md:264`  
  - [x] 文案智能体 (agents/writer.py)
- `prompt_library_generated.md:266`  
  │   ├── writer.py               # 文案智能体
- `prompt_library_generated.md:268`  
  - [ ] Stable Diffusion（图片生成，如不安装则只生成文案）
- `prompt_library_generated.md:270`  
  ✅ 小红书风格文案
- `prompt_library_generated.md:272`  
  - **多智能体协作**：策划、文案、设计、审核、发布五个智能体分工协作
- `prompt_library_generated.md:274`  
  - **智能内容生成**：自动生成符合小红书风格的文案和配图
- `prompt_library_generated.md:276`  
  【文案智能体】根据策略生成小红书风格文案
- `prompt_library_generated.md:278`  
  【图片智能体】生成符合文案的配图
- `prompt_library_generated.md:280`  
  - 生成关键词和话题标签
- `prompt_library_generated.md:282`  
  ### 2. 文案智能体 (CopyWriter)
- `prompt_library_generated.md:284`  
  - 根据策略生成小红书风格文案
- `prompt_library_generated.md:286`  
  │   ├── writer.py         # 文案智能体
- `prompt_library_generated.md:288`  
  - 自动生成小红书风格文案
- `prompt_library_generated.md:290`  
  2. 生成文案
- `prompt_library_generated.md:292`  
  2. 修改文案
- `prompt_library_generated.md:294`  
  生成关键词和话题标签
- `prompt_library_generated.md:296`  
  ### 文案智能体
- `prompt_library_generated.md:298`  
  生成吸引人的标题
- `prompt_library_generated.md:300`  
  输出完整文案
- `prompt_library_generated.md:302`  
  接收文案和策略
- `prompt_library_generated.md:304`  
  ### 2. 文案修改技巧
- `prompt_library_generated.md:306`  
  如果对生成的文案不满意：
- `prompt_library_generated.md:308`  
  1. 选择"修改文案"
- `prompt_library_generated.md:310`  
  ### Q2: 文案质量不满意？
- `prompt_library_generated.md:312`  
  2. 选择"修改文案"
- `prompt_library_generated.md:314`  
  4. 或手动编辑文案
- `prompt_library_generated.md:316`  
  - 未安装Stable Diffusion时系统只会生成文案
- `prompt_library_generated.md:318`  
  - **图片生成**: Stable Diffusion（未安装则只生成文案）
- `prompt_library_generated.md:320`  
  **A:** 图片生成是可选的，未安装时系统只会生成文案，不影响使用
- `prompt_library_generated.md:322`  
  - 生成文章标题和正文
- `prompt_library_generated.md:324`  
  - 生成标题
- `prompt_library_generated.md:326`  
  - 生成文章（标题+正文）
- `prompt_library_generated.md:328`  
  3. 查看生成的文章预览（标题、作者、正文）
- `prompt_library_generated.md:330`  
  - **多智能体协作**：策划、文案、设计、审核、发布五个智能体分工协作
- `prompt_library_generated.md:332`  
  - **智能内容生成**：自动生成符合小红书风格的文案和配图
- `prompt_library_generated.md:334`  
  【文案智能体】根据策略生成小红书风格文案
- `prompt_library_generated.md:336`  
  【图片智能体】生成符合文案的配图
- `prompt_library_generated.md:338`  
  - 生成关键词和话题标签
- `prompt_library_generated.md:340`  
  ### 2. 文案智能体 (CopyWriter)
- `prompt_library_generated.md:342`  
  - 根据策略生成小红书风格文案
- `prompt_library_generated.md:344`  
  │   ├── writer.py         # 文案智能体
- `prompt_library_generated.md:346`  
  - 自动生成小红书风格文案
- `prompt_library_generated.md:348`  
  2. 生成文案
- `prompt_library_generated.md:350`  
  2. 修改文案
- `prompt_library_generated.md:352`  
  生成关键词和话题标签
- `prompt_library_generated.md:354`  
  ### 文案智能体
- `prompt_library_generated.md:356`  
  生成吸引人的标题
- `prompt_library_generated.md:358`  
  输出完整文案
- `prompt_library_generated.md:360`  
  接收文案和策略
- `prompt_library_generated.md:362`  
  ### 2. 文案修改技巧
- `prompt_library_generated.md:364`  
  如果对生成的文案不满意：
- `prompt_library_generated.md:366`  
  1. 选择"修改文案"
- `prompt_library_generated.md:368`  
  ### Q2: 文案质量不满意？
- `prompt_library_generated.md:370`  
  2. 选择"修改文案"
- `prompt_library_generated.md:372`  
  4. 或手动编辑文案
- `prompt_library_generated.md:374`  
  - 未安装Stable Diffusion时系统只会生成文案
- `prompt_library_generated.md:376`  
  - **图片生成**: Stable Diffusion（未安装则只生成文案）
- `prompt_library_generated.md:378`  
  **A:** 图片生成是可选的，未安装时系统只会生成文案，不影响使用
- `prompt_library_generated.md:380`  
  - 生成文章标题和正文
- `prompt_library_generated.md:382`  
  - 生成标题
- `prompt_library_generated.md:384`  
  - 生成文章（标题+正文）
- `prompt_library_generated.md:386`  
  3. 查看生成的文章预览（标题、作者、正文）
- `README.md:9`  
  - **多智能体协作**：策划、文案、设计、审核、发布五个智能体分工协作
- `README.md:10`  
  - **智能内容生成**：自动生成符合小红书风格的文案和配图
- `README.md:54`  
  【文案智能体】根据策略生成小红书风格文案
- `README.md:56`  
  【图片智能体】生成符合文案的配图
- `README.md:149`  
  - 生成关键词和话题标签
- `README.md:151`  
  ### 2. 文案智能体 (CopyWriter)
- `README.md:152`  
  - 根据策略生成小红书风格文案
- `README.md:185`  
  │   ├── writer.py         # 文案智能体
- `使用指南.md:12`  
  - 自动生成小红书风格文案
- `使用指南.md:69`  
  2. 生成文案
- `使用指南.md:113`  
  2. 修改文案
- `使用指南.md:169`  
  生成关键词和话题标签
- `使用指南.md:174`  
  ### 文案智能体
- `使用指南.md:178`  
  生成吸引人的标题
- `使用指南.md:186`  
  输出完整文案
- `使用指南.md:191`  
  接收文案和策略
- `使用指南.md:241`  
  ### 2. 文案修改技巧
- `使用指南.md:243`  
  如果对生成的文案不满意：
- `使用指南.md:246`  
  1. 选择"修改文案"
- `使用指南.md:305`  
  ### Q2: 文案质量不满意？
- `使用指南.md:309`  
  2. 选择"修改文案"
- `使用指南.md:311`  
  4. 或手动编辑文案
- `使用指南.md:317`  
  - 未安装Stable Diffusion时系统只会生成文案
- `启动说明.md:123`  
  - **图片生成**: Stable Diffusion（未安装则只生成文案）
- `启动说明.md:146`  
  **A:** 图片生成是可选的，未安装时系统只会生成文案，不影响使用
- `微信公众号使用指南.md:69`  
  - 生成文章标题和正文
- `微信公众号使用指南.md:141`  
  - 生成标题
- `web\README.md:56`  
  - 生成文章（标题+正文）
- `web\README.md:64`  
  3. 查看生成的文章预览（标题、作者、正文）

## 智能体协作
- `launcher.py:33`  
  print("小红书多智能体内容生成系统 - 启动器".center(70))
- `main.py:4`  
  小红书多智能体内容生成与发布系统
- `main.py:29`  
  ║          小红书多智能体内容生成与发布系统                  ║
- `setup_check.py:46`  
  ("agents/designer.py", "图片智能体"),
- `test_generate.py:3`  
  """测试文章生成流程"""
- `wechat_main.py:4`  
  微信公众号多智能体内容生成与发布系统
- `wechat_main.py:48`  
  多智能体协同工作流：处理主题生成公众号文章
- `wechat_main.py:224`  
  ║        微信公众号多智能体内容生成与发布系统                ║
- `xiaohongshu_publisher.py:28`  
  多智能体协同工作流：处理主题生成内容
- `xiaohongshu_publisher.py:72`  
  print("🎨 图片智能体正在生成配图...")
- `agents\planner.py:6`  
  """策划智能体：分析主题，生成内容策略"""
- `auto_generated_documentation.md:6`  
  - 🟢 目标: 通过多智能体协作自动生成符合平台规范的图文内容并支持一键发布
- `auto_generated_documentation.md:12`  
  - 🟢 内容生成（智能体协作）
- `auto_generated_documentation.md:29`  
  用户请求 → 主程序(main.py) → 任务分发 → 各智能体(Agents) → AI模型/SD → 审核 → 发布
- `auto_generated_documentation.md:56`  
  - 🟢 核心流程完整（生成→审核→发布）
- `PROJECT_STATUS.md:19`  
  - [x] 图片智能体 (agents/designer.py)
- `PROJECT_STATUS.md:75`  
  │   ├── designer.py             # 图片智能体
- `prompt_library_generated.md:390`  
  print("小红书多智能体内容生成系统 - 启动器".center(70))
- `prompt_library_generated.md:392`  
  小红书多智能体内容生成与发布系统
- `prompt_library_generated.md:394`  
  ║          小红书多智能体内容生成与发布系统                  ║
- `prompt_library_generated.md:396`  
  ("agents/designer.py", "图片智能体"),
- `prompt_library_generated.md:398`  
  """测试文章生成流程"""
- `prompt_library_generated.md:400`  
  微信公众号多智能体内容生成与发布系统
- `prompt_library_generated.md:402`  
  多智能体协同工作流：处理主题生成公众号文章
- `prompt_library_generated.md:404`  
  ║        微信公众号多智能体内容生成与发布系统                ║
- `prompt_library_generated.md:406`  
  多智能体协同工作流：处理主题生成内容
- `prompt_library_generated.md:408`  
  print("🎨 图片智能体正在生成配图...")
- `prompt_library_generated.md:410`  
  """策划智能体：分析主题，生成内容策略"""
- `prompt_library_generated.md:412`  
  - 🟢 目标: 通过多智能体协作自动生成符合平台规范的图文内容并支持一键发布
- `prompt_library_generated.md:414`  
  - 🟢 内容生成（智能体协作）
- `prompt_library_generated.md:416`  
  用户请求 → 主程序(main.py) → 任务分发 → 各智能体(Agents) → AI模型/SD → 审核 → 发布
- `prompt_library_generated.md:418`  
  - 🟢 核心流程完整（生成→审核→发布）
- `prompt_library_generated.md:420`  
  - [x] 图片智能体 (agents/designer.py)
- `prompt_library_generated.md:422`  
  │   ├── designer.py             # 图片智能体
- `prompt_library_generated.md:424`  
  print("小红书多智能体内容生成系统 - 启动器".center(70))
- `prompt_library_generated.md:426`  
  小红书多智能体内容生成与发布系统
- `prompt_library_generated.md:428`  
  ║          小红书多智能体内容生成与发布系统                  ║
- `prompt_library_generated.md:430`  
  ("agents/designer.py", "图片智能体"),
- `prompt_library_generated.md:432`  
  """测试文章生成流程"""
- `prompt_library_generated.md:434`  
  微信公众号多智能体内容生成与发布系统
- `prompt_library_generated.md:436`  
  多智能体协同工作流：处理主题生成公众号文章
- `prompt_library_generated.md:438`  
  ║        微信公众号多智能体内容生成与发布系统                ║
- `prompt_library_generated.md:440`  
  多智能体协同工作流：处理主题生成内容
- `prompt_library_generated.md:442`  
  print("🎨 图片智能体正在生成配图...")
- `prompt_library_generated.md:444`  
  """策划智能体：分析主题，生成内容策略"""
- `prompt_library_generated.md:446`  
  - 🟢 目标: 通过多智能体协作自动生成符合平台规范的图文内容并支持一键发布
- `prompt_library_generated.md:448`  
  - 🟢 内容生成（智能体协作）
- `prompt_library_generated.md:450`  
  用户请求 → 主程序(main.py) → 任务分发 → 各智能体(Agents) → AI模型/SD → 审核 → 发布
- `prompt_library_generated.md:452`  
  - 🟢 核心流程完整（生成→审核→发布）
- `prompt_library_generated.md:454`  
  - [x] 图片智能体 (agents/designer.py)
- `prompt_library_generated.md:456`  
  │   ├── designer.py             # 图片智能体
- `prompt_library_generated.md:458`  
  小红书多智能体内容生成系统 - 启动器
- `prompt_library_generated.md:460`  
  # 小红书多智能体内容生成与发布系统
- `prompt_library_generated.md:462`  
  基于AI多智能体协作的小红书自动化内容生成与发布系统。
- `prompt_library_generated.md:464`  
  【策划智能体】分析主题，生成内容策略
- `prompt_library_generated.md:466`  
  ### 3. 图片智能体 (ImageDesigner)
- `prompt_library_generated.md:468`  
  │   ├── designer.py       # 图片智能体
- `prompt_library_generated.md:470`  
  # 📱 小红书多智能体内容生成系统 - 使用指南
- `prompt_library_generated.md:472`  
  这是一个基于AI多智能体协作的小红书自动化内容生成与发布系统。
- `prompt_library_generated.md:474`  
  享受多智能体协作生成小红书内容！🎉
- `prompt_library_generated.md:476`  
  本系统是基于多智能体架构的微信公众号内容生成与发布平台，支持：
- `prompt_library_generated.md:478`  
  3. 设计智能体 (ImageDesigner)
- `prompt_library_generated.md:480`  
  │   ├── designer.py             # 设计智能体
- `prompt_library_generated.md:482`  
  开始使用小红书多智能体内容生成系统了！
- `prompt_library_generated.md:484`  
  - designer.py - 设计智能体
- `prompt_library_generated.md:486`  
  2. 写作智能体生成文章
- `prompt_library_generated.md:488`  
  3. 设计智能体生成配图（可选）
- `prompt_library_generated.md:490`  
  小红书多智能体内容生成系统 - 启动器
- `prompt_library_generated.md:492`  
  # 小红书多智能体内容生成与发布系统
- `prompt_library_generated.md:494`  
  基于AI多智能体协作的小红书自动化内容生成与发布系统。
- `prompt_library_generated.md:496`  
  【策划智能体】分析主题，生成内容策略
- `prompt_library_generated.md:498`  
  ### 3. 图片智能体 (ImageDesigner)
- `prompt_library_generated.md:500`  
  │   ├── designer.py       # 图片智能体
- `prompt_library_generated.md:502`  
  # 📱 小红书多智能体内容生成系统 - 使用指南
- `prompt_library_generated.md:504`  
  这是一个基于AI多智能体协作的小红书自动化内容生成与发布系统。
- `prompt_library_generated.md:506`  
  享受多智能体协作生成小红书内容！🎉
- `prompt_library_generated.md:508`  
  本系统是基于多智能体架构的微信公众号内容生成与发布平台，支持：
- `prompt_library_generated.md:510`  
  3. 设计智能体 (ImageDesigner)
- `prompt_library_generated.md:512`  
  │   ├── designer.py             # 设计智能体
- `prompt_library_generated.md:514`  
  开始使用小红书多智能体内容生成系统了！
- `prompt_library_generated.md:516`  
  - designer.py - 设计智能体
- `prompt_library_generated.md:518`  
  2. 写作智能体生成文章
- `prompt_library_generated.md:520`  
  3. 设计智能体生成配图（可选）
- `Python已安装但仍无法运行.md:210`  
  小红书多智能体内容生成系统 - 启动器
- `README.md:1`  
  # 小红书多智能体内容生成与发布系统
- `README.md:3`  
  基于AI多智能体协作的小红书自动化内容生成与发布系统。
- `README.md:52`  
  【策划智能体】分析主题，生成内容策略
- `README.md:156`  
  ### 3. 图片智能体 (ImageDesigner)
- `README.md:186`  
  │   ├── designer.py       # 图片智能体
- `使用指南.md:1`  
  # 📱 小红书多智能体内容生成系统 - 使用指南
- `使用指南.md:7`  
  这是一个基于AI多智能体协作的小红书自动化内容生成与发布系统。
- `启动说明.md:158`  
  享受多智能体协作生成小红书内容！🎉
- `微信公众号使用指南.md:5`  
  本系统是基于多智能体架构的微信公众号内容生成与发布平台，支持：
- `微信公众号使用指南.md:146`  
  3. 设计智能体 (ImageDesigner)
- `微信公众号使用指南.md:273`  
  │   ├── designer.py             # 设计智能体
- `问题解决方案.md:199`  
  开始使用小红书多智能体内容生成系统了！
- `web\README.md:127`  
  - designer.py - 设计智能体
- `web\README.md:144`  
  2. 写作智能体生成文章
- `web\README.md:146`  
  3. 设计智能体生成配图（可选）

## 产品设计
- `prompt_library_generated.md:524`  
  这是一个基于 Flask 的 Web 界面，提供微信公众号内容生成与发布功能的可视化操作界面。
- `prompt_library_generated.md:526`  
  这是一个基于 Flask 的 Web 界面，提供微信公众号内容生成与发布功能的可视化操作界面。
- `web\README.md:5`  
  这是一个基于 Flask 的 Web 界面，提供微信公众号内容生成与发布功能的可视化操作界面。

## 创新功能
- `project_requirements_generated.md:1`  
  # 项目功能需求分析 - 自动生成
- `prompt_library_generated.md:530`  
  # 项目功能需求分析 - 自动生成
- `prompt_library_generated.md:532`  
  - 结合 `project-analyzer` 输出的功能点直接生成对应提示词
- `prompt_library_generated.md:534`  
  | **auto-doc-generator** | 自动分析代码结构，生成带完整性标记的项目文档（🔴🟡🟢） | 需要结构化文档生成、功能规格、架构说明、完整性报告 | `auto_generated_documentation.md` | `.codebuddy/skills/auto-doc-generator/` |
- `prompt_library_generated.md:536`  
  | **project-analyzer** | 扫描项目目录，自动推导一至三级功能点及调用方式、数据来源 | 快速了解项目功能结构、生成功能需求清单 | `project_requirements_generated.md` | `.codebuddy/skills/project-analyzer/` |
- `prompt_library_generated.md:1856`  
  - 结合 `project-analyzer` 输出的功能点直接生成对应提示词
- `SKILL_REGISTRY.md:7`  
  | **auto-doc-generator** | 自动分析代码结构，生成带完整性标记的项目文档（🔴🟡🟢） | 需要结构化文档生成、功能规格、架构说明、完整性报告 | `auto_generated_documentation.md` | `.codebuddy/skills/auto-doc-generator/` |
- `SKILL_REGISTRY.md:8`  
  | **project-analyzer** | 扫描项目目录，自动推导一至三级功能点及调用方式、数据来源 | 快速了解项目功能结构、生成功能需求清单 | `project_requirements_generated.md` | `.codebuddy/skills/project-analyzer/` |

## 验证优化
- `test_generate.py:13`  
  print("开始测试文章生成...")
- `agents\planner.py:98`  
  根据用户反馈优化内容策略
- `agents\planner.py:107`  
  logger.info(f"根据用户反馈优化策略: {user_feedback}")
- `agents\planner.py:110`  
  基于以下内容策略和用户反馈，优化内容策略：
- `prompt_library_generated.md:540`  
  print("开始测试文章生成...")
- `prompt_library_generated.md:542`  
  根据用户反馈优化内容策略
- `prompt_library_generated.md:544`  
  logger.info(f"根据用户反馈优化策略: {user_feedback}")
- `prompt_library_generated.md:546`  
  基于以下内容策略和用户反馈，优化内容策略：
- `prompt_library_generated.md:548`  
  print("开始测试文章生成...")
- `prompt_library_generated.md:550`  
  根据用户反馈优化内容策略
- `prompt_library_generated.md:552`  
  logger.info(f"根据用户反馈优化策略: {user_feedback}")
- `prompt_library_generated.md:554`  
  基于以下内容策略和用户反馈，优化内容策略：
- `prompt_library_generated.md:556`  
  - 输出：每个 Skill 的执行状态及生成文档清单，便于快速验证
- `SKILL_REGISTRY.md:27`  
  - 输出：每个 Skill 的执行状态及生成文档清单，便于快速验证

## 其他
- `ai_client.py:93`  
  def generate_image(self, prompt, **kwargs):
- `ai_client.py:95`  
  生成图片（仅OpenAI支持）
- `ai_client.py:98`  
  prompt: 图片提示词
- `ai_client.py:107`  
  prompt=prompt,
- `ai_client.py:113`  
  logger.error(f"图片生成失败: {str(e)}")
- `config.py:49`  
  # 图片生成引擎
- `main.py:46`  
  2. 生成预览 - 生成内容后确认
- `main.py:112`  
  # 生成内容
- `main.py:250`  
  print(f"\n图片生成引擎: {Config.IMAGE_ENGINE}")
- `run_all_skills_demo.py:13`  
  # 固定 Skill 根目录（用户目录下的 .codebuddy）
- `run_all_skills_demo.py:26`  
  "prompt-collector": (
- `run_all_skills_demo.py:27`  
  CODEBUDDY_ROOT / "prompt-collector" / "scripts" / "prompt_collector.py",
- `run_all_skills_demo.py:74`  
  # 列出生成的文档
- `run_all_skills_demo.py:76`  
  print("\n=== 生成文档清单（应在项目根目录）===")
- `run_all_skills_demo.py:80`  
  "prompt_library_generated.md",
- `setup_check.py:60`  
  ("generated_images", "图片生成目录"),
- `test_generate.py:23`  
  print("\n2. 开始生成文章...")
- `test_generate.py:30`  
  print("\n4. 生成完成!")
- `test_simple.py:33`  
  from agents.designer import ImageDesigner
- `test_simple.py:44`  
  'designer': ImageDesigner(),
- `test_simple_generate.py:23`  
  print("Step 4: 生成策略...")
- `test_simple_generate.py:36`  
  print("\nStep 5: 生成文章...")
- `test_simple_generate.py:40`  
  print("\n生成成功!")
- `test_simple_generate.py:45`  
  print(f"生成失败: {e}")
- `wechat_main.py:21`  
  from agents.designer import ImageDesigner
- `wechat_main.py:30`  
  """微信公众号内容生成与发布系统"""
- `wechat_main.py:39`  
  'designer': ImageDesigner(),
- `wechat_main.py:51`  
  theme: 用户输入的主题
- `wechat_main.py:54`  
  dict: 生成的内容包
- `wechat_main.py:65`  
  'image_prompts': None,
- `wechat_main.py:77`  
  # 2. 文章生成阶段
- `wechat_main.py:78`  
  print("【写作】生成公众号文章...")
- `wechat_main.py:84`  
  # 3. 图片生成阶段（可选）
- `wechat_main.py:85`  
  print("【配图】生成配图（可选）...")
- `wechat_main.py:86`  
  print("提示：已跳过图片生成\n")
- `wechat_main.py:87`  
  # Web 模式下跳过图片生成
- `wechat_main.py:88`  
  content_package['image_prompts'] = []
- `wechat_main.py:189`  
  """完整工作流：生成并发布"""
- `wechat_main.py:191`  
  # 生成内容
- `wechat_main.py:241`  
  2. 生成预览 - 生成文章后确认
- `wechat_main.py:306`  
  # 生成内容
- `wechat_main.py:445`  
  print(f"\n图片生成引擎: {Config.IMAGE_ENGINE}")
- `xiaohongshu_publisher.py:3`  
  from agents.designer import ImageDesigner
- `xiaohongshu_publisher.py:10`  
  """小红书内容生成与发布系统"""
- `xiaohongshu_publisher.py:19`  
  'designer': ImageDesigner(),
- `xiaohongshu_publisher.py:31`  
  theme: 用户输入的主题
- `xiaohongshu_publisher.py:34`  
  dict: 生成的内容包
- `xiaohongshu_publisher.py:39`  
  'image_prompts': list,
- `xiaohongshu_publisher.py:53`  
  'image_prompts': None,
- `xiaohongshu_publisher.py:71`  
  # 3. 图片生成阶段
- `xiaohongshu_publisher.py:73`  
  image_prompts = self.agents['designer'].generate_image_prompts(
- `xiaohongshu_publisher.py:76`  
  content_package['image_prompts'] = image_prompts
- `xiaohongshu_publisher.py:78`  
  print(f"✓ 生成{len(image_prompts)}个图片提示词:")
- `xiaohongshu_publisher.py:79`  
  for idx, prompt in enumerate(image_prompts):
- `xiaohongshu_publisher.py:80`  
  print(f"  {idx+1}. {prompt[:50]}...")
- `xiaohongshu_publisher.py:82`  
  print(f"\n正在生成图片...")
- `xiaohongshu_publisher.py:83`  
  image_paths = self.agents['designer'].generate_images(image_prompts)
- `xiaohongshu_publisher.py:85`  
  print(f"✓ 成功生成{len(image_paths)}张图片\n")
- `xiaohongshu_publisher.py:105`  
  print("内容生成完成！")
- `xiaohongshu_publisher.py:112`  
  logger.error(f"内容生成失败: {str(e)}")
- `xiaohongshu_publisher.py:113`  
  print(f"✗ 内容生成失败: {str(e)}\n")
- `xiaohongshu_publisher.py:132`  
  "3. 重新生成图片\n"
- `xiaohongshu_publisher.py:172`  
  print("  未生成图片")
- `xiaohongshu_publisher.py:197`  
  print("2. 让AI重新生成")
- `xiaohongshu_publisher.py:221`  
  """重新生成图片"""
- `xiaohongshu_publisher.py:222`  
  print("\n重新生成图片选项:")
- `xiaohongshu_publisher.py:229`  
  # 重新生成所有图片
- `xiaohongshu_publisher.py:230`  
  prompts = content_package.get('image_prompts', [])
- `xiaohongshu_publisher.py:231`  
  if prompts:
- `xiaohongshu_publisher.py:233`  
  for idx, prompt in enumerate(prompts):
- `xiaohongshu_publisher.py:234`  
  print(f"{idx+1}. {prompt}")
- `xiaohongshu_publisher.py:238`  
  new_prompt = input("输入新提示词（留空保持）: ")
- `xiaohongshu_publisher.py:239`  
  if new_prompt:
- `xiaohongshu_publisher.py:240`  
  prompts = [new_prompt]
- `xiaohongshu_publisher.py:242`  
  new_paths = self.agents['designer'].generate_images(prompts)
- `xiaohongshu_publisher.py:244`  
  print("✓ 图片已重新生成")
- `xiaohongshu_publisher.py:253`  
  idx = int(input("\n选择要重新生成的图片编号: ")) - 1
- `xiaohongshu_publisher.py:255`  
  new_prompt = input("输入新提示词: ")
- `xiaohongshu_publisher.py:256`  
  if new_prompt:
- `xiaohongshu_publisher.py:257`  
  new_path = self.agents['designer'].regenerate_image(
- `xiaohongshu_publisher.py:259`  
  new_prompt
- `xiaohongshu_publisher.py:262`  
  print("✓ 图片已重新生成")
- `xiaohongshu_publisher.py:306`  
  完整工作流：生成 → 确认 → 发布
- `xiaohongshu_publisher.py:315`  
  # 生成内容
- `xiaohongshu_publisher.py:334`  
  return {'success': False, 'message': '用户取消'}
- `agents\designer.py:8`  
  class ImageDesigner:
- `agents\designer.py:19`  
  def generate_image_prompts(self, theme: str, copywriting: str, strategy: dict) -> list:
- `agents\designer.py:21`  
  生成图片提示词
- `agents\designer.py:31`  
  logger.info("生成图片提示词")
- `agents\designer.py:33`  
  prompt = f"""
- `agents\designer.py:43`  
  请为小红书风格配图生成提示词，要求：
- `agents\designer.py:52`  
  "prompts": [
- `agents\designer.py:53`  
  "prompt1",
- `agents\designer.py:54`  
  "prompt2"
- `agents\designer.py:65`  
  {"role": "user", "content": prompt}
- `agents\designer.py:76`  
  prompts = result.get('prompts', [])
- `agents\designer.py:77`  
  logger.info(f"生成了{len(prompts)}个图片提示词")
- `agents\designer.py:78`  
  return prompts
- `agents\designer.py:81`  
  logger.error(f"提示词生成失败: {str(e)}")
- `agents\designer.py:82`  
  return self._get_default_prompts(theme)
- `agents\designer.py:84`  
  def _get_default_prompts(self, theme: str) -> list:
- `agents\designer.py:91`  
  def generate_images(self, prompts: list) -> list:
- `agents\designer.py:93`  
  根据提示词生成图片
- `agents\designer.py:96`  
  prompts: 图片提示词列表
- `agents\designer.py:99`  
  list: 生成的图片路径列表
- `agents\designer.py:101`  
  logger.info(f"开始生成{len(prompts)}张图片")
- `agents\designer.py:105`  
  for idx, prompt in enumerate(prompts):
- `agents\designer.py:107`  
  image_path = self._generate_single_image(prompt, idx)
- `agents\designer.py:112`  
  logger.error(f"生成第{idx+1}张图片失败: {str(e)}")
- `agents\designer.py:114`  
  logger.info(f"成功生成{len(image_paths)}张图片")
- `agents\designer.py:117`  
  def _generate_single_image(self, prompt: str, index: int) -> str:
- `agents\designer.py:119`  
  生成单张图片
- `agents\designer.py:122`  
  prompt: 提示词
- `agents\designer.py:129`  
  return self._generate_with_dalle(prompt, index)
- `agents\designer.py:131`  
  return self._generate_with_stable_diffusion(prompt, index)
- `agents\designer.py:133`  
  def _generate_with_dalle(self, prompt: str, index: int) -> str:
- `agents\designer.py:134`  
  """使用DALL-E 3生成图片"""
- `agents\designer.py:137`  
  prompt=prompt,
- `agents\designer.py:151`  
  logger.info(f"DALL-E生成图片成功: {image_path}")
- `agents\designer.py:155`  
  logger.error(f"DALL-E生成失败: {str(e)}")
- `agents\designer.py:158`  
  def _generate_with_stable_diffusion(self, prompt: str, index: int) -> str:
- `agents\designer.py:159`  
  """使用Stable Diffusion生成图片"""
- `agents\designer.py:163`  
  "prompt": prompt,
- `agents\designer.py:164`  
  "negative_prompt": "low quality, blurry, ugly, distorted",
- `agents\designer.py:184`  
  logger.info(f"Stable Diffusion生成图片成功: {image_path}")
- `agents\designer.py:188`  
  logger.error(f"Stable Diffusion生成失败: {str(e)}")
- `agents\designer.py:191`  
  def regenerate_image(self, old_path: str, new_prompt: str) -> str:
- `agents\designer.py:193`  
  重新生成指定图片
- `agents\designer.py:197`  
  new_prompt: 新的提示词
- `agents\designer.py:202`  
  logger.info(f"重新生成图片: {old_path}")
- `agents\designer.py:207`  
  return self._generate_single_image(new_prompt, index)
- `agents\planner.py:14`  
  分析主题，生成内容策略
- `agents\planner.py:17`  
  theme: 用户输入的主题
- `agents\planner.py:24`  
  prompt = f"""
- `agents\planner.py:58`  
  {"role": "user", "content": prompt}
- `agents\planner.py:76`  
  logger.info(f"内容策略生成成功: {strategy}")
- `agents\planner.py:80`  
  logger.error(f"内容策略生成失败: {str(e)}")
- `agents\planner.py:102`  
  user_feedback: 用户反馈意见
- `agents\planner.py:109`  
  prompt = f"""
- `agents\planner.py:113`  
  用户反馈：{user_feedback}
- `agents\planner.py:124`  
  {"role": "user", "content": prompt}
- `agents\reviewer.py:117`  
  prompt = f"""
- `agents\reviewer.py:147`  
  {"role": "user", "content": prompt}
- `agents\reviewer.py:202`  
  """生成摘要"""
- `agents\wechat_writer.py:14`  
  生成微信公众号文章
- `agents\wechat_writer.py:30`  
  logger.info(f"开始生成公众号文章，主题: {theme}")
- `agents\wechat_writer.py:38`  
  # 生成摘要
- `agents\wechat_writer.py:57`  
  prompt = f"""
- `agents\wechat_writer.py:79`  
  messages=[{'role': 'user', 'content': prompt}],
- `agents\wechat_writer.py:107`  
  prompt = f"""
- `agents\wechat_writer.py:139`  
  messages=[{'role': 'user', 'content': prompt}],
- `agents\wechat_writer.py:176`  
  """生成文章摘要"""
- `agents\writer.py:25`  
  prompt = f"""
- `agents\writer.py:52`  
  {"role": "user", "content": prompt}
- `agents\writer.py:95`  
  feedback: 用户反馈
- `agents\writer.py:103`  
  prompt = f"""
- `agents\writer.py:109`  
  用户反馈：{feedback}
- `agents\writer.py:118`  
  {"role": "user", "content": prompt}
- `agents\writer.py:143`  
  prompt = f"""
- `agents\writer.py:159`  
  {"role": "user", "content": prompt}
- `web\api_server.py:86`  
  """生成预览 - 异步处理"""
- `web\api_server.py:95`  
  print(f"\n收到生成预览请求: {theme}")
- `web\api_server.py:136`  
  print(f"生成预览失败: {e}")
- `web\api_server.py:141`  
  'message': f'生成失败: {str(e)}'
- `web\api_server_simple.py:57`  
  """异步生成预览"""
- `API_SETUP_GUIDE.md:11`  
  5. [图片生成方案](#5-图片生成方案)
- `API_SETUP_GUIDE.md:20`  
  ✅ **免费额度高**：新用户赠送500万Tokens（约相当于2000元OpenAI额度）
- `API_SETUP_GUIDE.md:42`  
  6. 复制生成的API Key（格式：sk-xxxxxxxx）
- `API_SETUP_GUIDE.md:73`  
  - 新用户免费额度：500万Tokens
- `API_SETUP_GUIDE.md:85`  
  ✅ 新用户赠送免费额度
- `API_SETUP_GUIDE.md:106`  
  2. 复制生成的Key
- `API_SETUP_GUIDE.md:117`  
  - 新用户免费试用
- `API_SETUP_GUIDE.md:129`  
  ✅ 新用户免费额度
- `API_SETUP_GUIDE.md:155`  
  - 新用户免费额度
- `API_SETUP_GUIDE.md:168`  
  ✅ 新用户免费额度
- `API_SETUP_GUIDE.md:194`  
  - 新用户免费额度
- `API_SETUP_GUIDE.md:200`  
  ## 5. 图片生成方案
- `API_SETUP_GUIDE.md:243`  
  # 复制配置模板
- `API_SETUP_GUIDE.md:284`  
  | 服务商 | 新用户免费 | 价格 | 速度 | 中文支持 | 推荐度 |
- `API_SETUP_GUIDE.md:315`  
  ### Q4: 图片生成必须配置吗？
- `auto_generated_documentation.md:1`  
  # 自动生成项目文档 - 20260206205332
- `auto_generated_documentation.md:2`  
  > 生成时间: 2026-02-11 17:27
- `auto_generated_documentation.md:5`  
  - 🟢 项目名称: 小红书内容生成与发布平台
- `auto_generated_documentation.md:13`  
  - 🟢 图片生成（Stable Diffusion）
- `auto_generated_documentation.md:48`  
  - 🔴 持久化用户数据与内容库（建议补充）
- `project_requirements_generated.md:2`  
  > 生成时间: 2026-02-11 17:27
- `project_requirements_generated.md:7`  
  **需求描述**：读取运行时设置
- `project_requirements_generated.md:14`  
  **需求描述**：分析市场热点，推荐选题
- `project_requirements_generated.md:20`  
  **数据来源**：AI模型、用户输入
- `project_requirements_generated.md:26`  
  **需求描述**：规则校验与敏感词检测
- `project_requirements_generated.md:33`  
  **需求描述**：读取运行时设置
- `project_requirements_generated.md:40`  
  **需求描述**：读取运行时设置
- `project_requirements_generated.md:47`  
  **需求描述**：读取运行时设置
- `project_requirements_generated.md:54`  
  **需求描述**：读取运行时设置
- `project_requirements_generated.md:61`  
  **需求描述**：读取运行时设置
- `PROJECT_STATUS.md:3`  
  生成时间: 2026-02-06
- `PROJECT_STATUS.md:32`  
  - [x] .env.example（配置模板）
- `PROJECT_STATUS.md:79`  
  ├── generated_images/            # 生成的图片目录
- `PROJECT_STATUS.md:90`  
  ├── .env.example                 # 配置模板
- `PROJECT_STATUS.md:149`  
  ### Windows用户
- `PROJECT_STATUS.md:169`  
  ✅ 内容策略生成
- `PROJECT_STATUS.md:171`  
  ✅ AI图片生成
- `PROJECT_STATUS.md:202`  
  开始使用系统生成小红书内容！🎉
- `prompt_library_generated.md:1`  
  # 提示词模板库 - 自动生成
- `prompt_library_generated.md:2`  
  > 生成时间: 2026-02-11 17:26
- `prompt_library_generated.md:29`  
  - `agents\designer.py:9`
- `prompt_library_generated.md:31`  
  - `agents\designer.py:25`
- `prompt_library_generated.md:33`  
  - `agents\designer.py:34`
- `prompt_library_generated.md:35`  
  - `agents\designer.py:36`
- `prompt_library_generated.md:141`  
  - `prompt_library_generated.md:4`
- `prompt_library_generated.md:143`  
  - `prompt_library_generated.md:6`
- `prompt_library_generated.md:145`  
  - `prompt_library_generated.md:8`
- `prompt_library_generated.md:147`  
  - `prompt_library_generated.md:10`
- `prompt_library_generated.md:149`  
  - `prompt_library_generated.md:12`
- `prompt_library_generated.md:151`  
  - `prompt_library_generated.md:14`
- `prompt_library_generated.md:153`  
  - `prompt_library_generated.md:16`
- `prompt_library_generated.md:155`  
  - `prompt_library_generated.md:18`
- `prompt_library_generated.md:157`  
  - `prompt_library_generated.md:20`
- `prompt_library_generated.md:159`  
  - `prompt_library_generated.md:22`
- `prompt_library_generated.md:161`  
  - `prompt_library_generated.md:24`
- `prompt_library_generated.md:163`  
  - `prompt_library_generated.md:26`
- `prompt_library_generated.md:165`  
  - `prompt_library_generated.md:28`
- `prompt_library_generated.md:167`  
  - `prompt_library_generated.md:30`
- `prompt_library_generated.md:169`  
  - `prompt_library_generated.md:32`
- `prompt_library_generated.md:171`  
  - `prompt_library_generated.md:34`
- `prompt_library_generated.md:173`  
  - `prompt_library_generated.md:36`
- `prompt_library_generated.md:175`  
  - `prompt_library_generated.md:38`
- `prompt_library_generated.md:177`  
  - `prompt_library_generated.md:40`
- `prompt_library_generated.md:179`  
  - `prompt_library_generated.md:42`
- `prompt_library_generated.md:181`  
  - `prompt_library_generated.md:44`
- `prompt_library_generated.md:183`  
  - `prompt_library_generated.md:46`
- `prompt_library_generated.md:185`  
  - `prompt_library_generated.md:48`
- `prompt_library_generated.md:187`  
  - `prompt_library_generated.md:50`
- `prompt_library_generated.md:189`  
  - `prompt_library_generated.md:52`
- `prompt_library_generated.md:191`  
  - `prompt_library_generated.md:54`
- `prompt_library_generated.md:193`  
  - `prompt_library_generated.md:56`
- `prompt_library_generated.md:195`  
  - `prompt_library_generated.md:58`
- `prompt_library_generated.md:197`  
  - `prompt_library_generated.md:60`
- `prompt_library_generated.md:199`  
  - `prompt_library_generated.md:62`
- `prompt_library_generated.md:201`  
  - `prompt_library_generated.md:64`
- `prompt_library_generated.md:203`  
  - `prompt_library_generated.md:66`
- `prompt_library_generated.md:205`  
  - `prompt_library_generated.md:68`
- `prompt_library_generated.md:207`  
  - `prompt_library_generated.md:70`
- `prompt_library_generated.md:209`  
  - `prompt_library_generated.md:72`
- `prompt_library_generated.md:211`  
  - `prompt_library_generated.md:74`
- `prompt_library_generated.md:213`  
  - `prompt_library_generated.md:76`
- `prompt_library_generated.md:215`  
  - `prompt_library_generated.md:78`
- `prompt_library_generated.md:217`  
  - `prompt_library_generated.md:80`
- `prompt_library_generated.md:219`  
  - `prompt_library_generated.md:82`
- `prompt_library_generated.md:221`  
  - `prompt_library_generated.md:84`
- `prompt_library_generated.md:223`  
  - `prompt_library_generated.md:86`
- `prompt_library_generated.md:225`  
  - `prompt_library_generated.md:88`
- `prompt_library_generated.md:227`  
  - `prompt_library_generated.md:90`
- `prompt_library_generated.md:229`  
  - `prompt_library_generated.md:92`
- `prompt_library_generated.md:231`  
  - `prompt_library_generated.md:94`
- `prompt_library_generated.md:233`  
  - `prompt_library_generated.md:96`
- `prompt_library_generated.md:235`  
  - `prompt_library_generated.md:98`
- `prompt_library_generated.md:237`  
  - `prompt_library_generated.md:100`
- `prompt_library_generated.md:239`  
  - `prompt_library_generated.md:102`
- `prompt_library_generated.md:241`  
  - `prompt_library_generated.md:104`
- `prompt_library_generated.md:243`  
  - `prompt_library_generated.md:106`
- `prompt_library_generated.md:245`  
  - `prompt_library_generated.md:108`
- `prompt_library_generated.md:247`  
  - `prompt_library_generated.md:110`
- `prompt_library_generated.md:249`  
  - `prompt_library_generated.md:112`
- `prompt_library_generated.md:251`  
  - `prompt_library_generated.md:114`
- `prompt_library_generated.md:253`  
  - `prompt_library_generated.md:116`
- `prompt_library_generated.md:255`  
  - `prompt_library_generated.md:118`
- `prompt_library_generated.md:257`  
  - `prompt_library_generated.md:120`
- `prompt_library_generated.md:259`  
  - `prompt_library_generated.md:122`
- `prompt_library_generated.md:261`  
  - `prompt_library_generated.md:124`
- `prompt_library_generated.md:263`  
  - `prompt_library_generated.md:126`
- `prompt_library_generated.md:265`  
  - `prompt_library_generated.md:128`
- `prompt_library_generated.md:267`  
  - `prompt_library_generated.md:130`
- `prompt_library_generated.md:269`  
  - `prompt_library_generated.md:132`
- `prompt_library_generated.md:271`  
  - `prompt_library_generated.md:134`
- `prompt_library_generated.md:273`  
  - `prompt_library_generated.md:136`
- `prompt_library_generated.md:275`  
  - `prompt_library_generated.md:138`
- `prompt_library_generated.md:277`  
  - `prompt_library_generated.md:140`
- `prompt_library_generated.md:279`  
  - `prompt_library_generated.md:142`
- `prompt_library_generated.md:281`  
  - `prompt_library_generated.md:144`
- `prompt_library_generated.md:283`  
  - `prompt_library_generated.md:146`
- `prompt_library_generated.md:285`  
  - `prompt_library_generated.md:148`
- `prompt_library_generated.md:287`  
  - `prompt_library_generated.md:150`
- `prompt_library_generated.md:289`  
  - `prompt_library_generated.md:152`
- `prompt_library_generated.md:291`  
  - `prompt_library_generated.md:154`
- `prompt_library_generated.md:293`  
  - `prompt_library_generated.md:156`
- `prompt_library_generated.md:295`  
  - `prompt_library_generated.md:158`
- `prompt_library_generated.md:297`  
  - `prompt_library_generated.md:160`
- `prompt_library_generated.md:299`  
  - `prompt_library_generated.md:162`
- `prompt_library_generated.md:301`  
  - `prompt_library_generated.md:164`
- `prompt_library_generated.md:303`  
  - `prompt_library_generated.md:166`
- `prompt_library_generated.md:305`  
  - `prompt_library_generated.md:168`
- `prompt_library_generated.md:307`  
  - `prompt_library_generated.md:170`
- `prompt_library_generated.md:309`  
  - `prompt_library_generated.md:172`
- `prompt_library_generated.md:311`  
  - `prompt_library_generated.md:174`
- `prompt_library_generated.md:313`  
  - `prompt_library_generated.md:176`
- `prompt_library_generated.md:315`  
  - `prompt_library_generated.md:178`
- `prompt_library_generated.md:317`  
  - `prompt_library_generated.md:180`
- `prompt_library_generated.md:319`  
  - `prompt_library_generated.md:182`
- `prompt_library_generated.md:321`  
  - `prompt_library_generated.md:184`
- `prompt_library_generated.md:323`  
  - `prompt_library_generated.md:186`
- `prompt_library_generated.md:325`  
  - `prompt_library_generated.md:188`
- `prompt_library_generated.md:327`  
  - `prompt_library_generated.md:190`
- `prompt_library_generated.md:423`  
  - `prompt_library_generated.md:194`
- `prompt_library_generated.md:425`  
  - `prompt_library_generated.md:196`
- `prompt_library_generated.md:427`  
  - `prompt_library_generated.md:198`
- `prompt_library_generated.md:429`  
  - `prompt_library_generated.md:200`
- `prompt_library_generated.md:431`  
  - `prompt_library_generated.md:202`
- `prompt_library_generated.md:433`  
  - `prompt_library_generated.md:204`
- `prompt_library_generated.md:435`  
  - `prompt_library_generated.md:206`
- `prompt_library_generated.md:437`  
  - `prompt_library_generated.md:208`
- `prompt_library_generated.md:439`  
  - `prompt_library_generated.md:210`
- `prompt_library_generated.md:441`  
  - `prompt_library_generated.md:212`
- `prompt_library_generated.md:443`  
  - `prompt_library_generated.md:214`
- `prompt_library_generated.md:445`  
  - `prompt_library_generated.md:216`
- `prompt_library_generated.md:447`  
  - `prompt_library_generated.md:218`
- `prompt_library_generated.md:449`  
  - `prompt_library_generated.md:220`
- `prompt_library_generated.md:451`  
  - `prompt_library_generated.md:222`
- `prompt_library_generated.md:453`  
  - `prompt_library_generated.md:224`
- `prompt_library_generated.md:455`  
  - `prompt_library_generated.md:226`
- `prompt_library_generated.md:457`  
  - `prompt_library_generated.md:228`
- `prompt_library_generated.md:459`  
  - `prompt_library_generated.md:230`
- `prompt_library_generated.md:461`  
  - `prompt_library_generated.md:232`
- `prompt_library_generated.md:463`  
  - `prompt_library_generated.md:234`
- `prompt_library_generated.md:465`  
  - `prompt_library_generated.md:236`
- `prompt_library_generated.md:467`  
  - `prompt_library_generated.md:238`
- `prompt_library_generated.md:469`  
  - `prompt_library_generated.md:240`
- `prompt_library_generated.md:471`  
  - `prompt_library_generated.md:242`
- `prompt_library_generated.md:473`  
  - `prompt_library_generated.md:244`
- `prompt_library_generated.md:475`  
  - `prompt_library_generated.md:246`
- `prompt_library_generated.md:477`  
  - `prompt_library_generated.md:248`
- `prompt_library_generated.md:479`  
  - `prompt_library_generated.md:250`
- `prompt_library_generated.md:481`  
  - `prompt_library_generated.md:252`
- `prompt_library_generated.md:483`  
  - `prompt_library_generated.md:254`
- `prompt_library_generated.md:485`  
  - `prompt_library_generated.md:256`
- `prompt_library_generated.md:487`  
  - `prompt_library_generated.md:258`
- `prompt_library_generated.md:523`  
  - `prompt_library_generated.md:262`
- `prompt_library_generated.md:531`  
  - `prompt_library_generated.md:849`
- `prompt_library_generated.md:547`  
  - `prompt_library_generated.md:269`
- `prompt_library_generated.md:549`  
  - `prompt_library_generated.md:271`
- `prompt_library_generated.md:551`  
  - `prompt_library_generated.md:273`
- `prompt_library_generated.md:553`  
  - `prompt_library_generated.md:275`
- `prompt_library_generated.md:560`  
  def generate_image(self, prompt, **kwargs):
- `prompt_library_generated.md:562`  
  生成图片（仅OpenAI支持）
- `prompt_library_generated.md:564`  
  prompt: 图片提示词
- `prompt_library_generated.md:566`  
  prompt=prompt,
- `prompt_library_generated.md:568`  
  logger.error(f"图片生成失败: {str(e)}")
- `prompt_library_generated.md:570`  
  # 图片生成引擎
- `prompt_library_generated.md:572`  
  2. 生成预览 - 生成内容后确认
- `prompt_library_generated.md:574`  
  # 生成内容
- `prompt_library_generated.md:576`  
  print(f"\n图片生成引擎: {Config.IMAGE_ENGINE}")
- `prompt_library_generated.md:578`  
  # 固定 Skill 根目录（用户目录下的 .codebuddy）
- `prompt_library_generated.md:580`  
  "prompt-collector": (
- `prompt_library_generated.md:582`  
  CODEBUDDY_ROOT / "prompt-collector" / "scripts" / "prompt_collector.py",
- `prompt_library_generated.md:584`  
  # 列出生成的文档
- `prompt_library_generated.md:586`  
  print("\n=== 生成文档清单（应在项目根目录）===")
- `prompt_library_generated.md:588`  
  "prompt_library_generated.md",
- `prompt_library_generated.md:590`  
  ("generated_images", "图片生成目录"),
- `prompt_library_generated.md:592`  
  print("\n2. 开始生成文章...")
- `prompt_library_generated.md:594`  
  print("\n4. 生成完成!")
- `prompt_library_generated.md:596`  
  from agents.designer import ImageDesigner
- `prompt_library_generated.md:598`  
  'designer': ImageDesigner(),
- `prompt_library_generated.md:600`  
  print("Step 4: 生成策略...")
- `prompt_library_generated.md:602`  
  print("\nStep 5: 生成文章...")
- `prompt_library_generated.md:604`  
  print("\n生成成功!")
- `prompt_library_generated.md:606`  
  print(f"生成失败: {e}")
- `prompt_library_generated.md:608`  
  from agents.designer import ImageDesigner
- `prompt_library_generated.md:610`  
  """微信公众号内容生成与发布系统"""
- `prompt_library_generated.md:612`  
  'designer': ImageDesigner(),
- `prompt_library_generated.md:614`  
  theme: 用户输入的主题
- `prompt_library_generated.md:616`  
  dict: 生成的内容包
- `prompt_library_generated.md:618`  
  'image_prompts': None,
- `prompt_library_generated.md:620`  
  # 2. 文章生成阶段
- `prompt_library_generated.md:622`  
  print("【写作】生成公众号文章...")
- `prompt_library_generated.md:624`  
  # 3. 图片生成阶段（可选）
- `prompt_library_generated.md:626`  
  print("【配图】生成配图（可选）...")
- `prompt_library_generated.md:628`  
  print("提示：已跳过图片生成\n")
- `prompt_library_generated.md:630`  
  # Web 模式下跳过图片生成
- `prompt_library_generated.md:632`  
  content_package['image_prompts'] = []
- `prompt_library_generated.md:634`  
  """完整工作流：生成并发布"""
- `prompt_library_generated.md:636`  
  # 生成内容
- `prompt_library_generated.md:638`  
  2. 生成预览 - 生成文章后确认
- `prompt_library_generated.md:640`  
  # 生成内容
- `prompt_library_generated.md:642`  
  print(f"\n图片生成引擎: {Config.IMAGE_ENGINE}")
- `prompt_library_generated.md:644`  
  from agents.designer import ImageDesigner
- `prompt_library_generated.md:646`  
  """小红书内容生成与发布系统"""
- `prompt_library_generated.md:648`  
  'designer': ImageDesigner(),
- `prompt_library_generated.md:650`  
  theme: 用户输入的主题
- `prompt_library_generated.md:652`  
  dict: 生成的内容包
- `prompt_library_generated.md:654`  
  'image_prompts': list,
- `prompt_library_generated.md:656`  
  'image_prompts': None,
- `prompt_library_generated.md:658`  
  # 3. 图片生成阶段
- `prompt_library_generated.md:660`  
  image_prompts = self.agents['designer'].generate_image_prompts(
- `prompt_library_generated.md:662`  
  content_package['image_prompts'] = image_prompts
- `prompt_library_generated.md:664`  
  print(f"✓ 生成{len(image_prompts)}个图片提示词:")
- `prompt_library_generated.md:666`  
  for idx, prompt in enumerate(image_prompts):
- `prompt_library_generated.md:668`  
  print(f"  {idx+1}. {prompt[:50]}...")
- `prompt_library_generated.md:670`  
  print(f"\n正在生成图片...")
- `prompt_library_generated.md:672`  
  image_paths = self.agents['designer'].generate_images(image_prompts)
- `prompt_library_generated.md:674`  
  print(f"✓ 成功生成{len(image_paths)}张图片\n")
- `prompt_library_generated.md:676`  
  print("内容生成完成！")
- `prompt_library_generated.md:678`  
  logger.error(f"内容生成失败: {str(e)}")
- `prompt_library_generated.md:680`  
  print(f"✗ 内容生成失败: {str(e)}\n")
- `prompt_library_generated.md:682`  
  "3. 重新生成图片\n"
- `prompt_library_generated.md:684`  
  print("  未生成图片")
- `prompt_library_generated.md:686`  
  print("2. 让AI重新生成")
- `prompt_library_generated.md:688`  
  """重新生成图片"""
- `prompt_library_generated.md:690`  
  print("\n重新生成图片选项:")
- `prompt_library_generated.md:692`  
  # 重新生成所有图片
- `prompt_library_generated.md:694`  
  prompts = content_package.get('image_prompts', [])
- `prompt_library_generated.md:696`  
  if prompts:
- `prompt_library_generated.md:698`  
  for idx, prompt in enumerate(prompts):
- `prompt_library_generated.md:700`  
  print(f"{idx+1}. {prompt}")
- `prompt_library_generated.md:702`  
  new_prompt = input("输入新提示词（留空保持）: ")
- `prompt_library_generated.md:704`  
  if new_prompt:
- `prompt_library_generated.md:706`  
  prompts = [new_prompt]
- `prompt_library_generated.md:708`  
  new_paths = self.agents['designer'].generate_images(prompts)
- `prompt_library_generated.md:710`  
  print("✓ 图片已重新生成")
- `prompt_library_generated.md:712`  
  idx = int(input("\n选择要重新生成的图片编号: ")) - 1
- `prompt_library_generated.md:714`  
  new_prompt = input("输入新提示词: ")
- `prompt_library_generated.md:716`  
  if new_prompt:
- `prompt_library_generated.md:718`  
  new_path = self.agents['designer'].regenerate_image(
- `prompt_library_generated.md:720`  
  new_prompt
- `prompt_library_generated.md:722`  
  print("✓ 图片已重新生成")
- `prompt_library_generated.md:724`  
  完整工作流：生成 → 确认 → 发布
- `prompt_library_generated.md:726`  
  # 生成内容
- `prompt_library_generated.md:728`  
  return {'success': False, 'message': '用户取消'}
- `prompt_library_generated.md:729`  
  - `agents\designer.py:8`
- `prompt_library_generated.md:730`  
  class ImageDesigner:
- `prompt_library_generated.md:731`  
  - `agents\designer.py:19`
- `prompt_library_generated.md:732`  
  def generate_image_prompts(self, theme: str, copywriting: str, strategy: dict) -> list:
- `prompt_library_generated.md:733`  
  - `agents\designer.py:21`
- `prompt_library_generated.md:734`  
  生成图片提示词
- `prompt_library_generated.md:735`  
  - `agents\designer.py:31`
- `prompt_library_generated.md:736`  
  logger.info("生成图片提示词")
- `prompt_library_generated.md:737`  
  - `agents\designer.py:33`
- `prompt_library_generated.md:738`  
  prompt = f"""
- `prompt_library_generated.md:739`  
  - `agents\designer.py:43`
- `prompt_library_generated.md:740`  
  请为小红书风格配图生成提示词，要求：
- `prompt_library_generated.md:741`  
  - `agents\designer.py:52`
- `prompt_library_generated.md:742`  
  "prompts": [
- `prompt_library_generated.md:743`  
  - `agents\designer.py:53`
- `prompt_library_generated.md:744`  
  "prompt1",
- `prompt_library_generated.md:745`  
  - `agents\designer.py:54`
- `prompt_library_generated.md:746`  
  "prompt2"
- `prompt_library_generated.md:747`  
  - `agents\designer.py:65`
- `prompt_library_generated.md:748`  
  {"role": "user", "content": prompt}
- `prompt_library_generated.md:749`  
  - `agents\designer.py:76`
- `prompt_library_generated.md:750`  
  prompts = result.get('prompts', [])
- `prompt_library_generated.md:751`  
  - `agents\designer.py:77`
- `prompt_library_generated.md:752`  
  logger.info(f"生成了{len(prompts)}个图片提示词")
- `prompt_library_generated.md:753`  
  - `agents\designer.py:78`
- `prompt_library_generated.md:754`  
  return prompts
- `prompt_library_generated.md:755`  
  - `agents\designer.py:81`
- `prompt_library_generated.md:756`  
  logger.error(f"提示词生成失败: {str(e)}")
- `prompt_library_generated.md:757`  
  - `agents\designer.py:82`
- `prompt_library_generated.md:758`  
  return self._get_default_prompts(theme)
- `prompt_library_generated.md:759`  
  - `agents\designer.py:84`
- `prompt_library_generated.md:760`  
  def _get_default_prompts(self, theme: str) -> list:
- `prompt_library_generated.md:761`  
  - `agents\designer.py:91`
- `prompt_library_generated.md:762`  
  def generate_images(self, prompts: list) -> list:
- `prompt_library_generated.md:763`  
  - `agents\designer.py:93`
- `prompt_library_generated.md:764`  
  根据提示词生成图片
- `prompt_library_generated.md:765`  
  - `agents\designer.py:96`
- `prompt_library_generated.md:766`  
  prompts: 图片提示词列表
- `prompt_library_generated.md:767`  
  - `agents\designer.py:99`
- `prompt_library_generated.md:768`  
  list: 生成的图片路径列表
- `prompt_library_generated.md:769`  
  - `agents\designer.py:101`
- `prompt_library_generated.md:770`  
  logger.info(f"开始生成{len(prompts)}张图片")
- `prompt_library_generated.md:771`  
  - `agents\designer.py:105`
- `prompt_library_generated.md:772`  
  for idx, prompt in enumerate(prompts):
- `prompt_library_generated.md:773`  
  - `agents\designer.py:107`
- `prompt_library_generated.md:774`  
  image_path = self._generate_single_image(prompt, idx)
- `prompt_library_generated.md:775`  
  - `agents\designer.py:112`
- `prompt_library_generated.md:776`  
  logger.error(f"生成第{idx+1}张图片失败: {str(e)}")
- `prompt_library_generated.md:777`  
  - `agents\designer.py:114`
- `prompt_library_generated.md:778`  
  logger.info(f"成功生成{len(image_paths)}张图片")
- `prompt_library_generated.md:779`  
  - `agents\designer.py:117`
- `prompt_library_generated.md:780`  
  def _generate_single_image(self, prompt: str, index: int) -> str:
- `prompt_library_generated.md:781`  
  - `agents\designer.py:119`
- `prompt_library_generated.md:782`  
  生成单张图片
- `prompt_library_generated.md:783`  
  - `agents\designer.py:122`
- `prompt_library_generated.md:784`  
  prompt: 提示词
- `prompt_library_generated.md:785`  
  - `agents\designer.py:129`
- `prompt_library_generated.md:786`  
  return self._generate_with_dalle(prompt, index)
- `prompt_library_generated.md:787`  
  - `agents\designer.py:131`
- `prompt_library_generated.md:788`  
  return self._generate_with_stable_diffusion(prompt, index)
- `prompt_library_generated.md:789`  
  - `agents\designer.py:133`
- `prompt_library_generated.md:790`  
  def _generate_with_dalle(self, prompt: str, index: int) -> str:
- `prompt_library_generated.md:791`  
  - `agents\designer.py:134`
- `prompt_library_generated.md:792`  
  """使用DALL-E 3生成图片"""
- `prompt_library_generated.md:793`  
  - `agents\designer.py:137`
- `prompt_library_generated.md:794`  
  prompt=prompt,
- `prompt_library_generated.md:795`  
  - `agents\designer.py:151`
- `prompt_library_generated.md:796`  
  logger.info(f"DALL-E生成图片成功: {image_path}")
- `prompt_library_generated.md:797`  
  - `agents\designer.py:155`
- `prompt_library_generated.md:798`  
  logger.error(f"DALL-E生成失败: {str(e)}")
- `prompt_library_generated.md:799`  
  - `agents\designer.py:158`
- `prompt_library_generated.md:800`  
  def _generate_with_stable_diffusion(self, prompt: str, index: int) -> str:
- `prompt_library_generated.md:801`  
  - `agents\designer.py:159`
- `prompt_library_generated.md:802`  
  """使用Stable Diffusion生成图片"""
- `prompt_library_generated.md:803`  
  - `agents\designer.py:163`
- `prompt_library_generated.md:804`  
  "prompt": prompt,
- `prompt_library_generated.md:805`  
  - `agents\designer.py:164`
- `prompt_library_generated.md:806`  
  "negative_prompt": "low quality, blurry, ugly, distorted",
- `prompt_library_generated.md:807`  
  - `agents\designer.py:184`
- `prompt_library_generated.md:808`  
  logger.info(f"Stable Diffusion生成图片成功: {image_path}")
- `prompt_library_generated.md:809`  
  - `agents\designer.py:188`
- `prompt_library_generated.md:810`  
  logger.error(f"Stable Diffusion生成失败: {str(e)}")
- `prompt_library_generated.md:811`  
  - `agents\designer.py:191`
- `prompt_library_generated.md:812`  
  def regenerate_image(self, old_path: str, new_prompt: str) -> str:
- `prompt_library_generated.md:813`  
  - `agents\designer.py:193`
- `prompt_library_generated.md:814`  
  重新生成指定图片
- `prompt_library_generated.md:815`  
  - `agents\designer.py:197`
- `prompt_library_generated.md:816`  
  new_prompt: 新的提示词
- `prompt_library_generated.md:817`  
  - `agents\designer.py:202`
- `prompt_library_generated.md:818`  
  logger.info(f"重新生成图片: {old_path}")
- `prompt_library_generated.md:819`  
  - `agents\designer.py:207`
- `prompt_library_generated.md:820`  
  return self._generate_single_image(new_prompt, index)
- `prompt_library_generated.md:822`  
  分析主题，生成内容策略
- `prompt_library_generated.md:824`  
  theme: 用户输入的主题
- `prompt_library_generated.md:826`  
  prompt = f"""
- `prompt_library_generated.md:828`  
  {"role": "user", "content": prompt}
- `prompt_library_generated.md:830`  
  logger.info(f"内容策略生成成功: {strategy}")
- `prompt_library_generated.md:832`  
  logger.error(f"内容策略生成失败: {str(e)}")
- `prompt_library_generated.md:834`  
  user_feedback: 用户反馈意见
- `prompt_library_generated.md:836`  
  prompt = f"""
- `prompt_library_generated.md:838`  
  用户反馈：{user_feedback}
- `prompt_library_generated.md:840`  
  {"role": "user", "content": prompt}
- `prompt_library_generated.md:842`  
  prompt = f"""
- `prompt_library_generated.md:844`  
  {"role": "user", "content": prompt}
- `prompt_library_generated.md:846`  
  """生成摘要"""
- `prompt_library_generated.md:848`  
  生成微信公众号文章
- `prompt_library_generated.md:850`  
  logger.info(f"开始生成公众号文章，主题: {theme}")
- `prompt_library_generated.md:852`  
  # 生成摘要
- `prompt_library_generated.md:854`  
  prompt = f"""
- `prompt_library_generated.md:856`  
  messages=[{'role': 'user', 'content': prompt}],
- `prompt_library_generated.md:858`  
  prompt = f"""
- `prompt_library_generated.md:860`  
  messages=[{'role': 'user', 'content': prompt}],
- `prompt_library_generated.md:862`  
  """生成文章摘要"""
- `prompt_library_generated.md:864`  
  prompt = f"""
- `prompt_library_generated.md:866`  
  {"role": "user", "content": prompt}
- `prompt_library_generated.md:868`  
  feedback: 用户反馈
- `prompt_library_generated.md:870`  
  prompt = f"""
- `prompt_library_generated.md:872`  
  用户反馈：{feedback}
- `prompt_library_generated.md:874`  
  {"role": "user", "content": prompt}
- `prompt_library_generated.md:876`  
  prompt = f"""
- `prompt_library_generated.md:878`  
  {"role": "user", "content": prompt}
- `prompt_library_generated.md:880`  
  """生成预览 - 异步处理"""
- `prompt_library_generated.md:882`  
  print(f"\n收到生成预览请求: {theme}")
- `prompt_library_generated.md:884`  
  print(f"生成预览失败: {e}")
- `prompt_library_generated.md:886`  
  'message': f'生成失败: {str(e)}'
- `prompt_library_generated.md:888`  
  """异步生成预览"""
- `prompt_library_generated.md:890`  
  5. [图片生成方案](#5-图片生成方案)
- `prompt_library_generated.md:892`  
  ✅ **免费额度高**：新用户赠送500万Tokens（约相当于2000元OpenAI额度）
- `prompt_library_generated.md:894`  
  6. 复制生成的API Key（格式：sk-xxxxxxxx）
- `prompt_library_generated.md:896`  
  - 新用户免费额度：500万Tokens
- `prompt_library_generated.md:898`  
  ✅ 新用户赠送免费额度
- `prompt_library_generated.md:900`  
  2. 复制生成的Key
- `prompt_library_generated.md:902`  
  - 新用户免费试用
- `prompt_library_generated.md:904`  
  ✅ 新用户免费额度
- `prompt_library_generated.md:906`  
  - 新用户免费额度
- `prompt_library_generated.md:908`  
  ✅ 新用户免费额度
- `prompt_library_generated.md:910`  
  - 新用户免费额度
- `prompt_library_generated.md:912`  
  ## 5. 图片生成方案
- `prompt_library_generated.md:914`  
  # 复制配置模板
- `prompt_library_generated.md:916`  
  | 服务商 | 新用户免费 | 价格 | 速度 | 中文支持 | 推荐度 |
- `prompt_library_generated.md:918`  
  ### Q4: 图片生成必须配置吗？
- `prompt_library_generated.md:920`  
  # 自动生成项目文档 - 20260206205332
- `prompt_library_generated.md:922`  
  > 生成时间: 2026-02-11 17:26
- `prompt_library_generated.md:924`  
  - 🟢 项目名称: 小红书内容生成与发布平台
- `prompt_library_generated.md:926`  
  - 🟢 图片生成（Stable Diffusion）
- `prompt_library_generated.md:928`  
  - 🔴 持久化用户数据与内容库（建议补充）
- `prompt_library_generated.md:930`  
  > 生成时间: 2026-02-11 17:26
- `prompt_library_generated.md:932`  
  **需求描述**：读取运行时设置
- `prompt_library_generated.md:934`  
  **需求描述**：分析市场热点，推荐选题
- `prompt_library_generated.md:936`  
  **数据来源**：AI模型、用户输入
- `prompt_library_generated.md:938`  
  **需求描述**：规则校验与敏感词检测
- `prompt_library_generated.md:940`  
  **需求描述**：读取运行时设置
- `prompt_library_generated.md:942`  
  **需求描述**：读取运行时设置
- `prompt_library_generated.md:944`  
  **需求描述**：读取运行时设置
- `prompt_library_generated.md:946`  
  **需求描述**：读取运行时设置
- `prompt_library_generated.md:948`  
  **需求描述**：读取运行时设置
- `prompt_library_generated.md:950`  
  生成时间: 2026-02-06
- `prompt_library_generated.md:952`  
  - [x] .env.example（配置模板）
- `prompt_library_generated.md:954`  
  ├── generated_images/            # 生成的图片目录
- `prompt_library_generated.md:956`  
  ├── .env.example                 # 配置模板
- `prompt_library_generated.md:958`  
  ### Windows用户
- `prompt_library_generated.md:960`  
  ✅ 内容策略生成
- `prompt_library_generated.md:962`  
  ✅ AI图片生成
- `prompt_library_generated.md:964`  
  开始使用系统生成小红书内容！🎉
- `prompt_library_generated.md:965`  
  - `prompt_library_generated.md:1`
- `prompt_library_generated.md:966`  
  # 提示词模板库 - 自动生成
- `prompt_library_generated.md:967`  
  - `prompt_library_generated.md:2`
- `prompt_library_generated.md:968`  
  > 生成时间: 2026-02-11 17:04
- `prompt_library_generated.md:969`  
  - `prompt_library_generated.md:29`
- `prompt_library_generated.md:970`  
  - `agents\designer.py:9`
- `prompt_library_generated.md:971`  
  - `prompt_library_generated.md:31`
- `prompt_library_generated.md:972`  
  - `agents\designer.py:25`
- `prompt_library_generated.md:973`  
  - `prompt_library_generated.md:33`
- `prompt_library_generated.md:974`  
  - `agents\designer.py:34`
- `prompt_library_generated.md:975`  
  - `prompt_library_generated.md:35`
- `prompt_library_generated.md:976`  
  - `agents\designer.py:36`
- `prompt_library_generated.md:977`  
  - `prompt_library_generated.md:279`
- `prompt_library_generated.md:978`  
  def generate_image(self, prompt, **kwargs):
- `prompt_library_generated.md:979`  
  - `prompt_library_generated.md:281`
- `prompt_library_generated.md:980`  
  生成图片（仅OpenAI支持）
- `prompt_library_generated.md:981`  
  - `prompt_library_generated.md:283`
- `prompt_library_generated.md:982`  
  prompt: 图片提示词
- `prompt_library_generated.md:983`  
  - `prompt_library_generated.md:285`
- `prompt_library_generated.md:984`  
  prompt=prompt,
- `prompt_library_generated.md:985`  
  - `prompt_library_generated.md:287`
- `prompt_library_generated.md:986`  
  logger.error(f"图片生成失败: {str(e)}")
- `prompt_library_generated.md:987`  
  - `prompt_library_generated.md:289`
- `prompt_library_generated.md:988`  
  # 图片生成引擎
- `prompt_library_generated.md:989`  
  - `prompt_library_generated.md:291`
- `prompt_library_generated.md:990`  
  2. 生成预览 - 生成内容后确认
- `prompt_library_generated.md:991`  
  - `prompt_library_generated.md:293`
- `prompt_library_generated.md:992`  
  # 生成内容
- `prompt_library_generated.md:993`  
  - `prompt_library_generated.md:295`
- `prompt_library_generated.md:994`  
  print(f"\n图片生成引擎: {Config.IMAGE_ENGINE}")
- `prompt_library_generated.md:995`  
  - `prompt_library_generated.md:297`
- `prompt_library_generated.md:996`  
  ("generated_images", "图片生成目录"),
- `prompt_library_generated.md:997`  
  - `prompt_library_generated.md:299`
- `prompt_library_generated.md:998`  
  print("\n2. 开始生成文章...")
- `prompt_library_generated.md:999`  
  - `prompt_library_generated.md:301`
- `prompt_library_generated.md:1000`  
  print("\n4. 生成完成!")
- `prompt_library_generated.md:1001`  
  - `prompt_library_generated.md:303`
- `prompt_library_generated.md:1002`  
  from agents.designer import ImageDesigner
- `prompt_library_generated.md:1003`  
  - `prompt_library_generated.md:305`
- `prompt_library_generated.md:1004`  
  'designer': ImageDesigner(),
- `prompt_library_generated.md:1005`  
  - `prompt_library_generated.md:307`
- `prompt_library_generated.md:1006`  
  print("Step 4: 生成策略...")
- `prompt_library_generated.md:1007`  
  - `prompt_library_generated.md:309`
- `prompt_library_generated.md:1008`  
  print("\nStep 5: 生成文章...")
- `prompt_library_generated.md:1009`  
  - `prompt_library_generated.md:311`
- `prompt_library_generated.md:1010`  
  print("\n生成成功!")
- `prompt_library_generated.md:1011`  
  - `prompt_library_generated.md:313`
- `prompt_library_generated.md:1012`  
  print(f"生成失败: {e}")
- `prompt_library_generated.md:1013`  
  - `prompt_library_generated.md:315`
- `prompt_library_generated.md:1014`  
  from agents.designer import ImageDesigner
- `prompt_library_generated.md:1015`  
  - `prompt_library_generated.md:317`
- `prompt_library_generated.md:1016`  
  """微信公众号内容生成与发布系统"""
- `prompt_library_generated.md:1017`  
  - `prompt_library_generated.md:319`
- `prompt_library_generated.md:1018`  
  'designer': ImageDesigner(),
- `prompt_library_generated.md:1019`  
  - `prompt_library_generated.md:321`
- `prompt_library_generated.md:1020`  
  theme: 用户输入的主题
- `prompt_library_generated.md:1021`  
  - `prompt_library_generated.md:323`
- `prompt_library_generated.md:1022`  
  dict: 生成的内容包
- `prompt_library_generated.md:1023`  
  - `prompt_library_generated.md:325`
- `prompt_library_generated.md:1024`  
  'image_prompts': None,
- `prompt_library_generated.md:1025`  
  - `prompt_library_generated.md:327`
- `prompt_library_generated.md:1026`  
  # 2. 文章生成阶段
- `prompt_library_generated.md:1027`  
  - `prompt_library_generated.md:329`
- `prompt_library_generated.md:1028`  
  print("【写作】生成公众号文章...")
- `prompt_library_generated.md:1029`  
  - `prompt_library_generated.md:331`
- `prompt_library_generated.md:1030`  
  # 3. 图片生成阶段（可选）
- `prompt_library_generated.md:1031`  
  - `prompt_library_generated.md:333`
- `prompt_library_generated.md:1032`  
  print("【配图】生成配图（可选）...")
- `prompt_library_generated.md:1033`  
  - `prompt_library_generated.md:335`
- `prompt_library_generated.md:1034`  
  print("提示：已跳过图片生成\n")
- `prompt_library_generated.md:1035`  
  - `prompt_library_generated.md:337`
- `prompt_library_generated.md:1036`  
  # Web 模式下跳过图片生成
- `prompt_library_generated.md:1037`  
  - `prompt_library_generated.md:339`
- `prompt_library_generated.md:1038`  
  content_package['image_prompts'] = []
- `prompt_library_generated.md:1039`  
  - `prompt_library_generated.md:341`
- `prompt_library_generated.md:1040`  
  """完整工作流：生成并发布"""
- `prompt_library_generated.md:1041`  
  - `prompt_library_generated.md:343`
- `prompt_library_generated.md:1042`  
  # 生成内容
- `prompt_library_generated.md:1043`  
  - `prompt_library_generated.md:345`
- `prompt_library_generated.md:1044`  
  2. 生成预览 - 生成文章后确认
- `prompt_library_generated.md:1045`  
  - `prompt_library_generated.md:347`
- `prompt_library_generated.md:1046`  
  # 生成内容
- `prompt_library_generated.md:1047`  
  - `prompt_library_generated.md:349`
- `prompt_library_generated.md:1048`  
  print(f"\n图片生成引擎: {Config.IMAGE_ENGINE}")
- `prompt_library_generated.md:1049`  
  - `prompt_library_generated.md:351`
- `prompt_library_generated.md:1050`  
  from agents.designer import ImageDesigner
- `prompt_library_generated.md:1051`  
  - `prompt_library_generated.md:353`
- `prompt_library_generated.md:1052`  
  """小红书内容生成与发布系统"""
- `prompt_library_generated.md:1053`  
  - `prompt_library_generated.md:355`
- `prompt_library_generated.md:1054`  
  'designer': ImageDesigner(),
- `prompt_library_generated.md:1055`  
  - `prompt_library_generated.md:357`
- `prompt_library_generated.md:1056`  
  theme: 用户输入的主题
- `prompt_library_generated.md:1057`  
  - `prompt_library_generated.md:359`
- `prompt_library_generated.md:1058`  
  dict: 生成的内容包
- `prompt_library_generated.md:1059`  
  - `prompt_library_generated.md:361`
- `prompt_library_generated.md:1060`  
  'image_prompts': list,
- `prompt_library_generated.md:1061`  
  - `prompt_library_generated.md:363`
- `prompt_library_generated.md:1062`  
  'image_prompts': None,
- `prompt_library_generated.md:1063`  
  - `prompt_library_generated.md:365`
- `prompt_library_generated.md:1064`  
  # 3. 图片生成阶段
- `prompt_library_generated.md:1065`  
  - `prompt_library_generated.md:367`
- `prompt_library_generated.md:1066`  
  image_prompts = self.agents['designer'].generate_image_prompts(
- `prompt_library_generated.md:1067`  
  - `prompt_library_generated.md:369`
- `prompt_library_generated.md:1068`  
  content_package['image_prompts'] = image_prompts
- `prompt_library_generated.md:1069`  
  - `prompt_library_generated.md:371`
- `prompt_library_generated.md:1070`  
  print(f"✓ 生成{len(image_prompts)}个图片提示词:")
- `prompt_library_generated.md:1071`  
  - `prompt_library_generated.md:373`
- `prompt_library_generated.md:1072`  
  for idx, prompt in enumerate(image_prompts):
- `prompt_library_generated.md:1073`  
  - `prompt_library_generated.md:375`
- `prompt_library_generated.md:1074`  
  print(f"  {idx+1}. {prompt[:50]}...")
- `prompt_library_generated.md:1075`  
  - `prompt_library_generated.md:377`
- `prompt_library_generated.md:1076`  
  print(f"\n正在生成图片...")
- `prompt_library_generated.md:1077`  
  - `prompt_library_generated.md:379`
- `prompt_library_generated.md:1078`  
  image_paths = self.agents['designer'].generate_images(image_prompts)
- `prompt_library_generated.md:1079`  
  - `prompt_library_generated.md:381`
- `prompt_library_generated.md:1080`  
  print(f"✓ 成功生成{len(image_paths)}张图片\n")
- `prompt_library_generated.md:1081`  
  - `prompt_library_generated.md:383`
- `prompt_library_generated.md:1082`  
  print("内容生成完成！")
- `prompt_library_generated.md:1083`  
  - `prompt_library_generated.md:385`
- `prompt_library_generated.md:1084`  
  logger.error(f"内容生成失败: {str(e)}")
- `prompt_library_generated.md:1085`  
  - `prompt_library_generated.md:387`
- `prompt_library_generated.md:1086`  
  print(f"✗ 内容生成失败: {str(e)}\n")
- `prompt_library_generated.md:1087`  
  - `prompt_library_generated.md:389`
- `prompt_library_generated.md:1088`  
  "3. 重新生成图片\n"
- `prompt_library_generated.md:1089`  
  - `prompt_library_generated.md:391`
- `prompt_library_generated.md:1090`  
  print("  未生成图片")
- `prompt_library_generated.md:1091`  
  - `prompt_library_generated.md:393`
- `prompt_library_generated.md:1092`  
  print("2. 让AI重新生成")
- `prompt_library_generated.md:1093`  
  - `prompt_library_generated.md:395`
- `prompt_library_generated.md:1094`  
  """重新生成图片"""
- `prompt_library_generated.md:1095`  
  - `prompt_library_generated.md:397`
- `prompt_library_generated.md:1096`  
  print("\n重新生成图片选项:")
- `prompt_library_generated.md:1097`  
  - `prompt_library_generated.md:399`
- `prompt_library_generated.md:1098`  
  # 重新生成所有图片
- `prompt_library_generated.md:1099`  
  - `prompt_library_generated.md:401`
- `prompt_library_generated.md:1100`  
  prompts = content_package.get('image_prompts', [])
- `prompt_library_generated.md:1101`  
  - `prompt_library_generated.md:403`
- `prompt_library_generated.md:1102`  
  if prompts:
- `prompt_library_generated.md:1103`  
  - `prompt_library_generated.md:405`
- `prompt_library_generated.md:1104`  
  for idx, prompt in enumerate(prompts):
- `prompt_library_generated.md:1105`  
  - `prompt_library_generated.md:407`
- `prompt_library_generated.md:1106`  
  print(f"{idx+1}. {prompt}")
- `prompt_library_generated.md:1107`  
  - `prompt_library_generated.md:409`
- `prompt_library_generated.md:1108`  
  new_prompt = input("输入新提示词（留空保持）: ")
- `prompt_library_generated.md:1109`  
  - `prompt_library_generated.md:411`
- `prompt_library_generated.md:1110`  
  if new_prompt:
- `prompt_library_generated.md:1111`  
  - `prompt_library_generated.md:413`
- `prompt_library_generated.md:1112`  
  prompts = [new_prompt]
- `prompt_library_generated.md:1113`  
  - `prompt_library_generated.md:415`
- `prompt_library_generated.md:1114`  
  new_paths = self.agents['designer'].generate_images(prompts)
- `prompt_library_generated.md:1115`  
  - `prompt_library_generated.md:417`
- `prompt_library_generated.md:1116`  
  print("✓ 图片已重新生成")
- `prompt_library_generated.md:1117`  
  - `prompt_library_generated.md:419`
- `prompt_library_generated.md:1118`  
  idx = int(input("\n选择要重新生成的图片编号: ")) - 1
- `prompt_library_generated.md:1119`  
  - `prompt_library_generated.md:421`
- `prompt_library_generated.md:1120`  
  new_prompt = input("输入新提示词: ")
- `prompt_library_generated.md:1121`  
  - `prompt_library_generated.md:423`
- `prompt_library_generated.md:1122`  
  if new_prompt:
- `prompt_library_generated.md:1123`  
  - `prompt_library_generated.md:425`
- `prompt_library_generated.md:1124`  
  new_path = self.agents['designer'].regenerate_image(
- `prompt_library_generated.md:1125`  
  - `prompt_library_generated.md:427`
- `prompt_library_generated.md:1126`  
  new_prompt
- `prompt_library_generated.md:1127`  
  - `prompt_library_generated.md:429`
- `prompt_library_generated.md:1128`  
  print("✓ 图片已重新生成")
- `prompt_library_generated.md:1129`  
  - `prompt_library_generated.md:431`
- `prompt_library_generated.md:1130`  
  完整工作流：生成 → 确认 → 发布
- `prompt_library_generated.md:1131`  
  - `prompt_library_generated.md:433`
- `prompt_library_generated.md:1132`  
  # 生成内容
- `prompt_library_generated.md:1133`  
  - `prompt_library_generated.md:435`
- `prompt_library_generated.md:1134`  
  return {'success': False, 'message': '用户取消'}
- `prompt_library_generated.md:1135`  
  - `prompt_library_generated.md:436`
- `prompt_library_generated.md:1136`  
  - `agents\designer.py:8`
- `prompt_library_generated.md:1137`  
  - `prompt_library_generated.md:437`
- `prompt_library_generated.md:1138`  
  class ImageDesigner:
- `prompt_library_generated.md:1139`  
  - `prompt_library_generated.md:438`
- `prompt_library_generated.md:1140`  
  - `agents\designer.py:19`
- `prompt_library_generated.md:1141`  
  - `prompt_library_generated.md:439`
- `prompt_library_generated.md:1142`  
  def generate_image_prompts(self, theme: str, copywriting: str, strategy: dict) -> list:
- `prompt_library_generated.md:1143`  
  - `prompt_library_generated.md:440`
- `prompt_library_generated.md:1144`  
  - `agents\designer.py:21`
- `prompt_library_generated.md:1145`  
  - `prompt_library_generated.md:441`
- `prompt_library_generated.md:1146`  
  生成图片提示词
- `prompt_library_generated.md:1147`  
  - `prompt_library_generated.md:442`
- `prompt_library_generated.md:1148`  
  - `agents\designer.py:31`
- `prompt_library_generated.md:1149`  
  - `prompt_library_generated.md:443`
- `prompt_library_generated.md:1150`  
  logger.info("生成图片提示词")
- `prompt_library_generated.md:1151`  
  - `prompt_library_generated.md:444`
- `prompt_library_generated.md:1152`  
  - `agents\designer.py:33`
- `prompt_library_generated.md:1153`  
  - `prompt_library_generated.md:445`
- `prompt_library_generated.md:1154`  
  prompt = f"""
- `prompt_library_generated.md:1155`  
  - `prompt_library_generated.md:446`
- `prompt_library_generated.md:1156`  
  - `agents\designer.py:43`
- `prompt_library_generated.md:1157`  
  - `prompt_library_generated.md:447`
- `prompt_library_generated.md:1158`  
  请为小红书风格配图生成提示词，要求：
- `prompt_library_generated.md:1159`  
  - `prompt_library_generated.md:448`
- `prompt_library_generated.md:1160`  
  - `agents\designer.py:52`
- `prompt_library_generated.md:1161`  
  - `prompt_library_generated.md:449`
- `prompt_library_generated.md:1162`  
  "prompts": [
- `prompt_library_generated.md:1163`  
  - `prompt_library_generated.md:450`
- `prompt_library_generated.md:1164`  
  - `agents\designer.py:53`
- `prompt_library_generated.md:1165`  
  - `prompt_library_generated.md:451`
- `prompt_library_generated.md:1166`  
  "prompt1",
- `prompt_library_generated.md:1167`  
  - `prompt_library_generated.md:452`
- `prompt_library_generated.md:1168`  
  - `agents\designer.py:54`
- `prompt_library_generated.md:1169`  
  - `prompt_library_generated.md:453`
- `prompt_library_generated.md:1170`  
  "prompt2"
- `prompt_library_generated.md:1171`  
  - `prompt_library_generated.md:454`
- `prompt_library_generated.md:1172`  
  - `agents\designer.py:65`
- `prompt_library_generated.md:1173`  
  - `prompt_library_generated.md:455`
- `prompt_library_generated.md:1174`  
  {"role": "user", "content": prompt}
- `prompt_library_generated.md:1175`  
  - `prompt_library_generated.md:456`
- `prompt_library_generated.md:1176`  
  - `agents\designer.py:76`
- `prompt_library_generated.md:1177`  
  - `prompt_library_generated.md:457`
- `prompt_library_generated.md:1178`  
  prompts = result.get('prompts', [])
- `prompt_library_generated.md:1179`  
  - `prompt_library_generated.md:458`
- `prompt_library_generated.md:1180`  
  - `agents\designer.py:77`
- `prompt_library_generated.md:1181`  
  - `prompt_library_generated.md:459`
- `prompt_library_generated.md:1182`  
  logger.info(f"生成了{len(prompts)}个图片提示词")
- `prompt_library_generated.md:1183`  
  - `prompt_library_generated.md:460`
- `prompt_library_generated.md:1184`  
  - `agents\designer.py:78`
- `prompt_library_generated.md:1185`  
  - `prompt_library_generated.md:461`
- `prompt_library_generated.md:1186`  
  return prompts
- `prompt_library_generated.md:1187`  
  - `prompt_library_generated.md:462`
- `prompt_library_generated.md:1188`  
  - `agents\designer.py:81`
- `prompt_library_generated.md:1189`  
  - `prompt_library_generated.md:463`
- `prompt_library_generated.md:1190`  
  logger.error(f"提示词生成失败: {str(e)}")
- `prompt_library_generated.md:1191`  
  - `prompt_library_generated.md:464`
- `prompt_library_generated.md:1192`  
  - `agents\designer.py:82`
- `prompt_library_generated.md:1193`  
  - `prompt_library_generated.md:465`
- `prompt_library_generated.md:1194`  
  return self._get_default_prompts(theme)
- `prompt_library_generated.md:1195`  
  - `prompt_library_generated.md:466`
- `prompt_library_generated.md:1196`  
  - `agents\designer.py:84`
- `prompt_library_generated.md:1197`  
  - `prompt_library_generated.md:467`
- `prompt_library_generated.md:1198`  
  def _get_default_prompts(self, theme: str) -> list:
- `prompt_library_generated.md:1199`  
  - `prompt_library_generated.md:468`
- `prompt_library_generated.md:1200`  
  - `agents\designer.py:91`
- `prompt_library_generated.md:1201`  
  - `prompt_library_generated.md:469`
- `prompt_library_generated.md:1202`  
  def generate_images(self, prompts: list) -> list:
- `prompt_library_generated.md:1203`  
  - `prompt_library_generated.md:470`
- `prompt_library_generated.md:1204`  
  - `agents\designer.py:93`
- `prompt_library_generated.md:1205`  
  - `prompt_library_generated.md:471`
- `prompt_library_generated.md:1206`  
  根据提示词生成图片
- `prompt_library_generated.md:1207`  
  - `prompt_library_generated.md:472`
- `prompt_library_generated.md:1208`  
  - `agents\designer.py:96`
- `prompt_library_generated.md:1209`  
  - `prompt_library_generated.md:473`
- `prompt_library_generated.md:1210`  
  prompts: 图片提示词列表
- `prompt_library_generated.md:1211`  
  - `prompt_library_generated.md:474`
- `prompt_library_generated.md:1212`  
  - `agents\designer.py:99`
- `prompt_library_generated.md:1213`  
  - `prompt_library_generated.md:475`
- `prompt_library_generated.md:1214`  
  list: 生成的图片路径列表
- `prompt_library_generated.md:1215`  
  - `prompt_library_generated.md:476`
- `prompt_library_generated.md:1216`  
  - `agents\designer.py:101`
- `prompt_library_generated.md:1217`  
  - `prompt_library_generated.md:477`
- `prompt_library_generated.md:1218`  
  logger.info(f"开始生成{len(prompts)}张图片")
- `prompt_library_generated.md:1219`  
  - `prompt_library_generated.md:478`
- `prompt_library_generated.md:1220`  
  - `agents\designer.py:105`
- `prompt_library_generated.md:1221`  
  - `prompt_library_generated.md:479`
- `prompt_library_generated.md:1222`  
  for idx, prompt in enumerate(prompts):
- `prompt_library_generated.md:1223`  
  - `prompt_library_generated.md:480`
- `prompt_library_generated.md:1224`  
  - `agents\designer.py:107`
- `prompt_library_generated.md:1225`  
  - `prompt_library_generated.md:481`
- `prompt_library_generated.md:1226`  
  image_path = self._generate_single_image(prompt, idx)
- `prompt_library_generated.md:1227`  
  - `prompt_library_generated.md:482`
- `prompt_library_generated.md:1228`  
  - `agents\designer.py:112`
- `prompt_library_generated.md:1229`  
  - `prompt_library_generated.md:483`
- `prompt_library_generated.md:1230`  
  logger.error(f"生成第{idx+1}张图片失败: {str(e)}")
- `prompt_library_generated.md:1231`  
  - `prompt_library_generated.md:484`
- `prompt_library_generated.md:1232`  
  - `agents\designer.py:114`
- `prompt_library_generated.md:1233`  
  - `prompt_library_generated.md:485`
- `prompt_library_generated.md:1234`  
  logger.info(f"成功生成{len(image_paths)}张图片")
- `prompt_library_generated.md:1235`  
  - `prompt_library_generated.md:486`
- `prompt_library_generated.md:1236`  
  - `agents\designer.py:117`
- `prompt_library_generated.md:1237`  
  - `prompt_library_generated.md:487`
- `prompt_library_generated.md:1238`  
  def _generate_single_image(self, prompt: str, index: int) -> str:
- `prompt_library_generated.md:1239`  
  - `prompt_library_generated.md:488`
- `prompt_library_generated.md:1240`  
  - `agents\designer.py:119`
- `prompt_library_generated.md:1241`  
  - `prompt_library_generated.md:489`
- `prompt_library_generated.md:1242`  
  生成单张图片
- `prompt_library_generated.md:1243`  
  - `prompt_library_generated.md:490`
- `prompt_library_generated.md:1244`  
  - `agents\designer.py:122`
- `prompt_library_generated.md:1245`  
  - `prompt_library_generated.md:491`
- `prompt_library_generated.md:1246`  
  prompt: 提示词
- `prompt_library_generated.md:1247`  
  - `prompt_library_generated.md:492`
- `prompt_library_generated.md:1248`  
  - `agents\designer.py:129`
- `prompt_library_generated.md:1249`  
  - `prompt_library_generated.md:493`
- `prompt_library_generated.md:1250`  
  return self._generate_with_dalle(prompt, index)
- `prompt_library_generated.md:1251`  
  - `prompt_library_generated.md:494`
- `prompt_library_generated.md:1252`  
  - `agents\designer.py:131`
- `prompt_library_generated.md:1253`  
  - `prompt_library_generated.md:495`
- `prompt_library_generated.md:1254`  
  return self._generate_with_stable_diffusion(prompt, index)
- `prompt_library_generated.md:1255`  
  - `prompt_library_generated.md:496`
- `prompt_library_generated.md:1256`  
  - `agents\designer.py:133`
- `prompt_library_generated.md:1257`  
  - `prompt_library_generated.md:497`
- `prompt_library_generated.md:1258`  
  def _generate_with_dalle(self, prompt: str, index: int) -> str:
- `prompt_library_generated.md:1259`  
  - `prompt_library_generated.md:498`
- `prompt_library_generated.md:1260`  
  - `agents\designer.py:134`
- `prompt_library_generated.md:1261`  
  - `prompt_library_generated.md:499`
- `prompt_library_generated.md:1262`  
  """使用DALL-E 3生成图片"""
- `prompt_library_generated.md:1263`  
  - `prompt_library_generated.md:500`
- `prompt_library_generated.md:1264`  
  - `agents\designer.py:137`
- `prompt_library_generated.md:1265`  
  - `prompt_library_generated.md:501`
- `prompt_library_generated.md:1266`  
  prompt=prompt,
- `prompt_library_generated.md:1267`  
  - `prompt_library_generated.md:502`
- `prompt_library_generated.md:1268`  
  - `agents\designer.py:151`
- `prompt_library_generated.md:1269`  
  - `prompt_library_generated.md:503`
- `prompt_library_generated.md:1270`  
  logger.info(f"DALL-E生成图片成功: {image_path}")
- `prompt_library_generated.md:1271`  
  - `prompt_library_generated.md:504`
- `prompt_library_generated.md:1272`  
  - `agents\designer.py:155`
- `prompt_library_generated.md:1273`  
  - `prompt_library_generated.md:505`
- `prompt_library_generated.md:1274`  
  logger.error(f"DALL-E生成失败: {str(e)}")
- `prompt_library_generated.md:1275`  
  - `prompt_library_generated.md:506`
- `prompt_library_generated.md:1276`  
  - `agents\designer.py:158`
- `prompt_library_generated.md:1277`  
  - `prompt_library_generated.md:507`
- `prompt_library_generated.md:1278`  
  def _generate_with_stable_diffusion(self, prompt: str, index: int) -> str:
- `prompt_library_generated.md:1279`  
  - `prompt_library_generated.md:508`
- `prompt_library_generated.md:1280`  
  - `agents\designer.py:159`
- `prompt_library_generated.md:1281`  
  - `prompt_library_generated.md:509`
- `prompt_library_generated.md:1282`  
  """使用Stable Diffusion生成图片"""
- `prompt_library_generated.md:1283`  
  - `prompt_library_generated.md:510`
- `prompt_library_generated.md:1284`  
  - `agents\designer.py:163`
- `prompt_library_generated.md:1285`  
  - `prompt_library_generated.md:511`
- `prompt_library_generated.md:1286`  
  "prompt": prompt,
- `prompt_library_generated.md:1287`  
  - `prompt_library_generated.md:512`
- `prompt_library_generated.md:1288`  
  - `agents\designer.py:164`
- `prompt_library_generated.md:1289`  
  - `prompt_library_generated.md:513`
- `prompt_library_generated.md:1290`  
  "negative_prompt": "low quality, blurry, ugly, distorted",
- `prompt_library_generated.md:1291`  
  - `prompt_library_generated.md:514`
- `prompt_library_generated.md:1292`  
  - `agents\designer.py:184`
- `prompt_library_generated.md:1293`  
  - `prompt_library_generated.md:515`
- `prompt_library_generated.md:1294`  
  logger.info(f"Stable Diffusion生成图片成功: {image_path}")
- `prompt_library_generated.md:1295`  
  - `prompt_library_generated.md:516`
- `prompt_library_generated.md:1296`  
  - `agents\designer.py:188`
- `prompt_library_generated.md:1297`  
  - `prompt_library_generated.md:517`
- `prompt_library_generated.md:1298`  
  logger.error(f"Stable Diffusion生成失败: {str(e)}")
- `prompt_library_generated.md:1299`  
  - `prompt_library_generated.md:518`
- `prompt_library_generated.md:1300`  
  - `agents\designer.py:191`
- `prompt_library_generated.md:1301`  
  - `prompt_library_generated.md:519`
- `prompt_library_generated.md:1302`  
  def regenerate_image(self, old_path: str, new_prompt: str) -> str:
- `prompt_library_generated.md:1303`  
  - `prompt_library_generated.md:520`
- `prompt_library_generated.md:1304`  
  - `agents\designer.py:193`
- `prompt_library_generated.md:1305`  
  - `prompt_library_generated.md:521`
- `prompt_library_generated.md:1306`  
  重新生成指定图片
- `prompt_library_generated.md:1307`  
  - `prompt_library_generated.md:522`
- `prompt_library_generated.md:1308`  
  - `agents\designer.py:197`
- `prompt_library_generated.md:1309`  
  - `prompt_library_generated.md:523`
- `prompt_library_generated.md:1310`  
  new_prompt: 新的提示词
- `prompt_library_generated.md:1311`  
  - `prompt_library_generated.md:524`
- `prompt_library_generated.md:1312`  
  - `agents\designer.py:202`
- `prompt_library_generated.md:1313`  
  - `prompt_library_generated.md:525`
- `prompt_library_generated.md:1314`  
  logger.info(f"重新生成图片: {old_path}")
- `prompt_library_generated.md:1315`  
  - `prompt_library_generated.md:526`
- `prompt_library_generated.md:1316`  
  - `agents\designer.py:207`
- `prompt_library_generated.md:1317`  
  - `prompt_library_generated.md:527`
- `prompt_library_generated.md:1318`  
  return self._generate_single_image(new_prompt, index)
- `prompt_library_generated.md:1319`  
  - `prompt_library_generated.md:529`
- `prompt_library_generated.md:1320`  
  分析主题，生成内容策略
- `prompt_library_generated.md:1321`  
  - `prompt_library_generated.md:531`
- `prompt_library_generated.md:1322`  
  theme: 用户输入的主题
- `prompt_library_generated.md:1323`  
  - `prompt_library_generated.md:533`
- `prompt_library_generated.md:1324`  
  prompt = f"""
- `prompt_library_generated.md:1325`  
  - `prompt_library_generated.md:535`
- `prompt_library_generated.md:1326`  
  {"role": "user", "content": prompt}
- `prompt_library_generated.md:1327`  
  - `prompt_library_generated.md:537`
- `prompt_library_generated.md:1328`  
  logger.info(f"内容策略生成成功: {strategy}")
- `prompt_library_generated.md:1329`  
  - `prompt_library_generated.md:539`
- `prompt_library_generated.md:1330`  
  logger.error(f"内容策略生成失败: {str(e)}")
- `prompt_library_generated.md:1331`  
  - `prompt_library_generated.md:541`
- `prompt_library_generated.md:1332`  
  user_feedback: 用户反馈意见
- `prompt_library_generated.md:1333`  
  - `prompt_library_generated.md:543`
- `prompt_library_generated.md:1334`  
  prompt = f"""
- `prompt_library_generated.md:1335`  
  - `prompt_library_generated.md:545`
- `prompt_library_generated.md:1336`  
  用户反馈：{user_feedback}
- `prompt_library_generated.md:1337`  
  - `prompt_library_generated.md:547`
- `prompt_library_generated.md:1338`  
  {"role": "user", "content": prompt}
- `prompt_library_generated.md:1339`  
  - `prompt_library_generated.md:549`
- `prompt_library_generated.md:1340`  
  prompt = f"""
- `prompt_library_generated.md:1341`  
  - `prompt_library_generated.md:551`
- `prompt_library_generated.md:1342`  
  {"role": "user", "content": prompt}
- `prompt_library_generated.md:1343`  
  - `prompt_library_generated.md:553`
- `prompt_library_generated.md:1344`  
  """生成摘要"""
- `prompt_library_generated.md:1345`  
  - `prompt_library_generated.md:555`
- `prompt_library_generated.md:1346`  
  生成微信公众号文章
- `prompt_library_generated.md:1347`  
  - `prompt_library_generated.md:557`
- `prompt_library_generated.md:1348`  
  logger.info(f"开始生成公众号文章，主题: {theme}")
- `prompt_library_generated.md:1349`  
  - `prompt_library_generated.md:559`
- `prompt_library_generated.md:1350`  
  # 生成摘要
- `prompt_library_generated.md:1351`  
  - `prompt_library_generated.md:561`
- `prompt_library_generated.md:1352`  
  prompt = f"""
- `prompt_library_generated.md:1353`  
  - `prompt_library_generated.md:563`
- `prompt_library_generated.md:1354`  
  messages=[{'role': 'user', 'content': prompt}],
- `prompt_library_generated.md:1355`  
  - `prompt_library_generated.md:565`
- `prompt_library_generated.md:1356`  
  prompt = f"""
- `prompt_library_generated.md:1357`  
  - `prompt_library_generated.md:567`
- `prompt_library_generated.md:1358`  
  messages=[{'role': 'user', 'content': prompt}],
- `prompt_library_generated.md:1359`  
  - `prompt_library_generated.md:569`
- `prompt_library_generated.md:1360`  
  """生成文章摘要"""
- `prompt_library_generated.md:1361`  
  - `prompt_library_generated.md:571`
- `prompt_library_generated.md:1362`  
  prompt = f"""
- `prompt_library_generated.md:1363`  
  - `prompt_library_generated.md:573`
- `prompt_library_generated.md:1364`  
  {"role": "user", "content": prompt}
- `prompt_library_generated.md:1365`  
  - `prompt_library_generated.md:575`
- `prompt_library_generated.md:1366`  
  feedback: 用户反馈
- `prompt_library_generated.md:1367`  
  - `prompt_library_generated.md:577`
- `prompt_library_generated.md:1368`  
  prompt = f"""
- `prompt_library_generated.md:1369`  
  - `prompt_library_generated.md:579`
- `prompt_library_generated.md:1370`  
  用户反馈：{feedback}
- `prompt_library_generated.md:1371`  
  - `prompt_library_generated.md:581`
- `prompt_library_generated.md:1372`  
  {"role": "user", "content": prompt}
- `prompt_library_generated.md:1373`  
  - `prompt_library_generated.md:583`
- `prompt_library_generated.md:1374`  
  prompt = f"""
- `prompt_library_generated.md:1375`  
  - `prompt_library_generated.md:585`
- `prompt_library_generated.md:1376`  
  {"role": "user", "content": prompt}
- `prompt_library_generated.md:1377`  
  - `prompt_library_generated.md:587`
- `prompt_library_generated.md:1378`  
  """生成预览 - 异步处理"""
- `prompt_library_generated.md:1379`  
  - `prompt_library_generated.md:589`
- `prompt_library_generated.md:1380`  
  print(f"\n收到生成预览请求: {theme}")
- `prompt_library_generated.md:1381`  
  - `prompt_library_generated.md:591`
- `prompt_library_generated.md:1382`  
  print(f"生成预览失败: {e}")
- `prompt_library_generated.md:1383`  
  - `prompt_library_generated.md:593`
- `prompt_library_generated.md:1384`  
  'message': f'生成失败: {str(e)}'
- `prompt_library_generated.md:1385`  
  - `prompt_library_generated.md:595`
- `prompt_library_generated.md:1386`  
  """异步生成预览"""
- `prompt_library_generated.md:1387`  
  - `prompt_library_generated.md:597`
- `prompt_library_generated.md:1388`  
  5. [图片生成方案](#5-图片生成方案)
- `prompt_library_generated.md:1389`  
  - `prompt_library_generated.md:599`
- `prompt_library_generated.md:1390`  
  ✅ **免费额度高**：新用户赠送500万Tokens（约相当于2000元OpenAI额度）
- `prompt_library_generated.md:1391`  
  - `prompt_library_generated.md:601`
- `prompt_library_generated.md:1392`  
  6. 复制生成的API Key（格式：sk-xxxxxxxx）
- `prompt_library_generated.md:1393`  
  - `prompt_library_generated.md:603`
- `prompt_library_generated.md:1394`  
  - 新用户免费额度：500万Tokens
- `prompt_library_generated.md:1395`  
  - `prompt_library_generated.md:605`
- `prompt_library_generated.md:1396`  
  ✅ 新用户赠送免费额度
- `prompt_library_generated.md:1397`  
  - `prompt_library_generated.md:607`
- `prompt_library_generated.md:1398`  
  2. 复制生成的Key
- `prompt_library_generated.md:1399`  
  - `prompt_library_generated.md:609`
- `prompt_library_generated.md:1400`  
  - 新用户免费试用
- `prompt_library_generated.md:1401`  
  - `prompt_library_generated.md:611`
- `prompt_library_generated.md:1402`  
  ✅ 新用户免费额度
- `prompt_library_generated.md:1403`  
  - `prompt_library_generated.md:613`
- `prompt_library_generated.md:1404`  
  - 新用户免费额度
- `prompt_library_generated.md:1405`  
  - `prompt_library_generated.md:615`
- `prompt_library_generated.md:1406`  
  ✅ 新用户免费额度
- `prompt_library_generated.md:1407`  
  - `prompt_library_generated.md:617`
- `prompt_library_generated.md:1408`  
  - 新用户免费额度
- `prompt_library_generated.md:1409`  
  - `prompt_library_generated.md:619`
- `prompt_library_generated.md:1410`  
  ## 5. 图片生成方案
- `prompt_library_generated.md:1411`  
  - `prompt_library_generated.md:621`
- `prompt_library_generated.md:1412`  
  # 复制配置模板
- `prompt_library_generated.md:1413`  
  - `prompt_library_generated.md:623`
- `prompt_library_generated.md:1414`  
  | 服务商 | 新用户免费 | 价格 | 速度 | 中文支持 | 推荐度 |
- `prompt_library_generated.md:1415`  
  - `prompt_library_generated.md:625`
- `prompt_library_generated.md:1416`  
  ### Q4: 图片生成必须配置吗？
- `prompt_library_generated.md:1417`  
  - `prompt_library_generated.md:627`
- `prompt_library_generated.md:1418`  
  # 自动生成项目文档 - 20260206205332
- `prompt_library_generated.md:1419`  
  - `prompt_library_generated.md:629`
- `prompt_library_generated.md:1420`  
  > 生成时间: 2026-02-11 17:01
- `prompt_library_generated.md:1421`  
  - `prompt_library_generated.md:631`
- `prompt_library_generated.md:1422`  
  - 🟢 项目名称: 小红书内容生成与发布平台
- `prompt_library_generated.md:1423`  
  - `prompt_library_generated.md:633`
- `prompt_library_generated.md:1424`  
  - 🟢 图片生成（Stable Diffusion）
- `prompt_library_generated.md:1425`  
  - `prompt_library_generated.md:635`
- `prompt_library_generated.md:1426`  
  - 🔴 持久化用户数据与内容库（建议补充）
- `prompt_library_generated.md:1427`  
  - `prompt_library_generated.md:637`
- `prompt_library_generated.md:1428`  
  生成时间: 2026-02-06
- `prompt_library_generated.md:1429`  
  - `prompt_library_generated.md:639`
- `prompt_library_generated.md:1430`  
  - [x] .env.example（配置模板）
- `prompt_library_generated.md:1431`  
  - `prompt_library_generated.md:641`
- `prompt_library_generated.md:1432`  
  ├── generated_images/            # 生成的图片目录
- `prompt_library_generated.md:1433`  
  - `prompt_library_generated.md:643`
- `prompt_library_generated.md:1434`  
  ├── .env.example                 # 配置模板
- `prompt_library_generated.md:1435`  
  - `prompt_library_generated.md:645`
- `prompt_library_generated.md:1436`  
  ### Windows用户
- `prompt_library_generated.md:1437`  
  - `prompt_library_generated.md:647`
- `prompt_library_generated.md:1438`  
  ✅ 内容策略生成
- `prompt_library_generated.md:1439`  
  - `prompt_library_generated.md:649`
- `prompt_library_generated.md:1440`  
  ✅ AI图片生成
- `prompt_library_generated.md:1441`  
  - `prompt_library_generated.md:651`
- `prompt_library_generated.md:1442`  
  开始使用系统生成小红书内容！🎉
- `prompt_library_generated.md:1443`  
  - `prompt_library_generated.md:653`
- `prompt_library_generated.md:1444`  
  ### 方案3：使用Anaconda（适合数据科学用户）
- `prompt_library_generated.md:1445`  
  - `prompt_library_generated.md:655`
- `prompt_library_generated.md:1446`  
  #### 步骤3：使用Anaconda Prompt
- `prompt_library_generated.md:1447`  
  - `prompt_library_generated.md:657`
- `prompt_library_generated.md:1448`  
  - 搜索 "Anaconda Prompt"
- `prompt_library_generated.md:1449`  
  - `prompt_library_generated.md:659`
- `prompt_library_generated.md:1450`  
  3. 在"用户变量"或"系统变量"中找到"Path"
- `prompt_library_generated.md:1451`  
  - `prompt_library_generated.md:661`
- `prompt_library_generated.md:1452`  
  - 在"用户变量"中找到"Path"
- `prompt_library_generated.md:1453`  
  - `prompt_library_generated.md:663`
- `prompt_library_generated.md:1454`  
  ### 方案5：使用Anaconda Prompt
- `prompt_library_generated.md:1455`  
  - `prompt_library_generated.md:665`
- `prompt_library_generated.md:1456`  
  2. 搜索 "Anaconda Prompt"
- `prompt_library_generated.md:1457`  
  - `prompt_library_generated.md:667`
- `prompt_library_generated.md:1458`  
  3. 打开Anaconda Prompt
- `prompt_library_generated.md:1459`  
  - `prompt_library_generated.md:669`
- `prompt_library_generated.md:1460`  
  ## Windows 用户
- `prompt_library_generated.md:1461`  
  - `prompt_library_generated.md:671`
- `prompt_library_generated.md:1462`  
  ## Linux / Mac 用户
- `prompt_library_generated.md:1463`  
  - `prompt_library_generated.md:673`
- `prompt_library_generated.md:1464`  
  2. 生成预览 - 生成内容后确认
- `prompt_library_generated.md:1465`  
  - `prompt_library_generated.md:675`
- `prompt_library_generated.md:1466`  
  A: Windows用户尝试使用 `python3` 或 `py` 命令
- `prompt_library_generated.md:1467`  
  - `prompt_library_generated.md:677`
- `prompt_library_generated.md:1468`  
  - **人工确认**：生成内容后可预览和修改
- `prompt_library_generated.md:1469`  
  - `prompt_library_generated.md:679`
- `prompt_library_generated.md:1470`  
  # 复制配置模板
- `prompt_library_generated.md:1471`  
  - `prompt_library_generated.md:681`
- `prompt_library_generated.md:1472`  
  2. 注册账号（新用户赠送500万免费Tokens）
- `prompt_library_generated.md:1473`  
  - `prompt_library_generated.md:683`
- `prompt_library_generated.md:1474`  
  用户输入主题
- `prompt_library_generated.md:1475`  
  - `prompt_library_generated.md:685`
- `prompt_library_generated.md:1476`  
  复制配置模板：
- `prompt_library_generated.md:1477`  
  - `prompt_library_generated.md:687`
- `prompt_library_generated.md:1478`  
  2. 生成预览 - 生成内容后确认
- `prompt_library_generated.md:1479`  
  - `prompt_library_generated.md:689`
- `prompt_library_generated.md:1480`  
  # 生成并发布
- `prompt_library_generated.md:1481`  
  - `prompt_library_generated.md:691`
- `prompt_library_generated.md:1482`  
  - 支持根据反馈重新生成
- `prompt_library_generated.md:1483`  
  - `prompt_library_generated.md:693`
- `prompt_library_generated.md:1484`  
  - 生成AI绘画提示词
- `prompt_library_generated.md:1485`  
  - `prompt_library_generated.md:695`
- `prompt_library_generated.md:1486`  
  ├── .env.example          # 配置模板
- `prompt_library_generated.md:1487`  
  - `prompt_library_generated.md:697`
- `prompt_library_generated.md:1488`  
  ├── generated_images/     # 生成的图片
- `prompt_library_generated.md:1489`  
  - `prompt_library_generated.md:699`
- `prompt_library_generated.md:1490`  
  3. **图片生成**：DALL-E 3需要付费，Stable Diffusion需本地部署
- `prompt_library_generated.md:1491`  
  - `prompt_library_generated.md:701`
- `prompt_library_generated.md:1492`  
  自动回复或收集用户反馈。
- `prompt_library_generated.md:1493`  
  - `prompt_library_generated.md:703`
- `prompt_library_generated.md:1494`  
  - AI生成配图（可选）
- `prompt_library_generated.md:1495`  
  - `prompt_library_generated.md:705`
- `prompt_library_generated.md:1496`  
  2. 生成预览 - 生成内容后确认
- `prompt_library_generated.md:1497`  
  - `prompt_library_generated.md:707`
- `prompt_library_generated.md:1498`  
  3. 生成配图
- `prompt_library_generated.md:1499`  
  - `prompt_library_generated.md:709`
- `prompt_library_generated.md:1500`  
  **适用场景：** 熟悉主题，信任AI生成结果
- `prompt_library_generated.md:1501`  
  - `prompt_library_generated.md:711`
- `prompt_library_generated.md:1502`  
  AI自动生成内容
- `prompt_library_generated.md:1503`  
  - `prompt_library_generated.md:713`
- `prompt_library_generated.md:1504`  
  ### 2. 生成预览模式（推荐新手）
- `prompt_library_generated.md:1505`  
  - `prompt_library_generated.md:715`
- `prompt_library_generated.md:1506`  
  AI生成内容
- `prompt_library_generated.md:1507`  
  - `prompt_library_generated.md:717`
- `prompt_library_generated.md:1508`  
  3. 重新生成图片
- `prompt_library_generated.md:1509`  
  - `prompt_library_generated.md:719`
- `prompt_library_generated.md:1510`  
  生成AI绘画提示词
- `prompt_library_generated.md:1511`  
  - `prompt_library_generated.md:721`
- `prompt_library_generated.md:1512`  
  生成高质量配图
- `prompt_library_generated.md:1513`  
  - `prompt_library_generated.md:723`
- `prompt_library_generated.md:1514`  
  2. 选择"让AI重新生成"
- `prompt_library_generated.md:1515`  
  - `prompt_library_generated.md:725`
- `prompt_library_generated.md:1516`  
  ### 3. 图片生成技巧
- `prompt_library_generated.md:1517`  
  - `prompt_library_generated.md:727`
- `prompt_library_generated.md:1518`  
  1. 使用"生成预览"模式
- `prompt_library_generated.md:1519`  
  - `prompt_library_generated.md:729`
- `prompt_library_generated.md:1520`  
  3. 让AI根据反馈重新生成
- `prompt_library_generated.md:1521`  
  - `prompt_library_generated.md:731`
- `prompt_library_generated.md:1522`  
  ### Q3: 图片生成失败？
- `prompt_library_generated.md:1523`  
  - `prompt_library_generated.md:733`
- `prompt_library_generated.md:1524`  
  - 新用户免费：500万Tokens
- `prompt_library_generated.md:1525`  
  - `prompt_library_generated.md:735`
- `prompt_library_generated.md:1526`  
  - **相当于每次生成成本 < ¥0.01**
- `prompt_library_generated.md:1527`  
  - `prompt_library_generated.md:737`
- `prompt_library_generated.md:1528`  
  输入你的第一个主题，让AI帮你生成小红书内容！
- `prompt_library_generated.md:1529`  
  - `prompt_library_generated.md:739`
- `prompt_library_generated.md:1530`  
  ### Windows用户：
- `prompt_library_generated.md:1531`  
  - `prompt_library_generated.md:741`
- `prompt_library_generated.md:1532`  
  ## Windows用户（如果python命令不工作）
- `prompt_library_generated.md:1533`  
  - `prompt_library_generated.md:743`
- `prompt_library_generated.md:1534`  
  1. **快速发布** - 输入主题，自动生成并发布
- `prompt_library_generated.md:1535`  
  - `prompt_library_generated.md:745`
- `prompt_library_generated.md:1536`  
  2. **生成预览** - 生成内容后手动确认再发布
- `prompt_library_generated.md:1537`  
  - `prompt_library_generated.md:747`
- `prompt_library_generated.md:1538`  
  - **免费额度**: 500万Tokens（新用户）
- `prompt_library_generated.md:1539`  
  - `prompt_library_generated.md:749`
- `prompt_library_generated.md:1540`  
  - 自动写作：生成高质量公众号文章
- `prompt_library_generated.md:1541`  
  - `prompt_library_generated.md:751`
- `prompt_library_generated.md:1542`  
  - 图片生成：为文章生成配图（可选）
- `prompt_library_generated.md:1543`  
  - `prompt_library_generated.md:753`
- `prompt_library_generated.md:1544`  
  - 点击"重置"或"生成"获取 AppSecret
- `prompt_library_generated.md:1545`  
  - `prompt_library_generated.md:755`
- `prompt_library_generated.md:1546`  
  1. **快速发布** - 输入主题，自动生成并发布
- `prompt_library_generated.md:1547`  
  - `prompt_library_generated.md:757`
- `prompt_library_generated.md:1548`  
  2. **生成预览** - 生成文章后手动确认再发布
- `prompt_library_generated.md:1549`  
  - `prompt_library_generated.md:759`
- `prompt_library_generated.md:1550`  
  适合快速生成并发布文章的场景：
- `prompt_library_generated.md:1551`  
  - `prompt_library_generated.md:761`
- `prompt_library_generated.md:1552`  
  - （可选）生成配图
- `prompt_library_generated.md:1553`  
  - `prompt_library_generated.md:763`
- `prompt_library_generated.md:1554`  
  ### 2. 生成预览模式
- `prompt_library_generated.md:1555`  
  - `prompt_library_generated.md:765`
- `prompt_library_generated.md:1556`  
  3. 系统生成文章并显示预览
- `prompt_library_generated.md:1557`  
  - `prompt_library_generated.md:767`
- `prompt_library_generated.md:1558`  
  - 图片生成引擎
- `prompt_library_generated.md:1559`  
  - `prompt_library_generated.md:769`
- `prompt_library_generated.md:1560`  
  - 生成摘要
- `prompt_library_generated.md:1561`  
  - `prompt_library_generated.md:771`
- `prompt_library_generated.md:1562`  
  - 生成图片提示词
- `prompt_library_generated.md:1563`  
  - `prompt_library_generated.md:773`
- `prompt_library_generated.md:1564`  
  - 调用图片生成API
- `prompt_library_generated.md:1565`  
  - `prompt_library_generated.md:775`
- `prompt_library_generated.md:1566`  
  - 保存生成的图片
- `prompt_library_generated.md:1567`  
  - `prompt_library_generated.md:777`
- `prompt_library_generated.md:1568`  
  ### 内容生成特点
- `prompt_library_generated.md:1569`  
  - `prompt_library_generated.md:779`
- `prompt_library_generated.md:1570`  
  - **月之暗面**：适合中文生成
- `prompt_library_generated.md:1571`  
  - `prompt_library_generated.md:781`
- `prompt_library_generated.md:1572`  
  ### 图片生成配置
- `prompt_library_generated.md:1573`  
  - `prompt_library_generated.md:783`
- `prompt_library_generated.md:1574`  
  # 图片生成引擎
- `prompt_library_generated.md:1575`  
  - `prompt_library_generated.md:785`
- `prompt_library_generated.md:1576`  
  **注意**：图片生成是可选的，未配置时系统会跳过图片生成步骤。
- `prompt_library_generated.md:1577`  
  - `prompt_library_generated.md:787`
- `prompt_library_generated.md:1578`  
  ### Q4: 生成的文章质量不理想
- `prompt_library_generated.md:1579`  
  - `prompt_library_generated.md:789`
- `prompt_library_generated.md:1580`  
  3. 生成预览模式：先预览再决定是否发布
- `prompt_library_generated.md:1581`  
  - `prompt_library_generated.md:791`
- `prompt_library_generated.md:1582`  
  - 或者在生成预览模式下，可以取消发布，然后修改主题重新生成
- `prompt_library_generated.md:1583`  
  - `prompt_library_generated.md:793`
- `prompt_library_generated.md:1584`  
  - `generated_images/` - 生成的图片
- `prompt_library_generated.md:1585`  
  - `prompt_library_generated.md:795`
- `prompt_library_generated.md:1586`  
  ### 自定义文章模板
- `prompt_library_generated.md:1587`  
  - `prompt_library_generated.md:797`
- `prompt_library_generated.md:1588`  
  可以修改 `agents/wechat_writer.py` 来调整文章生成逻辑：
- `prompt_library_generated.md:1589`  
  - `prompt_library_generated.md:799`
- `prompt_library_generated.md:1590`  
  # 在 _generate_content 方法中修改 prompt
- `prompt_library_generated.md:1591`  
  - `prompt_library_generated.md:801`
- `prompt_library_generated.md:1592`  
  1. 先生成文章并保存为草稿
- `prompt_library_generated.md:1593`  
  - `prompt_library_generated.md:803`
- `prompt_library_generated.md:1594`  
  - ✅ 支持微信公众号文章生成
- `prompt_library_generated.md:1595`  
  - `prompt_library_generated.md:805`
- `prompt_library_generated.md:1596`  
  - ✅ 支持图片生成（可选）
- `prompt_library_generated.md:1597`  
  - `prompt_library_generated.md:807`
- `prompt_library_generated.md:1598`  
  ### 🥉 方案3：使用Anaconda（适合有经验的用户）
- `prompt_library_generated.md:1599`  
  - `prompt_library_generated.md:809`
- `prompt_library_generated.md:1600`  
  4. 安装完成后，打开 "Anaconda Prompt"（从开始菜单）
- `prompt_library_generated.md:1601`  
  - `prompt_library_generated.md:811`
- `prompt_library_generated.md:1602`  
  **启动系统（在Anaconda Prompt中）：**
- `prompt_library_generated.md:1603`  
  - `prompt_library_generated.md:813`
- `prompt_library_generated.md:1604`  
  ✅ **快速发布** - 输入主题，一键生成并发布文章
- `prompt_library_generated.md:1605`  
  - `prompt_library_generated.md:815`
- `prompt_library_generated.md:1606`  
  ✅ **生成预览** - 先生成内容预览，确认后再发布
- `prompt_library_generated.md:1607`  
  - `prompt_library_generated.md:817`
- `prompt_library_generated.md:1608`  
  **Windows用户：**
- `prompt_library_generated.md:1609`  
  - `prompt_library_generated.md:819`
- `prompt_library_generated.md:1610`  
  2. 选择是否生成配图（默认不生成）
- `prompt_library_generated.md:1611`  
  - `prompt_library_generated.md:821`
- `prompt_library_generated.md:1612`  
  ### 生成预览
- `prompt_library_generated.md:1613`  
  - `prompt_library_generated.md:823`
- `prompt_library_generated.md:1614`  
  2. 点击"生成内容"按钮
- `prompt_library_generated.md:1615`  
  - `prompt_library_generated.md:825`
- `prompt_library_generated.md:1616`  
  5. 或点击"重新生成"重新创作
- `prompt_library_generated.md:1617`  
  - `prompt_library_generated.md:827`
- `prompt_library_generated.md:1618`  
  **图片生成配置：**
- `prompt_library_generated.md:1619`  
  - `prompt_library_generated.md:829`
- `prompt_library_generated.md:1620`  
  - 选择图片生成引擎
- `prompt_library_generated.md:1621`  
  - `prompt_library_generated.md:831`
- `prompt_library_generated.md:1622`  
  - 默认为"不生成图片"
- `prompt_library_generated.md:1623`  
  - `prompt_library_generated.md:833`
- `prompt_library_generated.md:1624`  
  - `POST /api/generate_preview` - 生成预览
- `prompt_library_generated.md:1625`  
  - `prompt_library_generated.md:835`
- `prompt_library_generated.md:1626`  
  用户输入主题
- `prompt_library_generated.md:1627`  
  - `prompt_library_generated.md:837`
- `prompt_library_generated.md:1628`  
  1. **用户认证**
- `prompt_library_generated.md:1629`  
  - `prompt_library_generated.md:839`
- `prompt_library_generated.md:1630`  
  - 支持多用户管理
- `prompt_library_generated.md:1631`  
  - `prompt_library_generated.md:841`
- `prompt_library_generated.md:1632`  
  3. **模板管理**
- `prompt_library_generated.md:1633`  
  - `prompt_library_generated.md:843`
- `prompt_library_generated.md:1634`  
  - 保存常用的文章模板
- `prompt_library_generated.md:1635`  
  - `prompt_library_generated.md:845`
- `prompt_library_generated.md:1636`  
  - 快速套用模板
- `prompt_library_generated.md:1637`  
  - `prompt_library_generated.md:848`
- `prompt_library_generated.md:1638`  
  - 可将上述条目转为可调用模板，按目的快速检索
- `prompt_library_generated.md:1640`  
  ### 方案3：使用Anaconda（适合数据科学用户）
- `prompt_library_generated.md:1642`  
  #### 步骤3：使用Anaconda Prompt
- `prompt_library_generated.md:1644`  
  - 搜索 "Anaconda Prompt"
- `prompt_library_generated.md:1646`  
  3. 在"用户变量"或"系统变量"中找到"Path"
- `prompt_library_generated.md:1648`  
  - 在"用户变量"中找到"Path"
- `prompt_library_generated.md:1650`  
  ### 方案5：使用Anaconda Prompt
- `prompt_library_generated.md:1652`  
  2. 搜索 "Anaconda Prompt"
- `prompt_library_generated.md:1654`  
  3. 打开Anaconda Prompt
- `prompt_library_generated.md:1656`  
  ## Windows 用户
- `prompt_library_generated.md:1658`  
  ## Linux / Mac 用户
- `prompt_library_generated.md:1660`  
  2. 生成预览 - 生成内容后确认
- `prompt_library_generated.md:1662`  
  A: Windows用户尝试使用 `python3` 或 `py` 命令
- `prompt_library_generated.md:1664`  
  - **人工确认**：生成内容后可预览和修改
- `prompt_library_generated.md:1666`  
  # 复制配置模板
- `prompt_library_generated.md:1668`  
  2. 注册账号（新用户赠送500万免费Tokens）
- `prompt_library_generated.md:1670`  
  用户输入主题
- `prompt_library_generated.md:1672`  
  复制配置模板：
- `prompt_library_generated.md:1674`  
  2. 生成预览 - 生成内容后确认
- `prompt_library_generated.md:1676`  
  # 生成并发布
- `prompt_library_generated.md:1678`  
  - 支持根据反馈重新生成
- `prompt_library_generated.md:1680`  
  - 生成AI绘画提示词
- `prompt_library_generated.md:1682`  
  ├── .env.example          # 配置模板
- `prompt_library_generated.md:1684`  
  ├── generated_images/     # 生成的图片
- `prompt_library_generated.md:1686`  
  3. **图片生成**：DALL-E 3需要付费，Stable Diffusion需本地部署
- `prompt_library_generated.md:1688`  
  自动回复或收集用户反馈。
- `prompt_library_generated.md:1690`  
  > 自动生成的 Skill 相关文档统一索引，方便快速定位
- `prompt_library_generated.md:1692`  
  | Skill 名称 | 文档名称 | 存储位置 | 生成时间 |
- `prompt_library_generated.md:1694`  
  | **prompt-collector** | `prompt_library_generated.md` | `c:/Users/zhaoy/CodeBuddy/20260206205332/prompt_library_generated.md` | 自动生成 |
- `prompt_library_generated.md:1696`  
  | **project-analyzer** | `project_requirements_generated.md` | `c:/Users/zhaoy/CodeBuddy/20260206205332/project_requirements_generated.md` | 自动生成 |
- `prompt_library_generated.md:1698`  
  | **auto-doc-generator** | `auto_generated_documentation.md` | `c:/Users/zhaoy/CodeBuddy/20260206205332/auto_generated_documentation.md` | 自动生成 |
- `prompt_library_generated.md:1700`  
  | **SKILL_REGISTRY** | `SKILL_REGISTRY.md` | `c:/Users/zhaoy/CodeBuddy/20260206205332/SKILL_REGISTRY.md` | 手动生成 |
- `prompt_library_generated.md:1702`  
  ├── prompt_library_generated.md         ← prompt-collector 文档
- `prompt_library_generated.md:1704`  
  # Skill 注册清单（用户 Skill）
- `prompt_library_generated.md:1706`  
  | **prompt-collector** | 收集并分类项目中的提示词/模板，生成可检索的提示词库 | 收集复用提示词、按目的分类管理 | `prompt_library_generated.md` | `.codebuddy/skills/prompt-collector/` |
- `prompt_library_generated.md:1708`  
  - 示例：`@auto-doc-generator` 可对当前项目生成完整文档
- `prompt_library_generated.md:1710`  
  - AI生成配图（可选）
- `prompt_library_generated.md:1712`  
  2. 生成预览 - 生成内容后确认
- `prompt_library_generated.md:1714`  
  3. 生成配图
- `prompt_library_generated.md:1716`  
  **适用场景：** 熟悉主题，信任AI生成结果
- `prompt_library_generated.md:1718`  
  AI自动生成内容
- `prompt_library_generated.md:1720`  
  ### 2. 生成预览模式（推荐新手）
- `prompt_library_generated.md:1722`  
  AI生成内容
- `prompt_library_generated.md:1724`  
  3. 重新生成图片
- `prompt_library_generated.md:1726`  
  生成AI绘画提示词
- `prompt_library_generated.md:1728`  
  生成高质量配图
- `prompt_library_generated.md:1730`  
  2. 选择"让AI重新生成"
- `prompt_library_generated.md:1732`  
  ### 3. 图片生成技巧
- `prompt_library_generated.md:1734`  
  1. 使用"生成预览"模式
- `prompt_library_generated.md:1736`  
  3. 让AI根据反馈重新生成
- `prompt_library_generated.md:1738`  
  ### Q3: 图片生成失败？
- `prompt_library_generated.md:1740`  
  - 新用户免费：500万Tokens
- `prompt_library_generated.md:1742`  
  - **相当于每次生成成本 < ¥0.01**
- `prompt_library_generated.md:1744`  
  输入你的第一个主题，让AI帮你生成小红书内容！
- `prompt_library_generated.md:1746`  
  ### Windows用户：
- `prompt_library_generated.md:1748`  
  ## Windows用户（如果python命令不工作）
- `prompt_library_generated.md:1750`  
  1. **快速发布** - 输入主题，自动生成并发布
- `prompt_library_generated.md:1752`  
  2. **生成预览** - 生成内容后手动确认再发布
- `prompt_library_generated.md:1754`  
  - **免费额度**: 500万Tokens（新用户）
- `prompt_library_generated.md:1756`  
  - 自动写作：生成高质量公众号文章
- `prompt_library_generated.md:1758`  
  - 图片生成：为文章生成配图（可选）
- `prompt_library_generated.md:1760`  
  - 点击"重置"或"生成"获取 AppSecret
- `prompt_library_generated.md:1762`  
  1. **快速发布** - 输入主题，自动生成并发布
- `prompt_library_generated.md:1764`  
  2. **生成预览** - 生成文章后手动确认再发布
- `prompt_library_generated.md:1766`  
  适合快速生成并发布文章的场景：
- `prompt_library_generated.md:1768`  
  - （可选）生成配图
- `prompt_library_generated.md:1770`  
  ### 2. 生成预览模式
- `prompt_library_generated.md:1772`  
  3. 系统生成文章并显示预览
- `prompt_library_generated.md:1774`  
  - 图片生成引擎
- `prompt_library_generated.md:1776`  
  - 生成摘要
- `prompt_library_generated.md:1778`  
  - 生成图片提示词
- `prompt_library_generated.md:1780`  
  - 调用图片生成API
- `prompt_library_generated.md:1782`  
  - 保存生成的图片
- `prompt_library_generated.md:1784`  
  ### 内容生成特点
- `prompt_library_generated.md:1786`  
  - **月之暗面**：适合中文生成
- `prompt_library_generated.md:1788`  
  ### 图片生成配置
- `prompt_library_generated.md:1790`  
  # 图片生成引擎
- `prompt_library_generated.md:1792`  
  **注意**：图片生成是可选的，未配置时系统会跳过图片生成步骤。
- `prompt_library_generated.md:1794`  
  ### Q4: 生成的文章质量不理想
- `prompt_library_generated.md:1796`  
  3. 生成预览模式：先预览再决定是否发布
- `prompt_library_generated.md:1798`  
  - 或者在生成预览模式下，可以取消发布，然后修改主题重新生成
- `prompt_library_generated.md:1800`  
  - `generated_images/` - 生成的图片
- `prompt_library_generated.md:1802`  
  ### 自定义文章模板
- `prompt_library_generated.md:1804`  
  可以修改 `agents/wechat_writer.py` 来调整文章生成逻辑：
- `prompt_library_generated.md:1806`  
  # 在 _generate_content 方法中修改 prompt
- `prompt_library_generated.md:1808`  
  1. 先生成文章并保存为草稿
- `prompt_library_generated.md:1810`  
  - ✅ 支持微信公众号文章生成
- `prompt_library_generated.md:1812`  
  - ✅ 支持图片生成（可选）
- `prompt_library_generated.md:1814`  
  ### 🥉 方案3：使用Anaconda（适合有经验的用户）
- `prompt_library_generated.md:1816`  
  4. 安装完成后，打开 "Anaconda Prompt"（从开始菜单）
- `prompt_library_generated.md:1818`  
  **启动系统（在Anaconda Prompt中）：**
- `prompt_library_generated.md:1820`  
  ✅ **快速发布** - 输入主题，一键生成并发布文章
- `prompt_library_generated.md:1822`  
  ✅ **生成预览** - 先生成内容预览，确认后再发布
- `prompt_library_generated.md:1824`  
  **Windows用户：**
- `prompt_library_generated.md:1826`  
  2. 选择是否生成配图（默认不生成）
- `prompt_library_generated.md:1828`  
  ### 生成预览
- `prompt_library_generated.md:1830`  
  2. 点击"生成内容"按钮
- `prompt_library_generated.md:1832`  
  5. 或点击"重新生成"重新创作
- `prompt_library_generated.md:1834`  
  **图片生成配置：**
- `prompt_library_generated.md:1836`  
  - 选择图片生成引擎
- `prompt_library_generated.md:1838`  
  - 默认为"不生成图片"
- `prompt_library_generated.md:1840`  
  - `POST /api/generate_preview` - 生成预览
- `prompt_library_generated.md:1842`  
  用户输入主题
- `prompt_library_generated.md:1844`  
  1. **用户认证**
- `prompt_library_generated.md:1846`  
  - 支持多用户管理
- `prompt_library_generated.md:1848`  
  3. **模板管理**
- `prompt_library_generated.md:1850`  
  - 保存常用的文章模板
- `prompt_library_generated.md:1852`  
  - 快速套用模板
- `prompt_library_generated.md:1855`  
  - 可将上述条目转为可调用模板，按目的快速检索
- `Python安装指南.md:94`  
  ### 方案3：使用Anaconda（适合数据科学用户）
- `Python安装指南.md:106`  
  #### 步骤3：使用Anaconda Prompt
- `Python安装指南.md:109`  
  - 搜索 "Anaconda Prompt"
- `Python安装指南.md:196`  
  3. 在"用户变量"或"系统变量"中找到"Path"
- `Python已安装但仍无法运行.md:84`  
  - 在"用户变量"中找到"Path"
- `Python已安装但仍无法运行.md:95`  
  ### 方案5：使用Anaconda Prompt
- `Python已安装但仍无法运行.md:100`  
  2. 搜索 "Anaconda Prompt"
- `Python已安装但仍无法运行.md:101`  
  3. 打开Anaconda Prompt
- `QUICKSTART.md:3`  
  ## Windows 用户
- `QUICKSTART.md:25`  
  ## Linux / Mac 用户
- `QUICKSTART.md:42`  
  2. 生成预览 - 生成内容后确认
- `QUICKSTART.md:50`  
  A: Windows用户尝试使用 `python3` 或 `py` 命令
- `README.md:13`  
  - **人工确认**：生成内容后可预览和修改
- `README.md:33`  
  # 复制配置模板
- `README.md:43`  
  2. 注册账号（新用户赠送500万免费Tokens）
- `README.md:50`  
  用户输入主题
- `README.md:75`  
  复制配置模板：
- `README.md:119`  
  2. 生成预览 - 生成内容后确认
- `README.md:137`  
  # 生成并发布
- `README.md:154`  
  - 支持根据反馈重新生成
- `README.md:157`  
  - 生成AI绘画提示词
- `README.md:181`  
  ├── .env.example          # 配置模板
- `README.md:189`  
  ├── generated_images/     # 生成的图片
- `README.md:198`  
  3. **图片生成**：DALL-E 3需要付费，Stable Diffusion需本地部署
- `README.md:214`  
  自动回复或收集用户反馈。
- `SKILL_DOC_INDEX.md:3`  
  > 自动生成的 Skill 相关文档统一索引，方便快速定位
- `SKILL_DOC_INDEX.md:7`  
  | Skill 名称 | 文档名称 | 存储位置 | 生成时间 |
- `SKILL_DOC_INDEX.md:9`  
  | **prompt-collector** | `prompt_library_generated.md` | `c:/Users/zhaoy/CodeBuddy/20260206205332/prompt_library_generated.md` | 自动生成 |
- `SKILL_DOC_INDEX.md:10`  
  | **project-analyzer** | `project_requirements_generated.md` | `c:/Users/zhaoy/CodeBuddy/20260206205332/project_requirements_generated.md` | 自动生成 |
- `SKILL_DOC_INDEX.md:11`  
  | **auto-doc-generator** | `auto_generated_documentation.md` | `c:/Users/zhaoy/CodeBuddy/20260206205332/auto_generated_documentation.md` | 自动生成 |
- `SKILL_DOC_INDEX.md:12`  
  | **SKILL_REGISTRY** | `SKILL_REGISTRY.md` | `c:/Users/zhaoy/CodeBuddy/20260206205332/SKILL_REGISTRY.md` | 手动生成 |
- `SKILL_DOC_INDEX.md:25`  
  ├── prompt_library_generated.md         ← prompt-collector 文档
- `SKILL_REGISTRY.md:1`  
  # Skill 注册清单（用户 Skill）
- `SKILL_REGISTRY.md:9`  
  | **prompt-collector** | 收集并分类项目中的提示词/模板，生成可检索的提示词库 | 收集复用提示词、按目的分类管理 | `prompt_library_generated.md` | `.codebuddy/skills/prompt-collector/` |
- `SKILL_REGISTRY.md:15`  
  - 示例：`@auto-doc-generator` 可对当前项目生成完整文档
- `使用指南.md:13`  
  - AI生成配图（可选）
- `使用指南.md:50`  
  2. 生成预览 - 生成内容后确认
- `使用指南.md:70`  
  3. 生成配图
- `使用指南.md:80`  
  **适用场景：** 熟悉主题，信任AI生成结果
- `使用指南.md:86`  
  AI自动生成内容
- `使用指南.md:99`  
  ### 2. 生成预览模式（推荐新手）
- `使用指南.md:107`  
  AI生成内容
- `使用指南.md:114`  
  3. 重新生成图片
- `使用指南.md:193`  
  生成AI绘画提示词
- `使用指南.md:197`  
  生成高质量配图
- `使用指南.md:247`  
  2. 选择"让AI重新生成"
- `使用指南.md:254`  
  ### 3. 图片生成技巧
- `使用指南.md:308`  
  1. 使用"生成预览"模式
- `使用指南.md:310`  
  3. 让AI根据反馈重新生成
- `使用指南.md:313`  
  ### Q3: 图片生成失败？
- `使用指南.md:342`  
  - 新用户免费：500万Tokens
- `使用指南.md:344`  
  - **相当于每次生成成本 < ¥0.01**
- `使用指南.md:396`  
  输入你的第一个主题，让AI帮你生成小红书内容！
- `启动说明.md:5`  
  ### Windows用户：
- `启动说明.md:57`  
  ## Windows用户（如果python命令不工作）
- `启动说明.md:108`  
  1. **快速发布** - 输入主题，自动生成并发布
- `启动说明.md:109`  
  2. **生成预览** - 生成内容后手动确认再发布
- `启动说明.md:122`  
  - **免费额度**: 500万Tokens（新用户）
- `微信公众号使用指南.md:7`  
  - 自动写作：生成高质量公众号文章
- `微信公众号使用指南.md:8`  
  - 图片生成：为文章生成配图（可选）
- `微信公众号使用指南.md:24`  
  - 点击"重置"或"生成"获取 AppSecret
- `微信公众号使用指南.md:50`  
  1. **快速发布** - 输入主题，自动生成并发布
- `微信公众号使用指南.md:51`  
  2. **生成预览** - 生成文章后手动确认再发布
- `微信公众号使用指南.md:63`  
  适合快速生成并发布文章的场景：
- `微信公众号使用指南.md:70`  
  - （可选）生成配图
- `微信公众号使用指南.md:75`  
  ### 2. 生成预览模式
- `微信公众号使用指南.md:81`  
  3. 系统生成文章并显示预览
- `微信公众号使用指南.md:121`  
  - 图片生成引擎
- `微信公众号使用指南.md:143`  
  - 生成摘要
- `微信公众号使用指南.md:148`  
  - 生成图片提示词
- `微信公众号使用指南.md:149`  
  - 调用图片生成API
- `微信公众号使用指南.md:150`  
  - 保存生成的图片
- `微信公众号使用指南.md:165`  
  ### 内容生成特点
- `微信公众号使用指南.md:192`  
  - **月之暗面**：适合中文生成
- `微信公众号使用指南.md:207`  
  ### 图片生成配置
- `微信公众号使用指南.md:210`  
  # 图片生成引擎
- `微信公众号使用指南.md:217`  
  **注意**：图片生成是可选的，未配置时系统会跳过图片生成步骤。
- `微信公众号使用指南.md:241`  
  ### Q4: 生成的文章质量不理想
- `微信公众号使用指南.md:246`  
  3. 生成预览模式：先预览再决定是否发布
- `微信公众号使用指南.md:253`  
  - 或者在生成预览模式下，可以取消发布，然后修改主题重新生成
- `微信公众号使用指南.md:292`  
  - `generated_images/` - 生成的图片
- `微信公众号使用指南.md:314`  
  ### 自定义文章模板
- `微信公众号使用指南.md:316`  
  可以修改 `agents/wechat_writer.py` 来调整文章生成逻辑：
- `微信公众号使用指南.md:323`  
  # 在 _generate_content 方法中修改 prompt
- `微信公众号使用指南.md:330`  
  1. 先生成文章并保存为草稿
- `微信公众号使用指南.md:341`  
  - ✅ 支持微信公众号文章生成
- `微信公众号使用指南.md:342`  
  - ✅ 支持图片生成（可选）
- `问题解决方案.md:65`  
  ### 🥉 方案3：使用Anaconda（适合有经验的用户）
- `问题解决方案.md:72`  
  4. 安装完成后，打开 "Anaconda Prompt"（从开始菜单）
- `问题解决方案.md:74`  
  **启动系统（在Anaconda Prompt中）：**
- `web\README.md:9`  
  ✅ **快速发布** - 输入主题，一键生成并发布文章
- `web\README.md:10`  
  ✅ **生成预览** - 先生成内容预览，确认后再发布
- `web\README.md:29`  
  **Windows用户：**
- `web\README.md:52`  
  2. 选择是否生成配图（默认不生成）
- `web\README.md:60`  
  ### 生成预览
- `web\README.md:63`  
  2. 点击"生成内容"按钮
- `web\README.md:66`  
  5. 或点击"重新生成"重新创作
- `web\README.md:99`  
  **图片生成配置：**
- `web\README.md:100`  
  - 选择图片生成引擎
- `web\README.md:101`  
  - 默认为"不生成图片"
- `web\README.md:116`  
  - `POST /api/generate_preview` - 生成预览
- `web\README.md:134`  
  用户输入主题
- `web\README.md:240`  
  1. **用户认证**
- `web\README.md:242`  
  - 支持多用户管理
- `web\README.md:248`  
  3. **模板管理**
- `web\README.md:249`  
  - 保存常用的文章模板
- `web\README.md:250`  
  - 快速套用模板

## 使用建议
- 可将上述条目转为可调用模板，按目的快速检索
- 结合 `project-analyzer` 输出的功能点直接生成对应提示词