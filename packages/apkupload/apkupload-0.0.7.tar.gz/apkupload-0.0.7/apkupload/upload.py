import configargparse
import argparse
import base64
import hashlib
import hmac
import json
import os
import requests
import time
import urllib.parse
from datetime import datetime
# 解析输入的参数

content_template = """

* 应用名称：{name}
* 下载地址：[戳这里]({download_url})
* 更新说明：
{changelog}
* MD5：{md5}
* 版本名称：{version_name}
* 版本号：{version_code}
* 包大小：{size}
* 历史版本：[戳这里]({url})
![图片]({image})
"""


def parse():
    p = configargparse.ArgParser(
        config_file_parser_class=configargparse.YAMLConfigFileParser)
    p.add('--config', required=True, is_config_file=True)
    p.add('--version_code', required=True)
    p.add('--version_name', required=True)
    p.add('--send', required=True)
    p.add('--name', required=True)
    p.add('--base', required=True)
    p.add('--input', required=True)
    p.add('--output', required=True)
    p.add('--key', required=True)
    p.add('--password', required=True)
    p.add('--url', required=True)
    p.add('--secret', required=True)
    p.add('--token', required=True)
    p.add('--apk_repository', required=True)
    p.add('--apk_branch', required=True)
    p.add('--user', required=True)
    p.add('--repository', required=True)
    p.add('--github', required=True)
    p.add('--workflow', required=True, )
    p.add('--channels', required=True, nargs="+", )
    p.add('--changelog', required=True, nargs="+")
    p.add('--at', required=True, nargs="+")
    p.add('--image', required=True)
    return p.parse_args()


def generate_apk_name(output, name, new_version_name):
    now = datetime.strftime(datetime.now(), "%m_%d_%H%M")
    return f"{output}/{name}_{new_version_name}_{now}.apk"


def build_web(md5, size, version_name,version_code, name, changelog, user, repository, workflow, apk_repository, apk_branch, apk, headers,base,path):
    print(">>>> build web <<<<")
    file = f"https://raw.githubusercontent.com/{user}/{apk_repository}/{apk_branch}/{apk}"
    content = {
        "version_name": version_name,
        "version_code": version_code,
        "url": file,
        "name": name,
        "date": datetime.now().strftime("%Y-%m-%d %H时%M分%S秒"),
        "changelog": changelog,
        "md5":md5,
        "size":size,
        "file":path,
        "base":base,
    }
    body = {"ref": "main", "inputs": {"content": json.dumps(content)}}
    r = requests.post(
        f"https://api.github.com/repos/{user}/{repository}/actions/workflows/{workflow}/dispatches",
        headers=headers,
        json=body
    )
    print(r.status_code)


def change_version(output, input, version_code, version_name):
    os.system('rm -rf ' + output)
    os.system('rm -rf ' + input + "/build")
    result = ""
    print(">>>> change version <<<<")
    with open(input + "/apktool.yml", 'r') as f:
        lines = f.readlines()
        for line in lines[:-2]:
            result += line
        result += "  versionCode: '{version_code}'\n".format(
            version_code=version_code)
        result += "  versionName: " + version_name
    with open(input + "/apktool.yml", "w") as f:
        f.write(result)


def build_apk(output, input, apk, key, password):
    unalign = output + "/unalign.apk"
    unsign = output + "/unsign.apk"
    print(">>>> building apk <<<<")
    os.system(
        'apktool b -o {unalign} {decode}'.format(unalign=unalign, decode=input))
    print(">>>> aligning apk <<<<")
    os.system(
        'zipalign -f 4 {unalign} {unsign}'.format(unalign=unalign, unsign=unsign))
    print(">>>> signing apk <<<<")
    os.system('apksigner sign --ks {key} --ks-pass pass:{password} --out {apk} {unsign}'.format(
        key=key, password=password, apk=apk, unsign=unsign))


def upload_to_github(md5, size, apk, user, apk_repository, headers, send, name, url, changelog, secret, token, at, version_name, version_code,image,download_url):
    print(">>>> start upload <<<<")
    content = ""
    with open(apk, "rb") as file:
        base64_bytes = base64.b64encode(file.read())
        content = base64_bytes.decode("ascii")
    body = {"message": "upload apk", "content": content}
    apk_name = apk.split("/")[-1]
    r = requests.put(
        f"https://api.github.com/repos/{user}/{apk_repository}/contents/{apk_name}",
        headers=headers,
        json=body,
    )
    if (r.status_code == 200 or r.status_code == 201):
        print(">>>> upload success <<<<")
    else:
        print(f">>>> upload failed 请手动上传<<<<")
    if send == 'True':
        send_to_dingding(md5, size, name, url, changelog, secret,
                             token, at, version_name, version_code,image,download_url)


def send_to_dingding(md5, size, name, url, changelog, secret, token, at, version_name, version_code,image,download_url):
    print(">>>> send to dingding <<<<")
    content = content_template.format(name=name, download_url=download_url, changelog=changelog,
                                      md5=md5, version_name=version_name, version_code=version_code, size=size,image=image,url=url)
    atMobiles = []
    for i in at:
        atMobiles.append(i)
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc,
                         digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    url2 = f'https://oapi.dingtalk.com/robot/send?access_token={token}&timestamp=' + \
        timestamp + '&sign=' + sign
    h = {'Content-Type': 'application/json; charset=utf-8'}
    body = {"at": {"isAtAll":True},
        "msgtype": "markdown", "markdown":{"text": content, "title": "更新日志"}
            }
    r = requests.post(url2, headers=h, data=json.dumps(body))
    print(r.text)

def main():
    args = parse()
    version_code = args.version_code
    version_name = args.version_name
    name = args.name
    base = args.base
    send = args.send
    channels = args.channels
    input = args.input
    output = args.output
    key = args.key
    password = args.password
    secret = args.secret
    url = args.url
    token = args.token
    changelog = args.changelog
    changelog = [f"> - {item}" for item in changelog]
    changelog = "\n".join(changelog)
    github = args.github
    workflow = args.workflow
    apk_branch = args.apk_branch
    at = args.at
    user = args.user
    repository = args.repository
    apk_repository = args.apk_repository
    image = args.image
    headers = {"Accept": "application/vnd.github.v3+json",
               "Authorization": f"token {github}"}
   
    for channel in channels:
        new_version_name = f"{version_name}_{channel}"
        path = datetime.now().strftime("%Y%m%d%H%M")
        new_url = url+"/"+name+"/"+ path
        apk = generate_apk_name(output, name, new_version_name)
        apk_name = apk.split("/")[-1]
        download_url = f"https://raw.githubusercontent.com/{user}/{apk_repository}/{apk_branch}/{apk_name}"
        md5 = ""
        size = ""
        build_web(md5, size, new_version_name,version_code, name, changelog, user,
                  repository, workflow, apk_repository, apk_branch, apk_name, headers,base,path)
        change_version(output, input, version_code, new_version_name)
        build_apk(output, input, apk, key, password)
        md5 = hashlib.md5(open(apk, 'rb').read()).hexdigest()
        size = str(os.path.getsize(apk))+"字节"
        build_web(md5, size, new_version_name,version_code, name, changelog, user,
                  repository, workflow, apk_repository, apk_branch, apk_name, headers,base,path)
        
        upload_to_github(md5, size, apk, user, apk_repository, headers, send,
                         name, new_url, changelog, secret, token, at, new_version_name, version_code,image,download_url)


if __name__ == "__main__":
    main()
