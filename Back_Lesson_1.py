class Master:
    def __init__(self, master_id: int):
        self.master_id = master_id


class Service:
    def __init__(self, service_id: int):
        self.service_id = service_id


class Appointment:
    def __init__(
        self,
        appointment_id: int,
        client_name: str,
        master_id: int,
        service_id: int,
        time: str
    ):
        self.appointment_id = appointment_id
        self.client_name = client_name
        self.master_id = master_id
        self.service_id = service_id
        self.time = time


masters = [Master(1)]
services = [Service(1)]
appointments = []


def get_master(master_id: int):
    for master in masters:
        if master.master_id == master_id:
            return master
    return None


def get_service(service_id: int):
    for service in services:
        if service.service_id == service_id:
            return service
    return None


def create_appointment(
    client_name: str,
    master_id: int,
    service_id: int,
    time: str
) -> Appointment | None:

    # Проверяем заполненность полей
    if not client_name or not time or master_id is None or service_id is None:
        return None

    # Проверяем формат и рабочее время
    try:
        hours, minutes = map(int, time.split(":"))

        if not (0 <= hours <= 23 and 0 <= minutes <= 59):
            return None

        appointment_minutes = hours * 60 + minutes
        start_minutes = 8 * 60
        end_minutes = 20 * 60

        if not (start_minutes <= appointment_minutes <= end_minutes):
            return None

    except (ValueError, AttributeError):
        return None

    # Проверяем существование мастера и услуги
    master = get_master(master_id)
    service = get_service(service_id)

    if master is None or service is None:
        return None

    # Создаём объект записи
    appointment = Appointment(
        appointment_id=len(appointments) + 1,
        client_name=client_name,
        master_id=master.master_id,
        service_id=service.service_id,
        time=time
    )

    appointments.append(appointment)
    return appointment


first_appointment = create_appointment("Иванова А.А.", 1, 1, "10:00")
second_appointment = create_appointment("Петрова А.А.", 1, 1, "11:00")

print("Список записей:")

for appointment in appointments:
    print(appointment.client_name, appointment.time)

# пытаемся создать некорректную запись
no_correct_appointment = create_appointment(
    "Сидорова А.А.", 1, 1, "00:00"
)

print(len(appointments))

print("Список записей:")

for appointment in appointments:
    print(appointment.client_name, appointment.time)