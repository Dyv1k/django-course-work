from ..mainConfig import mainConfig

contacts = {
    **mainConfig,
    'developer': {
        'company': 'PskovHack',
        'name': 'Дуванов Илья Алексеевич',
        'tag': 'dyvik',
        'description': [
            'Web-developer',
            'Верстка современных адаптивных сайтов для любого направления - от создания сайта-визитки до интернет магазина',
            'Стек технологий: js, ts, python, React, Vue, Django, NextJs',
            'CMS системы: bitrix, wordpress',
            '(если Вы это читаете, поставьте пожалуйста автомат :) )'
        ],
        'contacts': {
            'email': {
                'link': 'duvanov.ilja@gmail.com',
                'image': 'images/social/email.svg'
            },
            'discord': {
                'link': 'https://discord.gg/ahAP33m4',
                'image': 'images/social/discord.svg'
            },
            'vk': {
                'link': 'https://vk.com/dyvik',
                'image': 'images/social/vk.svg'
            },
            'telegram': {
                'link': 'https://t.me/dyvik',
                'image': 'images/social/telegram.svg'
            },
        }
    }
}