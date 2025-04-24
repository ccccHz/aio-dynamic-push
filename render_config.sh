#!/bin/bash
# # 加载.env文件中的变量
# set -o allexport
# source env/.env
# set +o allexport

# # 读取 JSON payload 内容并转义为单行
# BILIBILI_PAYLOAD=$(<"$BILIBILI_PAYLOAD_FILE" jq -c .)
# douyu_room_id_list=$'\n'"$(echo "$DOUYU_ROOM_ID_LIST" | tr ',' '\n' | sed 's/^/  - /')"

# # 替换环境变量
# export BILIBILI_PAYLOAD
# export douyu_room_id_list

# # 渲染模板
# envsubst < config.yml > config.final.yml

# echo "配置已生成：config.final.yml"

# set -e

# # 加载 .env 中的变量
# export $(grep -v '^#' env/.env | xargs)

# # Load the entire JSON file into BILIBILI_PAYLOAD
# export BILIBILI_PAYLOAD="$(cat $BILIBILI_PAYLOAD_FILE)"

# # Use envsubst to render config.yml and output to config.final.yml, then use yq to split the comma-separated string into a list
# envsubst <config.yml |
#     yq eval '.query_task[].payload = env(BILIBILI_PAYLOAD) | .query_task[] |= (select(.type=="douyu") .room_id_list |= split(","))' - >config.final.yml

# echo "配置已生成：config.final.yml"

#!/bin/bash
set -eo pipefail

echo "正在加载环境变量..."
export $(grep -v '^#' env/.env | xargs)

echo "正在加载BILIBILI_PAYLOAD..."
BILIBILI_PAYLOAD=$(cat "$BILIBILI_PAYLOAD_FILE")
export BILIBILI_PAYLOAD

echo "开始生成最终配置文件..."
# 管道链式处理：
# 1. 先替换环境变量
# 2. 然后设置bilibili任务payload
# 3. 最后处理douyu任务room_id_list
envsubst <config.yml |
    yq eval '.query_task[] |= (select(.type=="bilibili") .payload = env(BILIBILI_PAYLOAD))' - |
    yq eval '.query_task[] |= (select(.type=="douyu") .room_id_list |= split(","))' - |
    yq eval '.query_task[] |= (select(.type=="bilibili") .uid_list |= split(","))' - >config.final.yml
# envsubst <config.yml |
#     yq eval '.query_task[] |= (select(.type=="bilibili") .payload = env(BILIBILI_PAYLOAD))' - |
#     yq eval '.query_task[] |= (select(.type=="douyu") .room_id_list |= split(","))' - >config.final.yml

echo "✅ 配置已成功生成：config.final.yml"
