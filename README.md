# geetest-crack-demo

<img src="https://img.shields.io/badge/Python-3.6+-green.svg" alt="limit">
<img src="https://img.shields.io/github/languages/code-size/tomhaoye/geetest-crack-demo" alt="size">
<img src="https://img.shields.io/github/last-commit/tomhaoye/geetest-crack-demo" alt="update">


### 极验验证码滑动行为模拟demo
>经过一番折腾成功率已经比较高了（70%-90%吧【2018/10/01】），某些背景干扰元素过多缺口又刚好在色差较小的地方的时候可能会计算错误，也可能还有某些特殊的情况，GIF是旧的，具体可看MP4。
代码仅供参考学习交流，有兴趣可以拿去玩玩，鉴于本人能力有限，代码、逻辑以及解决方式上有错误在所难免，请各位大佬多多指教~
另外我发现极验官网快改版了，鉴于该代码直接在极验官网上模拟，可能很快就用不了了，届时可以考虑接入api到自己本地再进行模拟测试。

### 软件要求
- Anaconda(可选)
- python 3.6+
- selenium
- chromedriver(有需要则改运行路径)
- PIL

### 目录结构

- app
    - nocaptcha.py  `完整模拟、单一图片处理定位`
    - getdiffbin.py `原图与缺口图对比处理方法`
- gif
    - *.gif `效果展示`
- pic   `nocaptcha.py 运行结果`
- src   `getdiffbin.py 运行结果`
    - 1~10.jpg/bmp  `每两张为一组原图[1,2],[3,4],……`
    - 其他.jpg/bmp   `运行结果`

### 理想效果

![效果](gif/ezgif-3-1c61b3c10b.gif)