# create a curl request with:
# 1. 'ce-ref' = '1234' in header
# 2. 'delta' = 'task name' in body
curl -X POST -H "ce-ref: tasks/somerandomuuid/234567890/task" -d '{"delta":"Find a pigeon"}' http://0.0.0.0:8080/predict
```

curl --header "Content-Type: application/json" \
                       --request POST \
                       --data '{"some":"request"}' \
                       http://0.0.0.0:8080/predict
