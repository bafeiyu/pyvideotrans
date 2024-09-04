# zh_recogn 识别
import requests

from videotrans.configure import config
from videotrans.configure._except import LogExcept
from videotrans.util import tools


def recogn(*,
           audio_file=None,
           cache_folder=None,
           uuid=None,
           set_p=None,
           inst=None):
    if config.exit_soft or (config.current_status != 'ing' and config.box_recogn != 'ing'):
        return False
    api_url = config.params['zh_recogn_api'].strip().rstrip('/').lower()
    if not api_url:
        raise LogExcept('必须填写地址')
    if not api_url.startswith('http'):
        api_url = f'http://{api_url}'
    if not api_url.endswith('/api'):
        api_url += '/api'
    files = {"audio": open(audio_file, 'rb')}

    if set_p:
        tools.set_process(
            f"识别可能较久，请耐心等待，进度可查看zh_recogn终端",
            type='logs',
            uuid=uuid)
    try:
        res = requests.post(f"{api_url}", files=files, proxies={"http": "", "https": ""}, timeout=3600)
        config.logger.info(f'zh_recogn:{res=}')
    except Exception as e:
        raise
    else:
        res = res.json()
        if "code" not in res or res['code'] != 0:
            raise LogExcept(f'{res["msg"]}')
        if "data" not in res or len(res['data']) < 1:
            raise LogExcept('识别出错')
        return res['data']
