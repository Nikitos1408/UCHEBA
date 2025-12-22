# Выполнил - Угарин Никита Александрович

## RESTful веб-приложение на Spring Boot

**Примеры запросов:**

**Создание задачи:**
```json
POST /api/tasks
Content-Type: application/json

{
  "title": "Изучить Spring Boot",
  "description": "Изучить основы Spring Boot и REST API"
}
```

**Обновление задачи:**
```json
PUT /api/tasks/1
Content-Type: application/json

{
  "title": "Изучить Spring Boot",
  "description": "Изучить основы Spring Boot и REST API",
  "completed": true
}
```

**Расположение:** `src/main/java/com/example/demo/controller/TaskController.java`

---

## Структура проекта

```
demo/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/example/demo/
│   │   │       ├── config/
│   │   │       │   ├── DataInitializer.java      # Инициализация тестовых данных
│   │   │       │   └── SecurityConfig.java       # Конфигурация безопасности
│   │   │       ├── controller/
│   │   │       │   └── TaskController.java       # REST контроллер
│   │   │       ├── entity/
│   │   │       │   └── Task.java                 # Модель задачи
│   │   │       ├── exception/
│   │   │       │   └── GlobalExceptionHandler.java  # Обработка ошибок
│   │   │       ├── repository/
│   │   │       │   └── TaskRepository.java       # Репозиторий
│   │   │       ├── service/
│   │   │       │   └── TaskService.java          # Сервисный слой
│   │   │       └── DemoApplication.java         # Главный класс приложения
│   │   └── resources/
│   │       └── application.yml                  # Конфигурация приложения
│   └── test/
└── pom.xml                                       # Maven конфигурация
```

---

## Запуск приложения

### Требования
- Java 17 или выше
- Maven 3.6+

### Команды для запуска

**Через Maven:**
```bash
cd demo
mvn spring-boot:run
```

**Через IDE:**
Запустить класс `DemoApplication.java`

### После запуска
- Приложение доступно по адресу: `http://localhost:8080`
- H2 консоль: `http://localhost:8080/h2-console`
- REST API: `http://localhost:8080/api/tasks`

---


