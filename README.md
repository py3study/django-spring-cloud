# 说明
使用6个django项目，来模拟java spring cloud架构，采用单入口模式调用api

`不涉及ribbon，hystrix，feign等功能，仅仅做演示而已，不是真正意义上的spring cloud。`

# 项目说明
| 项目名  | 说明 | 运行端口|部署顺序 |
| --- | --- | --- | --- |
| eureka  | eureka 微服务  | 8001 | 1 |
| config  | config 微服务  | 8002 | 2 |
| auth  | auth 微服务  | 8003 | 3 |
| user  | user 微服务  | 8004 | 4 |
| gateway  | gateway 微服务  | 8000 | 5 |
| demo_login  | 前端登录页面  | 8080 | 6 |

- 前端登录页面，采用bootstrap开发。使用ajax发送请求给api
- 后端微服务，采用rest framework实现，版本为3.11.0。
- 使用cors组件解决跨域问题

# 1.0
## 环境说明
| 操作系统  | 配置 | ip | 软件 |
| --- | --- | --- |--- |
| centos 7.6  | 2核4g  | 192.168.31.229 | pyton3.5.2,nginx1.16.1 |

## MySQL
由于本项目中，数据存储采用的是mysql，为了快速演示，直接使用docker启动mysql
```bash
docker run -d --restart=always --name example -e MYSQL_ROOT_PASSWORD=abcd@1234  -p 3306:3306 -v /data/mysql_3306/data:/var/lib/mysql mysql:5.7 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
```

### 初始化数据
```bash
# docker exec -it example /bin/bash
# mysql -u root -pabcd@1234
mysql> CREATE DATABASE usercenter DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
mysql> CREATE TABLE `users` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `username` varchar(16) DEFAULT NULL COMMENT '用户名',
  `password` varchar(32) DEFAULT NULL COMMENT '密码',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `last_time` datetime DEFAULT NULL COMMENT '最后一次登录时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户表';
mysql> INSERT INTO `usercenter`.`users` (`id`, `username`, `password`, `create_time`, `last_time`) VALUES ('1', 'xiao', '81dc9bdb52d04dc20036dbd8313ed055', '2020-02-05 11:55:27', '2020-02-05 11:55:30');
mysql> exit;
# exit
```

## url转发
请求方式| 来源  | 目标 | 说明 |
| ---| --- | --- | --- |
| POST | http://api.baidu.com/  | 127.0.0.1:8000  | gateway 微服务,网关统一入口 |
| POST | http://api.baidu.com/eureka  | 127.0.0.1:8001/server  | eureka 注册中心,各个微服务信息 |
| POST | http://api.baidu.com/config  | 127.0.0.1:8002/api/info/  | config 微服务 |
| POST | http://api.baidu.com/api-auth/login  | 127.0.0.1:8003/login/  | auth 微服务 |
| POST | http://api.baidu.com/api-user/info  | 127.0.0.1:8004/info/  | user 微服务 |
| GET | http://h5.baidu.com/  | 127.0.0.1:8080  | 前端登录页面 |

## 运行项目
### eureka
```bash
cd django-spring-cloud/1.0/eureka
pip3 install -r requirements.txt
python3 manage.py runserver 0.0.0.0:8001
```

### config
```bash
cd django-spring-cloud/1.0/config
pip3 install -r requirements.txt
python3 manage.py runserver 0.0.0.0:8002
```

### auth
```bash
cd django-spring-cloud/1.0/auth
pip3 install -r requirements.txt
python3 manage.py runserver 0.0.0.0:8003
```

### user
```bash
cd django-spring-cloud/1.0/user
pip3 install -r requirements.txt
python3 manage.py runserver 0.0.0.0:8004
```

### gateway
```bash
cd django-spring-cloud/1.0/gateway
pip3 install -r requirements.txt
python3 manage.py runserver 0.0.0.0:8000
```

