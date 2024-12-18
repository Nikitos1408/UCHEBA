# Задание 3 - Сборка игры в исполняемый файл (выполнил: Угарин Н.А)

## 1)Надо протестировать игру на работоспособность

## 2)Правильно структурировать файлы

├── main.py\
├── resources/\
│ ├── image.png\
│ └── sound.wav\
└── ...\

## 3)Запустить данную консольную команду и дождаться ее выполнения
```
pyinstaller --onefile --windowed alien_invasion.py --add-data "sounds;sounds" --add-data "images;images"
```

![image](https://github.com/user-attachments/assets/1a5370bc-7f10-4f98-a9c2-ca24e6e61019)

## 4)Можно открывать exe-файл игры в папке Dist и играть

![image](https://github.com/user-attachments/assets/9f4ea896-0741-4795-a877-22059c12a889)
