# common

> A common library for the project.

## Install

### poetry
```bash
poetry add git+https://github.com/ether-trading-system/common.git
```

아래와 같이 dependencies에 추가되면 정상 설치 입니다.
```
# pyproject.toml
[tool.poetry.dependencies]
...
common = {git = "https://github.com/ether-trading-system/common.git"}
```


### pip
```bash
pip install git+https://github.com/ether-trading-system/common.git
```

## Update

### poetry
```bash
poetry update common 
```


## Discord
디스코드 알림을 위한 모듈입니다.

### 설정
.env를 사용해 환경변수를 설정합니다.
채널을 추가하기 위해 아래 형식을 맞춰서 webhook을 등록해주세요

- `sample_topic`은 웹훅 대한 식별자 입니다. 원하는 웹훅을 식별하기 위한 key 정의해주세요.
- `name`은 웹훅의 이름을 정의해주세요. 채널에 메시지를 보낼 때 제목으로 사용됩니다.
- `url`은 웹훅의 URL을 정의해주세요. 웹훅을 통해 메시지를 보낼 수 있습니다.

```json
{
  "sample_topic": {
    "name": "sample",
    "url": "https://discord.com/api/webhooks/1274381556315852882/wyhFO7Xys5JlSi0Gypm9FppyGI_SstKXJcJ4rLLPoYP1VrcTsw-6hwTqMUAKeyuC2y5E"
  }
}
```

위 형식으로 정의된 json을 환경변수로 등록합니다.

```bash
COMMON_DISCORD='{ "sample_topic": { "name": "sample", "url": "https://discord.com/api/webhooks/1274381556315852882/wyhFO7Xys5JlSi0Gypm9FppyGI_SstKXJcJ4rLLPoYP1VrcTsw-6hwTqMUAKeyuC2y5E" } }'
```

### Usage

[`__test__ > discord.py`](__test__/discord.py) 파일을 참고해주세요.

```python
from common.discord import notify, notify_info, DiscordMessage, MessageColor

message = DiscordMessage(
    topic='sample_topic',
    title='title',
    message='message',
    data={'key': 'value'}
)

await notify(message, MessageColor.INFO)
await notify_info(message)
```
