FOLDER = 'main/'
TEMPLATES = {
    'category': {
        'create': f'{FOLDER}category_delete.html',
        'update': f'{FOLDER}category_update.html',
        'list': f'{FOLDER}category_list.html',
    },
    'transactions': {
        'create': f'{FOLDER}create_transaction.html',
        'list': f'{FOLDER}transaction_list.html',
    },
    'profile': {
        'info': f'{FOLDER}profile.html',
        'replenishment': f'{FOLDER}replenishment.html'
    },
}
