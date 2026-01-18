# Сборка мобильного приложения (Android APK)

Краткое руководство по сборке Android APK файла.

## Системные требования

- Python 3.8+
- Android SDK (API Level 21+)
- JDK 11+
- Минимум 5 ГБ свободного места

## Установка инструментов

### Android SDK

1. Скачайте и установите Android Studio: https://developer.android.com/studio
2. При установке Android SDK будет установлен автоматически
3. Путь к SDK обычно: `C:\Users\<Имя>\AppData\Local\Android\Sdk` (Windows) или `~/Android/Sdk` (Linux/macOS)

### JDK

1. Скачайте OpenJDK 17: https://adoptium.net/
2. Установите JDK и запомните путь установки

### Переменные окружения

**Windows:**
1. Откройте "Система" → "Переменные среды"
2. Добавьте `ANDROID_HOME` → путь к Android SDK
3. Добавьте `JAVA_HOME` → путь к JDK
4. Добавьте в `PATH`: `%ANDROID_HOME%\platform-tools` и `%JAVA_HOME%\bin`
5. Перезапустите терминал

**Linux/macOS:**
Добавьте в `~/.bashrc` или `~/.zshrc`:
```
export ANDROID_HOME=$HOME/Android/Sdk
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export PATH=$PATH:$ANDROID_HOME/platform-tools:$JAVA_HOME/bin
```
Примените: `source ~/.bashrc`

**Проверка:**
```
echo $ANDROID_HOME  # Linux/macOS
echo %ANDROID_HOME%  # Windows
java -version
```

## Установка зависимостей

```
pip install -r requirements-mobile.txt
```

## Сборка APK

```
python build_mobile.py
```

APK файл будет находиться по пути: `build/android/app/build/outputs/apk/release/app-release.apk`

## Настройка параметров

Отредактируйте `build_mobile.py`, функцию `main()`:
- `project_name` - имя проекта
- `package_name` - Android package name
- `version` - версия приложения
- `android_min_sdk` - минимальный SDK (по умолчанию: 21)

## Иконка приложения

Поместите иконку PNG 1024x1024 в `assets/icon.png`. Если иконка не найдена, используется иконка Flet по умолчанию.

## Установка на устройство

1. Включите "Отладка по USB" на устройстве
2. Подключите устройство через USB
3. Скопируйте APK файл на устройство и установите

Или используйте adb:
```
adb install build/android/app/build/outputs/apk/release/app-release.apk
```

## Решение проблем

- **ANDROID_HOME/JAVA_HOME не найдены**: Проверьте переменные окружения, перезапустите терминал
- **Команда 'flet' не найдена**: Установите `pip install flet flet-builder`
- **Ошибки сборки**: Удалите директорию `build/` и запустите сборку заново
- **Недостаточно места**: Убедитесь, что доступно минимум 5 ГБ
