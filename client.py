from celery_project.tasks import add,mul
result = add.delay()
print result.get()
result2 = mul.delay()
print result2.get()

