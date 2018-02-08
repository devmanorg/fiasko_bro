# Решатель квадратных уравнений

Код решает квадратное уравнение

# Как использовать

```Lots and lots of inline code```

Необходимо импортировать `get_roots`, вызов происходит так: `root1, root2 = get_roots(a, b, c)`, тут `a, b, с` -  коэффициенты квадратного уравнения, а `root1, root2` корни.
Пример:

```The confusion between inline and multiline code can lead to false positives```

```Python
from quadratic_equation import get_roots

root1, root2 = get_roots(1, 2, -3)
print(root1,root2)
```

# Как запустить

Скрипт требует для своей работы установленного интерпретатора Python версии 3.5

Запуск на Linux:

```bash
python tests.py # может понадобиться вызов python3 вместо python, зависит от настроек операционной системы
```

Запуск на Windows происходит аналогично.

# Цели проекта

Код создан в учебных целях. В рамках учебного курса по веб-разработке ― [DEVMAN.org](https://devman.org)
