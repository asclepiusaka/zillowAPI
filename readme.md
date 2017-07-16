## design idea
the current design idea about zillow API:

1. a wrapper class, has a lot of different wrapper method, each corresponding to one specific api, take(apikey, parameters) as input.
* 仔细想想我们好像并不需要将不同的方法放在同一个class里，没啥必要，他们之间几乎不共享信息？
2. inside the class, requests.get() is called and all kinds of exception is handled. A design idea is that method should return a XXAPIResult class, with their
attrs as different information, and a raw content attr to save the initial response body information.
3. fully test set should be provided, with official unittest module.
Since we have got several API key from 

## challenge:
how to return different response code as exception, for example: the daily limitation is reached.
or answer the following question: should we return it as exception?

## design detail:

## learnt:
* how to reveal inner layer exception information to higher layer.
