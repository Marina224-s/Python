from Address import Address
from Mailing import Mailing

# Создаем адреса
from_addr = Address("123456", "Москва", "Ленина", "10", "5")
to_addr = Address("654321", "Санкт-Петербург", "Пушкина", "20", "15")

# Создаем отправление
mail = Mailing(to_address=to_addr, from_address=from_addr, cost=350.75, track="AB123456789RU")

# Формируем и выводим строку
print(f"Отправление {mail.track} из {mail.from_address.index}, {mail.from_address.city}, {mail.from_address.street}, "
      f"{mail.from_address.house} - {mail.from_address.apartment} в {mail.to_address.index}, {mail.to_address.city}, "
      f"{mail.to_address.street}, {mail.to_address.house} - {mail.to_address.apartment}. "
      f"Стоимость {mail.cost} рублей.")