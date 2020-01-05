# Web crawler

This web crawler crawls the [Pastebin](https://pastebin.com/) site and stores the most recent "pastes" in a tinydb table.

### Prerequisites

docker

### Installing

```
docker run -d -v `pwd`:`pwd` -w `pwd` --name web_crawler alperthod/repo:web_crawler
```

### Debugging

In order to debug the container execution and see the current db file do:

```
tail -f web_crawler.log
```
in order to see the log file.

And in order to see the current *tiny_db* file type
```
tail -f pastebin_db.json
```

## Implementation explenation

This code run in two iterations:
* Crawling "https://pastebin.com/archive" and saving all pastes keys from it to a set
* Iterating all keys in the set and if they are not in the db yet- fetching the data from the specific paste page


### Parallelism

This task does not have any parallelism (multithreading or anything) since the only place I really thought it should be worth trying
was in fetching the pastes from [Pastebin](https://pastebin.com/), but it queried too many times too fast and it git my ip blocked so I decided to reduce the efficiency in order to avoid the blocking.

## Packages

* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - Html parser
* [Dateutil](https://dateutil.readthedocs.io/en/stable/) - Date parser
* [Tinydb](https://tinydb.readthedocs.io/en/latest/intro.html) - No-sql DB

## Authors

* **Hod Alpert**
