def func_request(self,request):
    print('\n' + '='*40)
    print(f"МЕТОД: {request.method} | ШЛЯХ: {request.path}")
    print('='*40)
    
    print("1. Дані з фронтенду (request.data):")
    print(request.data)
    
    print("\n2. URL параметри (request.query_params):")
    print(request.query_params)
    
    print("\n3. Хто робить запит (request.user):")
    if request.user.is_authenticated:
        print(f"Юзер: {request.user.username} (ID: {request.user.id})")
    else:
        print("Анонімний користувач")
        
    print('='*40 + '\n')
    