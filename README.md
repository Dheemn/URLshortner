# URLshortner
A simple web application to create short links 

| Endpoint         | Description                                                                                            |
|------------------|--------------------------------------------------------------------------------------------------------|
|         `/`        | The base endpoint                                                                                      |
| `/{6-char-string}` | This takes the 6 character string as input in the URL and redirect to the corresponding mapped URL     |
|       `new/`      | This endpoint is used to create the shortlink. <br>`Input`: the URL in request body. <br>`Output`: the path in |