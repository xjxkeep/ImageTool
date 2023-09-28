# ImageTool
`论文` `对比实验` `可视化` `图像处理`

一个开源的论文图像排版工具,实现了图像批量重命名,尺寸统一,标注可视化,一键生成word图表等功能.

## 环境
开发环境 python 3.11
numpy==1.25.2
Pillow==10.0.0
PyQt6==6.5.2
python-docx==0.8.11
## 使用
* 下载可执行文件
  [ImageTool](https://github.com/xjxkeep/ImageTool/releases/tag/V1.0.1)
* 下载源码运行
  ```
  git clone git@github.com:xjxkeep/ImageTool.git
  cd ImageTool
  pip install -r requirements.txt

  python main.py
  ```

## 功能演示
展示了该项目的基本功能实现,更多功能请下载自行探索.
### 文件打开
![打开图片文件](https://github.com/xjxkeep/ImageTool/blob/main/images/%E6%96%87%E4%BB%B6%E6%89%93%E5%BC%80.gif)
### 图片排版
![图片排版](https://github.com/xjxkeep/ImageTool/blob/main/images/%E5%9B%BE%E5%83%8F%E6%8E%92%E7%89%88.gif)
### 图像标注
> 注: 红色标注框显示闪烁是gif生成的问题
> 
![图像标注](https://github.com/xjxkeep/ImageTool/blob/main/images/%E5%9B%BE%E5%83%8F%E6%A0%87%E6%B3%A8.gif)
### 设置统一尺寸
![图像标注](https://github.com/xjxkeep/ImageTool/blob/main/images/%E7%BB%9F%E4%B8%80%E5%B0%BA%E5%AF%B8.gif)
### 导出word表格
![导出word表格](https://github.com/xjxkeep/ImageTool/blob/main/images/word%E7%94%9F%E6%88%90.gif)
## 其他功能
上文展示了项目的基础使用,本项目还有许多其他的功能期待您的探索.
* 图像操作支持撤销,当操作生效后也可以通过"取消"按钮恢复原始图像.
* 支持选择标注框的边框尺寸与颜色
* 可以通过添加放大镜来局部放大某个部分,放大比例可调
* 支持图像按列优先与按行优先顺序切换
* 支持统一调整所有图像的尺寸,并导出所有图像.
* 批量重命名: 双击列表可以调整文件名,导出图像时会以列表中的名字为图像命名.
* 图像标注窗口可分离,对于大尺寸图形可以全屏进行标注.


> 如果在使用中有任何疑问可以通过邮箱联系我 (715020813@qq.com)
>
> 觉得本项目对您的科研有帮助的话, 别忘了帮忙点一颗⭐小星星⭐
