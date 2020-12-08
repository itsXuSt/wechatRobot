# wechatRobot
## 功能
1. 监控 gerrit 提交；
2. 配置监控项目；
3. 启用、配置用户白名单，只监听白名单内用户；
4. 部分信息过滤，可配置是否显示未编译的项、是否显示被 -1 的项；

## Todo
1. 免打扰时段设置；

## 配置方式

1. 修改 config_template.json 为 config.json;
2. 配置字段
   1. wechatHook: 微信机器人的 hook 链接；
   2. customMsgs: 可自定义的消息内容；
   3. showNotVerified: 显示未编译通过的提交；
   4. showDisliked: 显示被其他人 -1 的提交；
   5. enableWhiteList: 启用白名单，启用后，仅白名单内用户的提交被推送
   6. whiteList: 白名单列表；
   7. donBotherMe: 免打扰时段（TODO）；
   8. gerritUrls.changeDataUrl: 获取所有未关闭提交 json 数据的 url；
   9. gerritUrls.commitDetailUrl: 具体提交的链接前缀，当不配置时，不在推送消息中以超链接显示提交；
   10. watchingProject: 要监视的项目名称；