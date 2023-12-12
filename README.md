### Попытки отправить факс с помощью API rufax web service и python
Запуск файла **test.py** выдает ошибку:
`Traceback (most recent call last):
  File "C:\NewDjangoProjects\rufax\test.py", line 52, in <module>
    response = client.post(url, json=submit_fax_list_request)    
AttributeError: 'Client' object has no attribute 'post'`



