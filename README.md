# Validation

## Run server:

From project root directory:

```bash
gunicorn validation.falcon_server.app:api
```

## Test from curl:

```bash
curl --header "Content-Type: application/json"\
    -X POST \
    -d '{"order_id":{"0":2,"1":2,"2":2,"3":2,"4":2,"5":2,"6":2,"7":2,"8":2,"9":3},\
    "product_id":{"0":33120,"1":28985,"2":9327,"3":45918,"4":30035,"5":17794,"6":40141,"7":1819,"8":43668,"9":33754},\
    "add_to_cart_order":{"0":1,"1":2,"2":3,"3":4,"4":5,"5":6,"6":7,"7":8,"8":9,"9":1},\
    "reordered":{"0":1,"1":1,"2":0,"3":1,"4":0,"5":1,"6":1,"7":1,"8":0,"9":1}}' \
    http://127.0.0.1:8000/test
```