# pytest-flexreport

### 1、介绍
pytest-flexreport是针对pytest的生成html报告的插件，自动收集用例执行的详细日志信息，以及相关错误和输出信息。使用起来非常简单，安装好pytest-testreport之后，运行用例时加上参数即可生成报告   

### 2、安装

pytest-testreport是基于python3.6开发的，安装前请确认你的python版本>3.6

安装命令

```pip install pytest-flexreport```

### 3、快速开始

###### 注意：如果安装了pytest-html这个插件，请先卸载，不然可能会有冲突

##### 使用案例：

- ###### 命令行执行： pytest 运行测试时加上参数--report 指定报告文件名

    ```shell
    # 指定报告文件名
    pytest --report=musen.html
    
    #其他配置参数
    --report=html报告文件路径
    --history_dir=history.json的目录路径，默认使用html文件同级目录
    --title=指定报告标题
    --tester=指定报告中的测试者
    --desc = 指定报告中的项目描述
    
    # 同时使用多个参数
    pytest --report=report.html --history_dir=./reports --title=测试报告 --tester=测试A --desc=项目描述
    ```
    
- ###### pytest.main执行

    ```shell
    import pytest
    
    pytest.main(['--report=musen.html',
                 '--history_dir=./reports',
                 '--title=测试报告标题',
                 '--tester=木森',
                 '--desc=报告描述信息'])
    ```



