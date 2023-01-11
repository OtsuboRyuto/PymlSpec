# PymlSpec
Yamlをベースに構成管理を誰でも簡単に実施できるツールです。

実行例
```
localhost:
  backend: "local://"
  tests:
  - "check google connection" :
      module: addr 
      args: google.com
      content: is_reachable
  - "check nginx service" :
      module: service
      args: nginx
      content: is_running
  - "mount point exists" :
      module: mount_point
      args: "/"
      content: exists
  - "mount point exists" :
      module: mount_point
      args: "/"
      content: filesystem
      expect: "ext"
 ```
 
 
   実行結果
```
=====================  test information  =====================
platform Linux version #1 SMP Wed Nov 23 01:01:46 UTC 2022
Python version 3.10.6
scheduled tests 4


========================  start test  ========================
=================  check google connection  =================


Success
Coverage 1/4
Test proceed in 0.03s
===================  check nginx service  ===================


Error
Expect value True, but actually False
Coverage 1/4
Test proceed in 0.06s
====================  mount point exists  ====================


Success
Coverage 2/4
Test proceed in 0.003s
====================  mount point exists  ====================


Error
Expect value ext, but actually ext4
Coverage 2/4
Test proceed in 0.003s
====================  Test Ended in 0.1s  ====================
                                           OK=2, NG=2, Total=4
```

テスト内容については以下参照\n
https://testinfra.readthedocs.io/en/latest/modules.html
