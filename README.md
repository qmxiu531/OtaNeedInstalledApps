### 自动下载三方App并安装
### How To Use

1. 程序会自动读取当前.exe文件下的xlxs文件,然后提示用户输入xlxs文件里面的项目名称

2. 程序读取对应项目的App名称，然后根据汇总的三方应用sheet里面的APP的包名去应用宝上搜索对应的App

3. 搜索到对应的APP后，进行解析下载地址

4. 下载对应的App到本地


### 2018.05.24号增加的功能
1. 增加多进程多台手机执行

2. 增加手机掉线后等待的处理

3. 增加软件商店下载失败后，会尝试去应用宝下载

4. 增加遍历的截图和log记录

root
    -- android-common-util 　兼容之前的应用，以后不更新
    -- app　                 用于测试common库
    -- common-analysis　     测试报告分析公共库
    -- common-func          测试功能公共库
    -- common-report　　　　　　测试报告公共库

</pre>

**注意点**

本程序还会集成一个遍历所有应用的Apk，在测试遍历之前请确认该Apk是否自动安装成功

```sh
# groupId value
COMMON_GROUP=com.gionee.autotest

# version value , if version contain snapshot, then publish it to SNAPSHOT_REPOSITORY_URL;or,RELEASE_REPOSITORY_URL
COMMON_VERSION_NAME=1.0.0
# or COMMON_VERSION_NAME=1.0.0-SNAPSHOT

# artifactId value
COMMON_ARTIFACT_ID=common-func
```

### License

     Copyright 2018 Gionee, Inc.

     Copyright 2018 Suse Qi <qimx@gionee.com>

     Licensed under the Apache License, Version 2.0 (the "License");
     you may not use this file except in compliance with the License.
     You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

     Unless required by applicable law or agreed to in writing, software
     distributed under the License is distributed on an "AS IS" BASIS,
     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
     See the License for the specific language governing permissions and
     limitations under the License.