package com.example.demo.config;

import com.example.demo.entity.Task;
import com.example.demo.repository.TaskRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class DataInitializer implements CommandLineRunner {
    
    private final TaskRepository taskRepository;
    
    @Autowired
    public DataInitializer(TaskRepository taskRepository) {
        this.taskRepository = taskRepository;
    }
    
    @Override
    public void run(String... args) throws Exception {
        // Инициализация тестовых данных
        if (taskRepository.count() == 0) {
            Task task1 = new Task("Изучить Spring Boot", "Изучить основы Spring Boot и REST API");
            Task task2 = new Task("Создать RESTful приложение", "Реализовать CRUD операции для управления задачами");
            Task task3 = new Task("Написать тесты", "Добавить unit и integration тесты");
            task3.setCompleted(true);
            
            taskRepository.save(task1);
            taskRepository.save(task2);
            taskRepository.save(task3);
            
            System.out.println("Тестовые данные инициализированы!");
        }
    }
}

