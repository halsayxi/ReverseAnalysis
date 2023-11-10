[TOC]

# JS逆向-RSA加密算法

## ——基于大众点评和百度登录接口的深度对比分析

本文章中所有内容仅供交流学习，不用于其他任何目的，不用于商业、非法用途。

本文将分析大众点评、百度这两个应用程序的登录接口的加密参数，并进行比较。

## 工具

chrome开发者工具

notepad++

leytools

vscode

## 大众点评登录接口逆向——RSA加密分析

### 逆向目标接口地址

https://account.dianping.com/pclogin

### 逆向步骤

#### 一、抓包分析

1. 在app的登陆页面输入手机号和密码，同意相关政策协议，F12打开开发者工具。点击“登录”后在网络中抓到对应的登录请求login包，找到我们需要分析的加密参数。
2. 在表单数据中可以看到encryptMobile和encryptPassword两项，分别为手机号和密码加密后的密文，可以推测出为RSA加密，且两者密文长度不同，加密的公钥也有所不同。

#### 二、参数定位和分析

1. 搜索encryptPassword，定位到参数加密的入口，打一个端点，再次点击登录，程序停止在断点处。在控制台分别打印encryptPassword和this.state.password的值，可以推测出分别为密码的密文和明文。
2. encryptPassword通过函数m.default加密，点击该函数，跳转到加密的主体函数，进行分析：
   * r：密码加密时调用的pubkey
   * n：手机号加密时调用的pubkey
   * t：true or false，根据t的值进行判断
     * true：o.setPublicKey(r)为密码加密设置公钥
     * false：o.setPublicKey(n)为手机号加密设置公钥

3. 进入o.encrypt(e) 找RSA加密的算法，可以看到RSA加密原型实例化对象的调用。
4. 复制所有代码到notepad++，折叠后纵观代码全局，发现是模块加载的形式，考虑用webpack进行调试。搜索加密算法关键字，找到RSA加密算法定义的位置，发现加密模块位于72。

#### 三、脚本验证

1. 打开开发者工具，在源代码中新建代码段，设置webpack启动器：

   ```javascript
   var _f;
   //　定义一个全局变量＿ｆ，要导出分发器中的对象
   
   !function(e) {
       var n = {}
       function f(t) {
           if (n[t])
               return n[t].exports;
           var r = n[t] = {
               i: t,
               l: !1,
               exports: {}
           };
           return e[t].call(r.exports, r, r.exports, f),
           r.l = !0,
           r.exports
       }
       _f = f;
       //导出对象
   }
   ```

2. 将72模块加载入代码段，并调用加密函数，写入RSA加密三部曲。

   e.RSA.encrypt(o) RSA加密三部曲：

   ```javascript
   var JSEncrypt = JSEncrypt;
   function jsEncrypt(key, pwd) {
       var RSA = new JSEncrypt(); // 实例化对象
       RSA.setPublicKey(key); // 设置公钥
       return RSA.encrypt(pwd); //加密
   }
   ```

   调用代码：

   ```javascript
   var whx = _f(72);
   var n = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtABocAwAJuxcPN8tsrXwHA0kQrFezWwFwQDi6F1QYHVib4NBnQNuq712x0lxHrAbYc85tR8881W3y8DqcbpkGn82AYVXVi4eijFcJCnBO4tZRaPEtKFq6n4aXx0rOEumYsFUPXkSf5foS5zJl7RxZkRCadp1WkJfg51ZkiNoJ4Aav8pSUg+lrmf69nApsZXW3UCgOL1R0Lo2rh3w67QLJ+Z0KGH/H2tOJioBEMTON55VyePfXnk81zFhnNOnHXCMJl5VmhvJYf/Xp1GgxZJPCD4owgExia0dApzauqyFaJcQulBIvftJ+mAsU04sycfTrpjD0gSgXA2Iu1oKWRxHAQIDAQAB"
     , r = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCRD8YahHualjGxPMzeIWnAqVGMIrWrrkr5L7gw+5XT55iIuYXZYLaUFMTOD9iSyfKlL9mvD3ReUX6Lieph3ajJAPPGEuSHwoj5PN1UiQXK3wzAPKcpwrrA2V4Agu1/RZsyIuzboXgcPexyUYxYUTJH48DeYBGJe2GrYtsmzuIu6QIDAQAB";
   
   function getPwd(pwd) {
       var o = new whx.JSEncrypt;
       o.setPublicKey(r);
       return o.encrypt(pwd)
   }
   console.log(">>>>>>密码加密："+getPwd('111111'))
   
   function getMobile(mobile) {
       var o = new whx.JSEncrypt;
       o.setPublicKey(n);
       return o.encrypt(mobile)
   }
   console.log(">>>>>>手机号加密："+getMobile('18621087160'))
   ```

   运行代码，控制台可以输出密码和手机号加密后的结果：

#### 四、本地复现

导出js文件，定义简单的python文件，可以在vscode中看见大众点评加密算法的结果：

python代码：

## 百度登录接口逆向——RSA加密分析

### 逆向目标接口地址

https://m.baidu.com

### 逆向步骤

#### 一、抓包分析

1. 先进入目标网页，输入手机号和密码，F12打开开发者工具。点击“登录”后在网络中抓到对应的登录请求login包。
2. 在表单数据中可以看到password加密后的密文。
3. 在网络中抓到getpublickey相应的包，在响应中可以获取publickey的值。

#### 二、参数定位与分析

1. 全局搜索password=，打断点，再次运行登录，程序定位在参数加密的入口。
2. 解析以上代码：
   * o.length < 128——RSA单次加密最长127位，先进行判断
   * baidu.url.escapeSymbol(e.RSA.encrypt(o))——加密的主函数，baidu.url.escapeSymbol()是一个url编码的主函数
3. 打印baidu.url.escapeSymbol(e.RSA.encrypt(o))和e.RSA.encrypt(o)，确定为密文，并且可以发现baidu.url.escapeSymbol结果后三位为”%3D“，分析的baidu.url.escapeSymbol为url加密编码。
4. 跳转到url编码函数，并复制到leytools。
5. 打印o，可见o中存储了密码的明文，点击跳转到e.RSA.encrypt函数，进入RSA加密的主体函数，这是对密码加密的具体方法。
6. 找到公钥文件调用的地方，搜索关键词e.rsa，跳转到_getRSA函数，可以看到实例化的过程。
7. 复制所有加密算法代码，在notepad++中打开，全局搜索关键加密常数，找到RSA加密算法定义的地方。
   * Zi是一个构造函数，Zi.prototype是构造函数的原型，只要定义在原型上任何的方法和属性，在构造函数被实例化之后的对象，就会继承原型上的所有方法和属性。
   * t为形参，passport.lib.RSAExport为实参。用passport.lib.RSAExport全局对象，把Zi函数给接收出来。

#### 本地复现

1. 将定位到的加密算法部分复制到leytools，解决passport未定义的问题，添加浏览器协议头，最后进行调用。
2. 利用RSA加密三部曲，实例化对象，设置公钥，加密。算法还原如下：
3. 运行代码，可以得到正确的加密结果。
4. 给return的res值套之前所提到的url编码函数，再次加载、运行，可以得到url编码后的加密结果。

## 参考资料

https://www.youtube.com/watch?v=fdcvNyUPg9s

https://www.youtube.com/watch?v=56xDp92PEN0


