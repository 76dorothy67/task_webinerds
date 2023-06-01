# Тестове завдання webinerds

Чат бот на базі OpenAI з постійною пам'яттю.   


# Інсталяція (Windows)


```bash
git clone https://github.com/76dorothy67/task_webinerds.git
cd task_webinerds
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
notepad .env
```
OpenAI API Key можна задати в файлі .env (див. .env.example), або змінною оточення OPENAI_API_KEY, або передати в програму параметром --api-key

Текож, для роботи програми, необхідні права на запис task_webinerds (в середині буде створено папку program_data)

Перевірено з використанням Python v3.10.7

# Використання

```bash
python program.py
```

## Аргументи командної строки

* -k *key*, --api-key *key* Дозволяє задачи OpenAI API Key, якщо не вказано в .env файлі чи змінних оточення ОС 
* -v --verbose Відображати інформацію для відлагодження
* -t *float*, --temperature *float* Задати параметр моделі temperature
* -h, --help Допомога

# Принцип дії

![Schema](https://i.gyazo.com/9cfbf2b6e0437d55f38f6f4e6a553a04.png)

# Контакти

[zozulinadarina97@gmail.com](mailto:zozulinadarina97@gmail.com)
