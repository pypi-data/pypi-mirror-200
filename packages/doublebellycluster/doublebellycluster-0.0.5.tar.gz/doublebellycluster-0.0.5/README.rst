Doublebellycluster
******************

Doublebellycluster - это Библиотека кластеризации на анализе плотности


Установка
*********


.. code:: bash

    pip install doublebellycluster

или

.. code:: bash

    python setup.py install

Примеры
*******

.. code:: python

    import doublebellycluster

    # J lkkkkkkk класс
    doubleclustering = doublebellycluster.Doubleclustering()
    # запустить кластеризацию на данных xy
    # данные должны быть непрерывными
    doubleclustering.do_continious( xy, show_plots = True,
                          calc_aggregate_all= False,
                          percentile_cut = 10)

    
    # Есть еще функции

    # Сравнивает две последовательности
    doublebellycluster.seq_match(a, b)

    # найти расстояние между кластерами
    doubleclustering.get_inter_dist(df,col)




История изменений
*****************

* **Release 1.3.2 (2023-03-20)**

  * Пока работает только на непрерывных данных

* **Release 1.3.1 (2023-02-28)**

  * Если гео данные - то их нужно подготавливать :code:`import pyproj` 
  * Исправлено :code:`AttributeError` при вызове :code:`ResourceLinkObject.public_listdir()`
