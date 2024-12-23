# Лабораторная работа № 6 - Установка корпоративной вики и системы управления задачами (Угарин Никита Александрович)

## 1. Введение
Цель и задача: Цель данной лабораторной работы — изучить процесс установки корпоративной вики и системы управления задачами (таск-трекера) на локальный сервер (ваш компьютер), оценить их основные возможности, особенности настройки и, опционально (что является очень желательным в реальных рабочих условиях), опробовать их интеграцию.

В данной работе рассматривается OpenProject, которая является, как и корпоративной вики, так и системой управления задачами.

## 2. Пошаговая установка
1.	Подготовка среды: Убедитесь, что на персональном компьютере установлен Docker.
2.	Запуск контейнера OpenProject: Для запуска OpenProject был использован следующий Docker-контейнер:
```
docker run -it -p 8080:80 -e OPENPROJECT_SECRET_KEY_BASE=secret -e OPENPROJECT_HOST__NAME=localhost:8080 -e OPENPROJECT_HTTPS=false -e OPENPROJECT_DEFAULT__LANGUAGE=en openproject/openproject:15
```
3.	Ожидание запуска: Docker загрузил образ openproject/openproject:15 и запустил контейнер. Процесс первого запуска может занять несколько минут.

 ![image](https://github.com/user-attachments/assets/b060c393-e2bc-4aaa-bc70-743549b1456c)

4.	Проверка доступности: После запуска OpenProject стал доступен по адресу http://localhost:8080 в веб-браузере

 ![image](https://github.com/user-attachments/assets/d7c87dbf-197f-4dde-bbd8-30203d0bd103)

5.	Вход: для входа надо ввести стандартный логин и пароль – admin, после чего его можно будет заменить. После выполнения всех действий нас пустит на главное меню.

 ![image](https://github.com/user-attachments/assets/02703f71-8b95-441d-b16e-166c65268591)

Чтобы остановить контейнер, просто нажмите CTRL-C.


## Описание изменений в конфигурационных файлах:
Конфигурационные файлы OpenProject не были модифицированы, так как все настройки выполнялись через переменные среды Docker. Это является одним из преимуществ Docker-контейнеров, поскольку все необходимые настройки инкапсулируются в рамках образа.
Команды, использованные в процессе установки, и их назначение:\
•	docker run: Основная команда для создания и запуска нового Docker-контейнера.\
•	-it: Запускает контейнер в интерактивном режиме (но в данном случае контейнер работает в detached mode, так как это OpenProject). -i обеспечивает интерактивный режим, а -t выделяет псевдотерминал.\
•	-p 8080:80: Пробрасывает порт 80 на контейнере на порт 8080 на хосте. Это позволяет получить доступ к OpenProject через http://localhost:8080.
•	-e OPENPROJECT_SECRET_KEY_BASE=secret: Задает секретный ключ для OpenProject.\
•	-e OPENPROJECT_HOST__NAME=localhost:8080: Указывает хостнейм для OpenProject (используется для генерации ссылок в приложении).\
•	-e OPENPROJECT_HTTPS=false: Отключает использование HTTPS.\
•	-e OPENPROJECT_DEFAULT__LANGUAGE=en: Устанавливает английский язык по умолчанию.\
•	openproject/openproject:15: Указывает имя Docker-образа и его версию, используемые для создания контейнера.\

## 3. Функциональный анализ
Краткое описание возможностей: OpenProject - это полнофункциональная система управления проектами с открытым исходным кодом, которая включает в себя:\
•	Управление задачами: Создание, назначение, отслеживание задач и подзадач.\
•	Планирование проектов: Gantt-диаграммы, календари, дорожные карты.\
•	Управление временем: Учет затраченного времени на задачи.\
•	Управление ресурсами: Распределение ресурсов между проектами.\
•	Wiki и форумы: Создание общей базы знаний и обсуждений.\
•	Agile-поддержка: Канбан-доски и Scrum-инструменты.
## Оценка удобства использования:
OpenProject имеет понятный и интуитивно понятный интерфейс, который может быть адаптирован под нужды пользователя. Ещё OpenProject предлагает множество настроек для различных аспектов, таких как типы задач, рабочие процессы и пользовательские роли, а также предоставляет гибкую систему управления доступом на основе ролей. Пользователи могут быть добавлены в проекты и иметь различные уровни доступа в зависимости от их роли.
## Описание основных функций:
OpenProject позволяет объединить все проекты в одном месте, что облегчает их отслеживание и управление. Присутствуют инструменты для совместной работы (задачи, wiki, форумы) облегчают взаимодействие между членами команды. Также OpenProject предоставляет инструменты для генерации отчетов по проектам, что позволяет отслеживать прогресс и выявлять проблемные области.
## 4. Интеграция
Примеры использования интеграции в корпоративной среде: 
Интеграция OpenProject может быть полезна для связи: с системами контроля версий (Git, Subversion), с инструментами для обмена сообщениями (Slack, Mattermost), с другими бизнес-приложениями (CRM, ERP).
## 5. Заключение
Преимущества OpenProject:\
•	Полнофункциональность: широкий набор инструментов для управления проектами.\
•	Бесплатность: Open-source лицензия.\
•	Гибкость: множество настроек и возможностей кастомизации.\
•	Интеграция: возможность интеграции с другими системами.
## Недостатки OpenProject:
Сложность: для полноценного использования требуется некоторое время на изучение. 
Нагрузка на ресурсы: в некоторых случаях может требовать достаточно ресурсов для работы.
## Рекомендации по применению в корпоративной среде:
OpenProject является отличным выбором для компаний любого размера, которым требуется мощная и гибкая система управления проектами. Рекомендуется использовать Docker для упрощения развертывания и масштабирования.
## 6. Ссылки на использованные источники
•	Официальный сайт OpenProject: https://www.openproject.org/ \
•	Страница Docker Hub образа OpenProject: https://hub.docker.com/r/openproject/openproject/ \
•	Официальная документация Docker
