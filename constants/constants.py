BUTTONS = {"upload": "📱 Отправить номер", "order": "📦 Мои заказы"}

MESSAGES = {
    "start": "Здравствуйте, {name}! \n Я бот отслежтивающий ваши заказы! Посмотреть их статусы вы можете нажатием на кнопку!",
    "phone_request": "Предоставьте ваш номер телефона, чтобы я мог найти ваши заказы!",
    "save_phone": "Ваш номер сохранен",
    "no_orders": "❌ Нет заказов",
    "order": (
        "Заказ #{order_id} - {title}\n Статус - {status}"
        "\n Что делаем - {description}"
        "\n Ожидаемая дата готовности {expectation_date}"
    ),
    "ready": "Для просмотра ваших заказов нажмите на кнопку!",
}


ADMIN_MESSAGES = {
    "welcome": "Добро пожаловать в панель мастера",
    "start": (
        "Выберите действие"
        "\n🔐 - Добавить мастера"
        "\n📋 - Работа с заказами"
        "\n🛠️ - Изменить данные мастеров"
    ),
    # admin creation
    "admin_telegram_username": "Введите ник в телеграм администратора",
    "admin_username": "Введите имя мастера",
    "admin_phone": "Введите номер телефона",
    "save_admin_username": "Хорошо, я запомнил имя {username}",
    "wrong_number": "Неправиьлный номер телефона, введите повторно",
    "rename_admin_telegram": "Поменял имя на - {telegram_username}",
    "rename_admin": "Поменял имя на - {username}",
    "create_admin": (
        "Добавляю нового админа?"
        "\nИмя - {username} \nТелефон - {phone}"
        "\n✏️ - Исправить данные"
        "\n✅ Создать мастера"
    ),
    "admin_exists": "Мастер с таким именем уже существует, введите другое имя",
    "admin_creation_failed": "Что-то пошло не так",
    "admin_created": "✅ Мастер добавлен",
    "edit_choose": "Что редактируем? \n👤 - Изменить имя\n📞 - Изменить номер",
    # admin edit
    "edit_admins": "Изменить мастеров",
    "choose_admin": "👀 Выберите мастера\n\n",
    "view_admin": "👤 {admin_id}. *{username}*\n📞 {phone}\n\n",
    "admin_retrieve": "Выбран мастер\n👤 *{username}*\n📞 {phone}\n Что будем менять?\n",
    "no_admins": "Список мастеров пуст",
    "not_id": "🚫 Это не ID\nВыберите id",
    "no_such_admin": "Нет такого мастера",
    "empty_username": "🚫 Имя не может быть пустым\nВведите имя заново",
    "confirm_changes": (
        "Сохраняю новые данные?"
        "\nИмя - {username} \nТелефон - {phone}"
        "\n✏️ - Исправить данные"
        "\n✅ Создать мастера"
    ),
    "admin_updated": "Данные мастера обновлены",
    "remove_admin": (
        "Удалить мастера?"
        "\n👤 *{username}*"
        "\n📞 {phone}\n Что будем менять?"
        "\n Нажмите 💀 для удаления мастера"
    ),
    "removed_admin": "мастер удален",
    # orders
    "order_start": (
        "Вы в панели управления заказами"
        "\nВыберите действие"
        "\n📥 - Создать заказ"
        "\n✏️ - Редактировать заказ"
        "\n🔍 - Поиск заказа"
    ),
    "create_order": "Введите наименование заказа",
    "order_title": "Запомнил название:\n{title}",
    "create_description": "Введите описание заказа",
    "order_description": "Запомнил описание\n{description}",
    "create_model_type": "Введите модель велосипеда",
    "order_model_type": "Запомнил модель:\n{model_type}",
    "create_price_estimate": "Введите стоимость заказа\n(пример ввода - '5055.5')",
    "wrong_order_price": "Вы ввели неправильную цену, введите заново\n(пример ввода - '5055.5')",
    "order_price_estimate": "Запомнил стоимость заказа\n💰 {price_estimate}",
    "create_is_paid": "Заказ был оплачен?",
    "no_is_paid": "🚫 Нет такого варианта\nЗаказ оплачен?",
    "order_is_paid_true": "Запомнил, заказ оплачен",
    "order_is_paid_false": "Запомнил, заказ не оплачен",
    "create_fullname": "Введите имя клиента",
    "no_fullname": "Неправильное имя! Введите имя еще раз",
    "order_fullname": "Запомнил имя клиента\n{fullname}",
    "create_order_phone": "Введите телефон заказчика",
    "order_phone": "Запомнил номер телефона \n{phone}",
    "create_master": "Введите имя мастера, выполняющего заказ",
    "view_master": "👤 {admin_id}. *{username}*\n\n",
    "no_master": "Неправильнре имя мастера! Введите имя еще раз",
    "order_master_error": "Не удалось найти мастера из администраторов, выберете заново",
    "order_master_mismatch": "Нашел мастера из администраторов",
    "order_master": "Запомнил имя мастера\n{master}",
    "create_comment": "Заполните комментарий к заказу, если он есть",
    "order_comment": "Запомнил комментарий\n{comment}",
    "order_info": (
        "Вы создали заказ:"
        "\n🏷️ Название: *{title}*"
        "\n📝 Описание: *{description}*"
        "\n🚲 Модель велосипеда: *{model_type}*"
        "\n💰 Стоимость заказа: *{price_estimate}₽*"
        "\n💳 Статус оплаты: *{is_paid}*"
        "\n👤 Имя клиента: *{fullname}*"
        "\n📞 Телефон клиента: *{phone}*"
        "\n🧑‍🔧 Мастер: *{master}*"
        "\n💬 Комментарий: *{comment}*"
        "\n\n*Создаем заказ?*"
    ),
    "order_confirm": "Создал заказ с номером  *{order_id}*!",
    "order_creation_failed": "Создать заказ не удалось",
    "choose_edit": (
        "\n\nЧто будем редактировать?"
        "\n🏷️ - Изменить название"
        "\n📝 - Изменить описание"
        "\n🚲 - Изменить модель"
        "\n💰 - Изменить стоимость"
        "\n💳 - Изменить статус оплаты"
        "\n👤 - Изменить имя клиента"
        "\n📞 - Изменить номер клиента"
        "\n🧑‍🔧 - Изменить мастера"
        "\n💬 - Изменить комментарий"
    ),
    # edit order
    "order_find": (
        "Для выберите как будем искать заказ:"
        "\n📌 - Поиск по Номеру заказа"
        "\n📞 - Поиск по Телефону клиента"
        "\n🧑‍🔧 - Поиск по Мастеру"
    ),
    "order_id_input": "Введите номер заказа",
    "no_order_id": "Введен некорректный номер, повторите ввод",
    "wrong_order": "Введен неправильный номер заказа",
    "order": (
        "📌 Номер заказа *{order_id}*:"
        "\n🏷️ Название: *{title}*"
        "\n📝 Описание: *{description}*"
        "\n🚲 Модель велосипеда: *{model_type}*"
        "\n💰 Стоимость заказа: *{price_estimate}₽*"
        "\n💳 Статус оплаты: *{is_paid}*"
        "\n👤 Имя клиента: *{fullname}*"
        "\n📞 Телефон клиента: *{phone}*"
        "\n🧑‍🔧 Мастер: *{master}*"
        "\n💬 Комментарий: *{comment}*"
    ),
    "empty_orders": "У мастера нет активных заказов",
    "by_master_error": "Что-то пошло не так",
    "choose_order": "👀 Выберите заказ\n\n",
    "view_order": (
        "Заказ - *{order_number}.*"
        "\n📌 Номер заказа - *{order_id}*:"
        "\n🏷️ Название: *{title}*"
        "\n🚲 Модель велосипеда: *{model_type}*"
        "\n🧑‍🔧 Мастер: *{master}*"
        "\n👤 Имя клиента: *{fullname}*"
        "\n📞 Телефон клиента: *{phone}*\n\n"
    ),
    "new_title": "Введите новое название",
    "new_description": "Введите новое описание",
    "new_model_type": "Введите новую модель велосипеда",
    "new_price_estimate": "Введите новую стоимость заказа",
    "new_is_paid": "Введите новый статус оплаты\n",
    "new_fullname": "Введите новое имя клиента",
    "new_phone": "Введите новый телефон клиента",
    "new_master": "new_master",
    "new_comment": "Введите новый комментарий",
    "no_edit_field": "Ошибка ввода",
    "edited_field": "Изменил поле",
    "empty_edited_field": "Введите значение заново",
    "edit_order_error": "Что-то пошло не так",
    "edit_order_success": "✅ Заказ изменен",
    # photo edit
    "photo_start": "Фотографии заказа",
}
ADMIN_BUTTONS = {
    "add_admin": "🔐",
    "edit_admins": "🛠️",
    "orders": "📋",
    "create_admin": "✅",
    "edit_admin": "✏️",
    "edit_username": "👤",
    "edit_phone": "📞",
    "cancel": "❌ В меню",
    "back_to_admins": "↩️ Назад к админам",
    "remove_admin": "💀",
    # orders
    "create_order": "📥",
    "edit_order": "✏️",
    "find_order": "🔍",
    "back_to_orders": "↩️ Назад в меню заказов",
    "is_paid_true": "Да",
    "is_paid_false": "Нет",
    "confirm_order": "✅",
    "order_edit_title": "🏷️",
    "order_edit_description": "📝",
    "order_edit_model_type": "🚲",
    "order_edit_price_estimate": "💰",
    "order_edit_is_paid": "💳",
    "order_edit_fullname": "👤",
    "order_edit_phone": "📞",
    "order_edit_master": "🧑‍🔧",
    "order_edit_comment": "💬",
    # edit orders
    "find_phone": "📞",
    "find_order_id": "📌",
    "find_master": "🧑‍🔧",
    "order_edit_photo": "📸 Фото заказа",
    # photo edit
    "new_photo": "📸 обновить фото",
    "delete_photo": "🗑️ удалить фото",
}


LOGGER = {"clear_state": "Состояние {current_state} прервано]"}

NUMBERS = {
    1: "1️⃣",
    2: "2️⃣",
    3: "3️⃣",
    4: "4️⃣",
    5: "5️⃣",
    6: "6️⃣",
    7: "7️⃣",
    8: "8️⃣",
    9: "9️⃣",
    10: "🔟",
}
