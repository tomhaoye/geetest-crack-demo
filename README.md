# geetest-crack-demo
极验验证码滑动行为模拟demo

>经过一番折腾成功率已经较高，暂未处理滑块左边突出的情况

### 软件要求
- Anaconda(可选)
- python 3.6+
- selenium
- chromedriver(有需要则改运行路径)
- PIL
- opencv(还没用上)

### 目录结构

- app
    - nocaptcha.py  `完整模拟、单一图片处理定位`
    - getdiffbin.py `原图与缺口图对比处理方法思路`
- gif
    - *.gif `缺口与图片对比度大及图片干扰元素较少的理想结果`
- pic   `nocaptcha.py 运行结果`
- src   `getdiffbin.py 运行结果`
    - 1~10.jpg/bmp  `每两张为一组原图[1,2],[3,4],……`
    - 其他.jpg/bmp   `运行结果`

### 理想效果

![效果](gif/ezgif-3-1c61b3c10b.gif)