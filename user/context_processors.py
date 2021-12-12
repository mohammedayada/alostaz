def categories_processor(request):
    if request.user.is_anonymous:
        is_chairman = False
        is_chef = False
    else:
        is_chairman = (request.user.type == 'chairman')
        is_chef = (request.user.type == 'editor_in_chief')
    return {'is_chairman': is_chairman,
            'is_chef': is_chef,
            }
