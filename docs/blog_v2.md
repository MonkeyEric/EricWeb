# 2021年12月1日需求，预计上线时间：2022年2月1日

#  项目需要做得事情
## 博客  
1. markdown编写，md形式显示，存储到数据库中等等，使用editormd的插件 finished 2021.12.8 
## 理财小能手 
1. 确定收支的分类【支持自定义】  finished 2022.1.6
2. 模仿layui添加一个刷新按钮，服务端缓存清楚按钮 【去掉，没有用，直接点击刷新按钮】
3. count_type_f 和count_type_s 可以进行下拉，并且可以进行联动  finished 2021.12
4. 搜索功能    finished 2021.12
5. 排序功能，不影响count_type_f的显示    finished 2021.12 
6. 即时修改功能   finished 2021.12
## 首页  
1. 设定隐藏左边的菜单栏   finished 2021.12.8
2. 跟自己的wiki做到统一，网站名字：Smelly Cat   finished 2021.12.8
3. 新增分类，标签，友链，系统公告。并且在分类、标签页面，鼠标悬浮，显示对应的个数     finished 2021.12.16
4. 修改为： 轮播图，个人名片，名言警句，文章列表，分类，标签，好友链接，系统公告等等。 finished 2021.1.4
5. 最近文章，包含文章下的标签，分类  finished 2021.12.16
6. 最近文章的 浏览 点赞功能
7. 快捷入口:收藏网站、个人wiki、理财小助手    finished 2021.1.4
8. 系统公告:自己线上更新版本的信息——目前设定为手动添加，写到一个文件中.  finished 2022.1.11
9. 友情链接：配置文件显示。   finished 2022.1.11
10. 滚动公告：如果有连续有N天没有编写博客或者日常总结，就给与提示  【去掉】
11. 个人名片的格式  finished 2021.12
12. 名言警句的添加，随机显示 finished 2021.12
13. 评论功能
## 登录
1. 整体网站的风格要简单，功能明确。用户登录以后，系统随机分配一个头像。【从百度批量下载的猫咪头像】，一种是在发表评论【走登录接口】的时候，一种是用户注册的时候。finished 2022.1.6
2. 需要加失败的提示语，是账号错误，还是密码错误。要加成功的提示语。 暂时去掉
3. 生产环境，注册一个账号后，将注册接口注销掉。利用配置文件来注销 利用env文件来配置 finished 2021.1.11
4. post和put的请求，都需要添加登录限制   finished 2021.1.11
    
## 收藏网站
1. 收藏网站添加：只有超级管理员可以添加 finished 2022.1.7
2. 页面布局样式已经做好，并且做成了自定义的类别，后台可修改配置  finished 2022.1.6 
3. 添加收藏网站，将分为两种: 1种是手动添加，另一种是，输入多个网址，爬取下来，存到数据库种，每次只能按照一种类别来进行添加
   


# js
1. blueimp jquery 视屏画廊插件blueimp Gallery
2. bootstrap-taginput  标签tag输入法
3. bootrapTour  用户引导插件
4. c3  可视化图表插件
5. chartist、chartjs 可视化插件
6. chosen 多选插件
7. clipboard  复制粘贴插件
8. clockpicker jquery时钟插件
9. codemirror  代码编辑器
10. cropper  cropperjs是一款非常强大却又简单的图片裁剪工具,
11. d3   数据可视化工具
12. datamaps  	excel地图可视化插件
13. datapicker  日期选择插件
14. dataTables	前端表格插件
15. daterangepicker	日期范围选择插件
16. diff_match_patch	写对比组件
17. dotdotdot	单行、多行文本溢出显示省略号插件
18. dropzone	一款JavaScript 文件拖拽上传插件,提供Ajax异步上传功能。
19. dualListbox	双向select选择框控件,作为对multiple select的扩展,使用起来非常简单,功能也更强大。
20. easypiechart	网页饼图组件
21. flot	利用js绘制图表
22. footable	表格响应式插件
23 fullcalendar	前端日历插件
24. gritter		一个小型的 jQuery 消息通知插件,通知效果如
25. i18next		多语言支持
26. iCheck		表单选择插件
27. idle-timer		时间插件
28. ionRangesSlider		进度条插件
29. jasny	输入框摸具
30. jeditable	单元格即时编辑插件
31. jqGrid	前端分页插件
32. jquery-ui  为基础的开源 JavaScript 网页用户界面代码库。包含底层用户交互、动画、特效和可更换主题的可视控件。
33. jsKnob   进度的插件
34. jsTree   动态树插件
35. justified-gallery 响应式画廊Gallery插件
36. jvectormap  jquery地图插件
37. ladda  按钮提交后多种加载动画效果
38. masonary    图片瀑布流插件
39. metisMenu	导航插件
40. netstable
41. nouslider	时间滑块
42. pace	pace.js是一款优秀的JavaScript插件,通过使用pace.js,我们可以制作出不同的网页进度条加载效果。
43. pdfjs   预览pdf
44. peity	数据可视化插件
45. preetyTextDiff	在线文本对比工具
46. pwstrength   用于twitter引导程序的jquery插件,为可视化显示输入密码的用户质量提供规则集。
47. rickshaw	可交互的时间序列图
48. select2    Select2是一款基于JQuery的下拉列表插件,
49. slick 	轮播插件
50. slimscroll   是一个小的(4.6KB)jQuery插件,它可以把任何的div转换成一个带有滚动条的可滚动区域,
51. sparkline  一类信息体积小和数据密度高的图表。就是小图表
52. steps	步骤条、时间轴
53. summernote   网页文本编辑器
54. sweetalert   美化alert窗口
55. switchery   仿照苹果IOS7的滑动按钮插件
56. tinycon		动态通知插件
57. toastr	是一个基于jQuery的非阻塞通知的JavaScript库。
58. topojson   基于html5的在线地图
59. touchpunch 移动端的触碰、长按、划屏
60. typehead  前端自动提示功能
61. validate 前端表单验证
62. video  前端播放插件
63. wow  实用滚动插件