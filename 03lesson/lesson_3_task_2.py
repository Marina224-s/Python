from smartphone import smartphone

catalog = [
    smartphone("IPhone","16Pro", "+79205672345"),
    smartphone("Samsung", "S24", "+79190151122"),
    smartphone("Xiaomi", "Mi14TPro","+79106151133"),
    smartphone("Nokia","3310","+79208905674"),
    smartphone("Huawei","Y3","+79453452134")

]

for smartphone in catalog:
    print(f"{smartphone.brand}{smartphone.model}{smartphone.namber}")
