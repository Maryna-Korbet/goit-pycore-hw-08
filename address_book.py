from collections import UserDict
from record import Record

from datetime import datetime, timedelta
from fields import DATE_FORMAT

class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.last_id = 0

    def add_record(self, record: Record) -> None:
        self.last_id += 1
        self.data[self.last_id] = record
    
    def find(self, name: str) -> Record | None:
        for record in self.data.values():
            if record.name.value == name:
                return record
        return None

    def delete(self, name: str):
        key = next((key for key in self.data.keys() if self.data[key].name.value == name), None)
        if key is None:
            print(f"Record with name {name} not found in contacts")
            return
        del self.data[key]
        print(f"Record {name} successfully deleted")

    def get_upcoming_birthdays(self):
        result = []
        current_date = datetime.today()
        current_year = current_date.year

        for record in self.data.values():
            if not record.birthday:
                continue

            # Замінюємо рік народження на поточний рік
            birthdate = record.birthday.value.replace(year=current_year)
            if birthdate < current_date:
                birthdate = birthdate.replace(year=current_year + 1)

            days_until_birthday = (birthdate - current_date).days
            if days_until_birthday <= 7:
                congratulation_date = birthdate
                if congratulation_date.weekday() in [5, 6]: 
                    congratulation_date += timedelta(days=(7 - congratulation_date.weekday()))

                result.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime(DATE_FORMAT) 
                })

            return result  