### 前端
```bash
cd django-spring-cloud/1.0/demo_login
pip3 install -r requirements.txt
python3 manage.py runserver 0.0.0.0:8080
```

## 配置nginx
将nginx_conf放入`/etc/nginx/conf.d`目录，并启动nginx
```bash
yum install -y nginx
cp django-login-example/1.0/nginx_conf/* /etc/nginx/conf.d
# 启动nginx
nginx
```

## 配置域名解析
如果没有dns，请修改windows 10的hosts文件，添加2条记录
```bash
192.168.31.229 h5.baidu.com
192.168.31.229 api.baidu.com
```

## 访问页面
```bash
http://h5.baidu.com
```
登录信息
```bash
用户名：xiao
密码：1234
```

# 2.0
## 环境说明
| 操作系统  | 配置 | ip | 主机名 |软件 |
| --- | --- | --- |--- |--- |
| centos 7.6 | 2核4g | 192.168.31.150 | k8s-master | Kubernetes 1.16.3,docker 19.03.5 |
| centos 7.6 | 2核4g | 192.168.31.178 | k8s-node01 | Kubernetes 1.16.3,docker 19.03.5 |
| centos 7.6 | 2核4g | 192.168.31.37 | harbor | docker 19.03.5,docker-compose 1.24.1,harbor 1.8.0 |
| centos 7.6 | 2核4g | 192.168.31.229 | mysql | docker 19.03.5 |

## MySQL
继续使用1.0版本中的mysql

## url转发
请求方式| 来源  | 目标 | 说明 |
| ---| --- | --- | --- |
| POST | http://api.baidu.com/  | svc-gateway.default.svc.cluster.local:8000  | gateway 微服务,网关统一入口 |
| POST | http://api.baidu.com/eureka  | svc-eureka.default.svc.cluster.local:8001/server  | eureka 注册中心,各个微服务信息 |
| POST | http://api.baidu.com/config  | svc-config.default.svc.cluster.local:8002/api/info/  | config 微服务 |
| POST | http://api.baidu.com/api-auth/login  | svc-auth.default.svc.cluster.local:8003/login/  | auth 微服务 |
| POST | http://api.baidu.com/api-user/info  | svc-user.default.svc.cluster.local:8004/info/  | user 微服务 |
| GET | http://h5.baidu.com/  | svc-login.default.svc.cluster.local:8080  | 前端登录页面 |
#### 说明
以svc-gateway.default.svc.cluster.local为例：

`svc-gateway` 表示service名

`default` 表示命名空间

`svc.cluster.local` 表示service的cluster ip

## 封装镜像
### django基础镜像
```bash
cd django-spring-cloud/2.0/django_base
docker build -t django:2.2.4 .
```

### eureka
```bash
cd django-spring-cloud/2.0/eureka
docker build -t eureka:v1 .
```

### config
```bash
cd django-spring-cloud/2.0/config
docker build -t config:v1 .
```

## auth
```bash
cd django-spring-cloud/2.0/auth
docker build -t auth:v1 .
```

## user
```bash
cd django-spring-cloud/2.0/user
docker build -t user:v1 .
```

## gateway
```bash
cd django-spring-cloud/2.0/gateway
docker build -t gateway:v1 .
```

### 前端
```bash
cd django-spring-cloud/2.0/demo_login
docker build -t demo_login:v1 .
```

## 推送镜像
```bash
docker login 192.168.31.37 -u admin -p Harbor12345

docker tag eureka:v1 192.168.31.37/library/eureka:v1
docker push 192.168.31.37/library/eureka:v1

docker tag config:v1 192.168.31.37/library/config:v1
docker push 192.168.31.37/library/config:v1

docker tag auth:v1 192.168.31.37/library/auth:v1
docker push 192.168.31.37/library/auth:v1

docker tag user:v1 192.168.31.37/library/user:v1
docker push 192.168.31.37/library/user:v1

docker tag gateway:v1 192.168.31.37/library/gateway:v1
docker push 192.168.31.37/library/gateway:v1

docker tag demo_login:v1 192.168.31.37/library/demo_login:v1
docker push 192.168.31.37/library/demo_login:v1
```

