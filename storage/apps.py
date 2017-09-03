from django.apps import AppConfig


class StoargeConfig(AppConfig):
    name = 'stoarge'


def navigation():
    return {
        'title': {
            'name': 'LYnStorage',
            'url': 'storage'
        },
        'left': [
            {
                'name': '업로드',
                'url': 'storage-upload'
            },
        ],
        'right': [
            {
                'dropdown': True,
                'name': 'LYnLab',
                'submenu': [
                    {
                        'name': '블로그',
                        'url': 'blog'
                    },
                    {
                        'name': '위키',
                        'url': 'wiki'
                    },
                    {
                        'name': '스토리지',
                        'url': 'storage'
                    },
                    {
                        'outer_url': True,
                        'name': '앉아서 집에가자',
                        'url': 'https://bus.lynlab.co.kr'
                    }
                ]
            },
        ],
    }
