# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['celery_yandex_serverless']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.26.101,<2.0.0',
 'celery>=5.2.7,<6.0.0',
 'django>=4,<5',
 'pycurl>=7.45.2,<8.0.0']

setup_kwargs = {
    'name': 'celery-yandex-serverless',
    'version': '0.0.2',
    'description': '',
    'long_description': '# Celery Yandex Serverless\n\nМодуль, позволяющий запустить celery-worker внутри Yandex Cloud Serverless Container.\n\n**Классический подход с отдельно запущенным воркером**\n1. Бекенд отправляет задачу в очередь.\n2. Отдельный процесс воркера забирает задачу из очереди и выполняет ее.\n\n**Serverless-подход**\nВ Serverless подходе предполагается, что нет никаких запущенных постоянно процессов приложения. Эти процессы запускаются\nлибо по запросу пользователя, либо по различным тригерам облаком. \n\nМодуль `celery-yandex-serverless` помогает запустить воркер следующим образом:\n1. Бекенд отправляет задачу в очередь\n2. После попадания задачи в очередь срабатывает триггер, который делает http-запрос serverless-контейнеру.\n3. Serverless-контейнер запускает код задачи, который ранее выполнялся в воркере.\n\n## Использование\n\n### Подключение Celery к Yandex Message Queue\n\n1. Перейдите на страницу каталога в Яндекс.Облаке\n2. Зайдите в раздел **Сервисные аккаунты**\n3. Посмотрите название сервисного аккаунта в каталоге Яндекс.Облака\n4. Сгенерируйте `ACCESS_KEY` и `SECRET_KEY` с помощью команды \n(замените `SERVICE_ACCOUNT_NAME` на название сервисного аккаунта):\n\n```bash\nyc iam access-key create --service-account-name SERVICE_ACCOUNT_NAME\n```\n\nКоманда вернет следующую информацию. Сохраните ее, она пригодится в будущем.\n\n```yml{5,6}\naccess_key:\n  id: aje...\n  service_account_id: aje...\n  created_at: "2023-03-24T17:49:01.555836400Z"\n  key_id: YCAJ... # <- Это access key\nsecret: YCPM... # <- Это secret key\n```\n\n### Настройка\nУкажите переменные окружения с использованием только что полученных данных:\n\n```\nAWS_ACCESS_KEY_ID="access key, скопированный выше"\nAWS_SECRET_ACCESS_KEY="secret key, скопированный выше"\nAWS_DEFAULT_REGION="ru-central1"\nCELERY_BROKER_URL=sqs://message-queue.api.cloud.yandex.net:443\nCELERY_BROKER_IS_SECURE=True\n```\n\nВ файле `settings.py` укажите:\n\n```python\nCELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")\nCELERY_BROKER_TRANSPORT_OPTIONS = {\n    \'is_secure\': os.environ.get("CELERY_BROKER_IS_SECURE", \'false\').lower() == \'true\'\n}\n```\n\nПосле этого отправьте celery-задачу, чтобы в Яндекс.Облаке появилась очередь.\n\n### Подключение модуля\n\n1. `pip install celery-yandex-serverless` - установите модуль\n2. В urls.py (`projectname` замените на название проекта):\n```python\nfrom django.urls import path\nfrom celery_yandex_serverless.django import worker_view_factory\n\nfrom projectname.celery import app\n\nurlpatterns = [\n    # другие адреса...\n    path("worker/<str:key>/", worker_view_factory(app)),\n]\n```\n\n3. Установите переменную окружения `CELERY_YANDEX_SERVERLESS_KEY` со случайным ключом. \nОн предотвратит нежелательные запуски воркеров по прямому обращению к URL.\n\n### Создание триггера в Яндекс.Облаке\n\nВ консольной команде ниже сделайте замены и выполните ее:\n- `YANDEX_MESSAGE_QUEUE_ARN` - ARN очереди\n- `SERVICE_ACCOUNT_NAME` - название сервисного аккаунта\n- `SERVERLESS_CONTAINER_NAME` - название serverless-контейнера\n- `CELERY_YANDEX_SERVERLESS_KEY` - ключ, созданный ранее\n\n```bash\nyc serverless trigger create message-queue \\\n  --name celery \\\n  --queue YANDEX_MESSAGE_QUEUE_ARN \\\n  --queue-service-account-name SERVICE_ACCOUNT_NAME \\\n  --invoke-container-name SERVERLESS_CONTAINER_NAME \\\n  --invoke-container-service-account-name SERVICE_ACCOUNT_NAME \\\n  --invoke-container-path /worker/CELERY_YANDEX_SERVERLESS_KEY \\\n  --batch-size 1 \\\n  --batch-cutoff 10s \n```\n\n## Статьи в Яндекс.Облаке\n- [Подключение Celery](https://cloud.yandex.ru/docs/message-queue/instruments/celery)\n- [Документация по созданию триггеров через yc](https://cloud.yandex.ru/docs/cli/cli-ref/managed-services/serverless/trigger/create/message-queue).\n- [Подробнее про работу триггера](https://cloud.yandex.ru/docs/serverless-containers/concepts/trigger/ymq-trigger).\n\n## Автор\n[Атнагулов Артур](https://atnartur.dev)\n\nЛицензия MIT.\n',
    'author': 'atnartur',
    'author_email': 'i@atnartur.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