## k8s发布应用
### 安装ingress
```bash
kubectl apply -f https://kuboard.cn/install-script/v1.17.x/nginx-ingress.yaml
```

### eureka
```bash
cd django-spring-cloud/2.0/eureka/
kubectl apply -f eureka.yaml
kubectl apply -f eureka-ingress.yaml 
```
`注意：请修改yaml文件中的仓库地址，改为实际环境中的harbor`

### config
```bash
cd django-spring-cloud/2.0/config/
kubectl apply -f config.yaml
```
`注意：请修改yaml文件中的仓库地址，改为实际环境中的harbor`

### auth
```bash
cd django-spring-cloud/2.0/auth/
kubectl apply -f auth.yaml
kubectl apply -f auth-ingress.yaml 
```
`注意：请修改yaml文件中的仓库地址，改为实际环境中的harbor`

### user
```bash
cd django-spring-cloud/2.0/user/
kubectl apply -f user.yaml
kubectl apply -f user-ingress.yaml 
```
`注意：请修改yaml文件中的仓库地址，改为实际环境中的harbor`

### gateway
```bash
cd django-spring-cloud/2.0/gateway/
kubectl apply -f gateway.yaml
kubectl apply -f gateway-ingress.yaml 
```
`注意：请修改yaml文件中的仓库地址，改为实际环境中的harbor`

### 前端
```bash
cd django-spring-cloud/2.0/demo_login
kubectl apply -f login.yaml
kubectl apply -f login-ingress.yaml 
```
`注意：请修改yaml文件中的仓库地址，改为实际环境中的harbor`

### 查看pods
```bash
# kubectl get pods -o wide
NAME                           READY   STATUS    RESTARTS   AGE   IP              NODE         NOMINATED NODE   READINESS GATES
svc-auth-69b784b446-qvz27      1/1     Running   0          48m   10.244.85.205   k8s-node01   <none>           <none>
svc-config-9cbd44858-m5z7p     1/1     Running   0          53m   10.244.85.204   k8s-node01   <none>           <none>
svc-eureka-55d485749-mpqhw     1/1     Running   0          41m   10.244.85.207   k8s-node01   <none>           <none>
svc-gateway-645755cb8d-nkfp7   1/1     Running   0          68m   10.244.85.203   k8s-node01   <none>           <none>
svc-login-66c8d579b5-xg6l6     1/1     Running   0          23m   10.244.85.210   k8s-node01   <none>           <none>
svc-user-5c8799c845-jxlr4      1/1     Running   0          25m   10.244.85.209   k8s-node01   <none>           <none>
```
确保处于`Running`状态

### 查看ingress
```bash
# kubectl get ingresses.extensions
NAME          HOSTS              ADDRESS   PORTS   AGE
svc-auth      auth.baidu.com               80      31m
svc-eureka    eureka.baidu.com             80      22m
svc-gateway   api.baidu.com                80      100m
svc-login     h5.baidu.com                 80      96m
svc-user      user.baidu.com               80      28m
```

## 访问页面
在1.0中，使用了nginx转发。在2.0就无需nginx转发了，直接使用ingress转发。
### 域名解析
将域名解析到任意node节点的ip即可。
```bash
192.168.31.178 h5.baidu.com
192.168.31.178 api.baidu.com
192.168.31.178 auth.baidu.com
192.168.31.178 user.baidu.com
192.168.31.178 eureka.baidu.com
```

```bash
http://h5.baidu.com
```
登录信息
```bash
用户名：xiao
密码：1234
```

# 详细操作
关于1.0，请查看链接：

https://www.cnblogs.com/xiao987334176/p/12260474.html
<br/>
<br/>
2.0请参考链接：

https://www.cnblogs.com/xiao987334176/p/12264159.html

<br/>
<br/>
Copyright (c) 2020-present, xiao You