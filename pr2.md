## Задача 1
Вывести служебную информацию о пакете matplotlib (Python). Разобрать основные элементы содержимого файла со служебной информацией из пакета. Как получить пакет без менеджера пакетов, прямо из репозитория?
```bash
(venv) C:\Users\lordp\OneDrive\Рабочий стол\confupr\task_2>pip3 show matplotlib
Name: matplotlib
Version: 3.9.2
Summary: Python plotting package
Home-page:
Author: John D. Hunter, Michael Droettboom
Author-email: Unknown <matplotlib-users@python.org>
License: License agreement for matplotlib versions 1.3.0 and later
=========================================================
Location: C:\Users\lordp\OneDrive\Рабочий стол\confupr\task_2\venv\Lib\site-packages
Requires: contourpy, cycler, fonttools, kiwisolver, numpy, packaging, pillow, pyparsing, python-dateutil
Required-by:
```
Установка без pip, тоже самое надо сделать со всеми зависимостями
```bash
pip install git+https://github.com/matplotlib/matplotlib.git
cd matplotlib
python setup.py install
```

## Задача 2
Вывести служебную информацию о пакете express (JavaScript). Разобрать основные элементы содержимого файла со служебной информацией из пакета. Как получить пакет без менеджера пакетов, прямо из репозитория?
```bash
>npm show express

express@4.21.0 | MIT | deps: 31 | versions: 279
Fast, unopinionated, minimalist web framework
http://expressjs.com/

keywords: express, framework, sinatra, web, http, rest, restful, router, app, api

dist
.tarball: https://registry.npmjs.org/express/-/express-4.21.0.tgz
.shasum: d57cb706d49623d4ac27833f1cbc466b668eb915
.integrity: sha512-VqcNGcj/Id5ZT1LZ/cfihi3ttTn+NJmkli2eZADigjq29qTlWi/hAQ43t/VLPq8+UX06FCEx3ByOYet6ZFblng==
.unpackedSize: 220.8 kB

dependencies:
accepts: ~1.3.8            cookie: 0.6.0              finalhandler: 1.3.1        parseurl: ~1.3.3
array-flatten: 1.1.1       debug: 2.6.9               fresh: 0.5.2               path-to-regexp: 0.1.10
body-parser: 1.20.3        depd: 2.0.0                http-errors: 2.0.0         proxy-addr: ~2.0.7
content-disposition: 0.5.4 encodeurl: ~2.0.0          merge-descriptors: 1.0.3   qs: 6.13.0
content-type: ~1.0.4       escape-html: ~1.0.3        methods: ~1.1.2            range-parser: ~1.2.1
cookie-signature: 1.0.6    etag: ~1.8.1               on-finished: 2.4.1         safe-buffer: 5.2.1
(...and 7 more.)

maintainers:
- wesleytodd <wes@wesleytodd.com>
- dougwilson <doug@somethingdoug.com>
- linusu <linus@folkdatorn.se>
- sheplu <jean.burellier@gmail.com>
- blakeembrey <hello@blakeembrey.com>
- ulisesgascon <ulisesgascondev@gmail.com>
- mikeal <mikeal.rogers@gmail.com>

dist-tags:
latest: 4.21.0  next: 5.0.0

published a week ago by wesleytodd <wes@wesleytodd.com>
```
Установка без npm
```bash
git clone https://github.com/expressjs/express.git
cd express
```
## Задача 3
Сформировать graphviz-код и получить изображения зависимостей matplotlib и express.
```bash

```
