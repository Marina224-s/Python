def is_year_leap(year):
     
        if year % 4 == 0:
         return True
     
        else:
           return False
      

year_to_check = 2024
result = is_year_leap(year_to_check)
print (f"год {year_to_check}:{result}")


year_to_check = 2023
result = is_year_leap(year_to_check)
print (f"год {year_to_check}:{result}")