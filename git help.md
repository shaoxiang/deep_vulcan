检查远程仓库列表：
首先，运行 git remote -v 来查看你当前仓库中配置的远程仓库列表。这将列出所有远程仓库的名称和它们对应的 URL。
git remote -v

添加上游仓库：
git remote add upstream https://github.com/isaac-sim/IsaacLab.git

添加原始仓库为上游（Upstream）
为了让你的 fork 能够跟踪原始仓库的变化，你需要将原始仓库设置为你的 fork 的上游仓库。这可以通过 Git 的 remote 命令完成：
git remote add upstream https://github.com/original-owner/original-repository.git

从上游仓库获取最新更改
为了将原始仓库的最新更改拉取到你的本地仓库，你可以首先切换到你的主分支（通常是 main 或 master）：
git checkout main
然后，从上游仓库的相同分支拉取更改：
git fetch upstream  
git merge upstream/main
这两个命令简写是：
git pull upstream main
推送更改到你的 Fork 仓库：
git push origin main

---

git add .
git reset HEAD source/third_part/*
git commit -m "添加IMU和激光雷达"

重置你的本地分支到远程分支的状态。但是，请注意，这将丢失你所有的本地更改和提交：
1获取远程仓库的最新更改：
git fetch origin
2切换到远程分支的最新状态
git reset --hard origin/main
git reset --hard origin

### git 代理
export https_proxy=socks5://127.0.0.1:1080
export http_proxy=socks5://127.0.0.1:1080

$env:https_proxy = "socks5://127.0.0.1:1080"
$env:http_proxy = "socks5://127.0.0.1:1080"

set https_proxy=socks5://127.0.0.1:1080
set http_proxy=socks5://127.0.0.1:1080

### 将git clone的别人代码库上传到自己的 github 代码仓
1、打开你克隆的仓库的目录。
使用以下命令添加新的远程仓库（假设你新的GitHub仓库URL为 https://github.com/<你的用户名>/<新仓库名>.git）：
git remote set-url origin https://github.com/<你的用户名>/<新仓库名>.git

2、推送代码到新的GitHub仓库，如果你使用 set-url 命令，你可以直接推送：
git push -u origin --all  # 推送所有分支
git push -u origin --tags # 推送所有标签

### 将 git fork 的代码上传到gitee
#### 添加 Gitee 远程仓库
git remote add gitee https://gitee.com/shaoxiang/IsaacLab.git
#### 推送代码到 Gitee
git push -u gitee --all
git push -u gitee --tags
#### 后续推送到 Gitee
git push gitee main # 推送到 Gitee

### 在使用 Conda 创建新环境时，你可以选择指定新环境的路径地址。

conda create --prefix D:/anaconda3/envs/modelscope python=3.10

### 修改远程仓库地址

git remote set-url origin https://gitee.com/shaoxiang/IsaacLab.git

---

## hugging face 下载
pip install -U huggingface_hub

repo_id：模型/数据集的完整id（如amritgupta/qafacteval）

### 命令行方式
设置国内镜像
Linux:
```
export HF_ENDPOINT=https://hf-mirror.com
```
windows powershell:
```
$env:HF_ENDPOINT = "https://hf-mirror.com"
```
#### 数据集下载
huggingface-cli download --repo-type dataset unitreerobotics/LAFAN1_Retargeting_Dataset --local-dir LAFAN1_Retargeting_Dataset

#### AgiBotDigitalWorld 数据集下载 
##### Make sure you have git-lfs installed (https://git-lfs.com)
git lfs install

##### When prompted for a password, use an access token with write permissions.
##### Generate one from your settings: https://huggingface.co/settings/tokens
git clone https://huggingface.co/datasets/agibot-world/AgiBotDigitalWorld

##### If you want to clone without large files - just their pointers
GIT_LFS_SKIP_SMUDGE=1 git clone https://huggingface.co/datasets/agibot-world/AgiBotDigitalWorld

### 模型下载

export HF_ENDPOINT=https://hf-mirror.com
$env:HF_ENDPOINT="https://hf-mirror.com"
set HF_ENDPOINT=https://hf-mirror.com

huggingface-cli download nvidia/GR00T-N1-2B --local-dir GR00T-N1-2B

git clone https://huggingface.co/nvidia/GR00T-N1-2B
cd GR00T-N1-2B
git lfs pull  # 下载大文件

git clone https://github.com/NVIDIA/Isaac-GR00T.git

huggingface-cli download nvidia/PhysicalAI-Robotics-GR00T-X-Embodiment-Sim --repo-type dataset --include "gr1_arms_only.CanSort/**" --local-dir gr00t_dataset