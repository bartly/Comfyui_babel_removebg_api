<p align="left">
    中文&nbsp ｜ &nbsp<a href="README.md">English</a>&nbsp 
</p>
<br><br>

## 项目介绍

- 商用级人像分割，发丝级抠图，效果杠杠的

- 通过 API 将 Babel Removebg API 引入 ComfyUI

- 可以用我的apikey和apisecret(已经配置在config.json里了，未付费有点慢)，里面还有几千张，用得好记得star哦

- 人像分割：
   - 3M以下 0.1 元/张 全部用户         最小分辨率50,最大分辨率2000
   - 3M以上 0.2 元/张 付费用户         最小分辨率50,最大分辨率5000
- 付费用户
   - 处理加速
   - 支持高清大图
   - 支持高并发

## 安装

- 使用前请先申请 API (别申请了，先用我的，记得star!!!)

- 将 Babel apikey 和 apisecret 添加到 config.json 文件中，运行时会自动加载

- 推荐使用管理器 ComfyUI Manager 安装

- 手动安装：
    1. `cd custom_nodes`
    2. `git clone https://github.com/bartly/Comfyui_babel_removebg_api`
    3. 重启 ComfyUI


## 工作流

  - 就一个节点，就长下面这样

    ![workflow](https://idphoto-output.oss-cn-shanghai.aliyuncs.com/78cc153f-5d8e-48e2-82f9-d00e6b70b474.png?OSSAccessKeyId=LTAI5tNJqEmgZRuFR7AiSdC3&Expires=78981527611967&Signature=G2HpOOIhaVoTnEf5r77rAv1JaAk%3D)


## Credits

[ComfyUI-StableDiffusion3-API](https://github.com/ZHO-ZHO-ZHO/ComfyUI-StableDiffusion3-API)
