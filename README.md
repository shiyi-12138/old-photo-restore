# 老照片修复（Bringing Old Photos Back to Life）

基于微软研究院 CVPR 2020 口头报告论文的 SOTA 老照片修复模型，通过三阶段 AI 流程对褪色、破损的老照片进行全方位修复。

## 功能

本模型提供以下三项修复能力，可独立使用或组合使用：

- **划痕修复**：自动检测并去除老照片上的划痕、折痕、污渍等物理损伤
- **全局质量增强**：修复褪色、模糊问题，恢复照片的对比度和清晰度
- **人脸增强**：对照片中人脸区域进行单独优化，修复模糊五官，提升面部细节

## 技术原理

本项目实现了以下 CVPR 2020 论文中的完整工作流：

1. **变分自编码器（VAE）潜在空间映射**：通过三域转换网络，将有瑕疵的老照片映射到干净图像域
2. **部分非局部块（Partial Non-local Block）**：针对划痕区域的结构化修复
3. **渐进式人脸增强**：基于 SPADE 的生成式人脸修复，支持 256×256 和 512×512 两种分辨率

## 使用方式

### 输入

上传一张需要修复的老照片（支持 JPG、PNG 格式）：

- `image`：待修复的老照片

### 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `with_scratch` | bool | false | 是否修复划痕（有划痕的旧照片建议开启） |
| `HR` | bool | false | 是否开启高分辨率模式（照片分辨率较高时建议开启） |

### 输出

修复后的照片，划痕被去除，色彩恢复，人脸细节增强。

## 关于原始项目

**Bringing Old Photos Back to Life** 是微软研究院在 CVPR 2020 发表的学术成果，发表后在全球范围内被广泛应用于老照片数字化修复。本项目将其封装为易于调用的云端 API。

## 许可

本项目基于 MIT 许可协议开源。通过 Replicate API 调用可用于商业用途。

## 引用

```
@inproceedings{wan2020bringing,
  title={Bringing Old Photos Back to Life},
  author={Wan, Ziyu and Zhang, Bo and Chen, Dongdong and Zhang, Pan and Chen, Dong and Liao, Jing and Wen, Fang},
  booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition},
  year={2020}
}
```
