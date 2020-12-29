import json
import urllib3
import time

config = {}
lastData = {}
http = urllib3.PoolManager()

# 发送给机器人的内容结构
robotMsg = {"msgtype": "markdown", "markdown": {"content": ""}}
waitToMerge = 0

def loadConfig():
    global config
    configFile = open("./config.json", "r")
    config = eval(configFile.read())
    configFile.close()

def requestGerritJson(project):
    if "gerritUrls" not in config:
        return NULL
    if "changeDataUrl" not in config["gerritUrls"]:
        return NULL
    gerritLink = config["gerritUrls"]["changeDataUrl"] + project
    if len(gerritLink) is 0:
        return NULL
    r = http.request("GET", gerritLink, headers={})
    commitsJson = str(r.data[4:], 'utf-8')
    # print(commitsJson)

    waitToMerge = 0
    commits = json.loads(commitsJson)
    return commits

# 根据 commits 内容组装消息
def composeMsg(commits):
    global waitToMerge
    msg = ""
    for commit in commits:
        labels = commit["labels"]

        # 编译失败的不推送
        vf = labels["Verified"]
        if "rejected" in vf:
            continue

        # 根据配置决定是否显示未编译通过的
        if len(vf) is 0 and config["showNotVerified"] is 0:
            continue

        # 被 -1 的不推送
        cr = labels["Code-Review"]
        if "disliked" in cr and config["showDisliked"] is 0:
            continue

        if commit["owner"]["name"] == "gerrit":
            continue

        if config["enableWhiteList"] == 1 and commit["owner"]["username"] not in config["whiteList"]:
            continue
        
        waitToMerge += 1
        linkName = commit["subject"]
        if "display_name" in commit["owner"]:
            userName = commit["owner"]["display_name"];
        else:
            userName = commit["owner"]["name"]
        userName = userName.replace("(成都)", "").replace("（成都）", "");
        branch = commit["branch"]
        if "commitDetailUrl" in config["gerritUrls"]:
            commitLink = str(config["gerritUrls"]["commitDetailUrl"]) % commit["project"]
            link = commitLink + str(commit["_number"])
            print(link)
            msg += "> %s: `%s` [%s](%s) \n" % (userName, branch, linkName, link)
        else:
            msg += "> %s: 「%s」%s \n" % (userName, branch, linkName)
    return msg

def pushMsg(msg):
    global waitToMerge
    global lastData
    msg = "还有<font color=\"warning\"> %d条 </font>没合并，各位大佬帮帮呀!(#`O′)\n" % (waitToMerge) + msg + "\n\n" + config["customMsgs"]
    # print(msg)
    robotMsg["markdown"]["content"] = msg
    data = json.dumps(robotMsg).encode("utf-8")
    if sorted(data) != sorted(lastData):
        result = http.request("POST", config["wechatHook"], body=data, headers={"Content-Type": "application/json"})
        print(result.data)
        lastData = data

def startProcess():
    while 1:
        loadConfig()
        global waitToMerge
        waitToMerge = 0
        if "watchingProject" not in config:
            time.sleep(300)
            continue

        msg = ""
        for project in config["watchingProject"]:
            commits = requestGerritJson(project)
            msg += composeMsg(commits)
        if msg != "":
            pushMsg(msg)
        time.sleep(300) 

startProcess()