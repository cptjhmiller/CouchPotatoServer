from .main import HDtorrents

def autoload():
    return HDtorrents()

config = [{
    'name': 'hdtorrents',
    'groups': [
        {
            'tab': 'searcher',
            'list': 'torrent_providers',
            'name': 'HDTorrents',
            'description': '<a href="https://hdts.ru">HDTorrents</a>',
            'wizard': True,
			'icon': 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABi0lEQVR4AZWSzUsbQRjGdyabTcvSNPTSHlpQQeMHJApC8CJRvHgQQU969+LJP8G7f4N3DwpeFRQvRr0EKaUl0ATSpkigUNFsMl/r9NmZLCEHA/nNO5PfvMPDm0DI6fV3ZxiolEICe1oZCBVCCmBPKwOh2ErKBHGE4KYEXBpSLkUlqO4LcM7f+6nVhRnOhSkOz/hexk+tL+YL0yPF2YmN4tynD++4gTLGkNNac9YFLoREBR1+cnF3dFY6v/m6PD+FaXiNJtgA4xYbABxiGrz6+6HWaI5/+Qh37YS0/3Znc8UxwNGBIIBX22z+/ZdJ+4wzyjpR4PEpODg8tgUXBv2iWUzSpa12B0IR6n6lvt8Aek2lZHb084+fdRNgrwY8z81PjhVy2d2ttUrtV/lbBa+JXGEpDMPnoF2tN1QYRqVUtf6nFbThb7wk7le395elcqhASLb39okDiHY00VCtCTEHwSiH4AI0lkOiT1dwMeSfT3SRxiQWNO7Zwj1egkoVIQFMKvSiC3bcjXq9Jf8DcDIRT3hh10kAAAAASUVORK5CYII=',
            'options': [
                {
                    'name': 'enabled',
                    'type': 'enabler',
                    'default': False,
                },
                {
                    'name': 'username',
                    'default': '',
                },
                {
                    'name': 'password',
                    'default': '',
                    'type': 'password',
                },
                {
                    'name': 'seed_ratio',
                    'label': 'Seed ratio',
                    'type': 'float',
                    'default': 1,
                    'description': 'Will not be (re)moved until this seed ratio is met.',
                },
                {
                    'name': 'seed_time',
                    'label': 'Seed time',
                    'type': 'int',
                    'default': 40,
                    'description': 'Will not be (re)moved until this seed time (in hours) is met.',
                },
                {
                    'name': 'extra_score',
                    'advanced': True,
                    'label': 'Extra Score',
                    'type': 'int',
                    'default': 20,
                    'description': 'Starting score for each release found via this provider.',
                }
            ],
        },
    ],
}]
