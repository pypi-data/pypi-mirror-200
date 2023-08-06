YaDisk
======

.. image:: https://img.shields.io/readthedocs/yadisk.svg
   :alt: Read the Docs
   :target: https://yadisk.readthedocs.io/en/latest/

.. image:: https://img.shields.io/pypi/v/yadisk.svg
   :alt: PyPI
   :target: https://pypi.org/project/yadisk

YaDisk - это библиотека-клиент REST API Яндекс.Диска.

.. _Read the Docs (EN): https://yadisk.readthedocs.io
.. _Read the Docs (RU): https://yadisk.readthedocs.io/ru/latest
.. _yadisk-async: https://github.com/ivknv/yadisk-async

Документация доступна на `Read the Docs (RU)`_ и `Read the Docs (EN)`_.

Установка
*********

.. code:: bash

    pip install yadisk

или

.. code:: bash

    python setup.py install

Примеры
*******

.. code:: python

    import Doubleclustering

    # J lkkkkkkk класс
    doubleclustering = Doubleclustering()
    # запустить кластеризацию на данных xy
    # данные должны быть непрерывными
    doubleclustering.do_continious( xy, show_plots = True,
                          calc_aggregate_all= False,
                          percentile_cut = 10)

    
    # Есть еще функции

    # Сравнивает две последовательности
    seq_match(a, b)

    # найти расстояние между кластерами
    get_inter_dist(df,col)


    # Создаёт новую папку "/test-dir"
    print(y.mkdir("/test-dir"))



История изменений
*****************

* **Release 1.3.2 (2023-03-20)**

  * Пока работает только на непрерывных данных

* **Release 1.3.1 (2023-02-28)**

  * Если гео данные - то их нужно подготавливать :code:`import pyproj` 
  * Исправлено :code:`AttributeError` при вызове :code:`ResourceLinkObject.public_listdir()`
