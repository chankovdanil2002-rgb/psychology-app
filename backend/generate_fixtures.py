"""
Management-style script: populate the database with 15+ records per table.

Run: cd backend && py generate_fixtures.py
Requires: Django settings and database to be configured.
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
django.setup()

from datetime import date, time, timedelta
from decimal import Decimal
from django.utils import timezone
from apps.users.models import User, EmailConfirmationToken
from apps.clients.models import ClientProfile
from apps.psychologists.models import PsychologistProfile
from apps.specializations.models import PsychologistSpecialization, Specialization
from apps.schedule.models import TimeSlot
from apps.appointments.models import Appointment
from apps.reviews.models import Review
from apps.notifications.models import Notification

PASSWORD = "password123"

# ================================================================
# Disconnect signals to avoid duplicate profiles
# ================================================================
from django.db.models.signals import post_save
from apps.users.signals import create_user_profile
post_save.disconnect(create_user_profile, sender=User)

print("Populating database...")

# ================================================================
# 1. USERS: 16 clients + 16 psychologists = 32
# ================================================================
client_data = [
    "anna.petrova@mail.ru", "dmitry.sokolov@yandex.ru",
    "elena.kozlova@gmail.com", "igor.novikov@mail.ru",
    "maria.fedorova@yandex.ru", "sergey.morozov@gmail.com",
    "olga.volkova@mail.ru", "alexey.lebedev@yandex.ru",
    "natalia.orlova@mail.ru", "pavel.kovalev@yandex.ru",
    "irina.nikolaeva@gmail.com", "roman.andreev@mail.ru",
    "julia.sidorova@yandex.ru", "maksim.egorov@gmail.com",
    "vera.zakharova@mail.ru", "artem.makarov@yandex.ru",
]
psych_data_emails = [
    "dr.ivanova@mail.ru", "dr.smirnov@yandex.ru",
    "dr.kuznetsova@gmail.com", "dr.popov@mail.ru",
    "dr.vasilieva@yandex.ru", "dr.pavlova@gmail.com",
    "dr.semenov@mail.ru", "dr.golubeva@yandex.ru",
    "dr.romanova@mail.ru", "dr.titov@yandex.ru",
    "dr.belova@gmail.com", "dr.korolev@mail.ru",
    "dr.medvedeva@yandex.ru", "dr.voronov@gmail.com",
    "dr.tarasova@mail.ru", "dr.grigoriev@yandex.ru",
]

client_users = []
for email in client_data:
    u, created = User.objects.get_or_create(
        email=email,
        defaults={"role": "client", "is_active": True},
    )
    if created:
        u.set_password(PASSWORD)
        u.save()
    client_users.append(u)
print(f"  Users (clients): {len(client_users)}")

psych_users = []
for email in psych_data_emails:
    u, created = User.objects.get_or_create(
        email=email,
        defaults={"role": "psychologist", "is_active": True},
    )
    if created:
        u.set_password(PASSWORD)
        u.save()
    psych_users.append(u)
print(f"  Users (psychologists): {len(psych_users)}")

# ================================================================
# 2. CLIENT PROFILES (16)
# ================================================================
client_info = [
    ("Анна", "Петрова", "+79161234501", "1995-03-15"),
    ("Дмитрий", "Соколов", "+79161234502", "1990-07-22"),
    ("Елена", "Козлова", "+79161234503", "1988-11-03"),
    ("Игорь", "Новиков", "+79161234504", "1992-01-18"),
    ("Мария", "Фёдорова", "+79161234505", "1997-06-30"),
    ("Сергей", "Морозов", "+79161234506", "1985-09-12"),
    ("Ольга", "Волкова", "+79161234507", "1993-04-25"),
    ("Алексей", "Лебедев", "+79161234508", "1991-12-08"),
    ("Наталья", "Орлова", "+79161234509", "1994-08-11"),
    ("Павел", "Ковалёв", "+79161234510", "1989-02-28"),
    ("Ирина", "Николаева", "+79161234511", "1996-05-19"),
    ("Роман", "Андреев", "+79161234512", "1987-10-07"),
    ("Юлия", "Сидорова", "+79161234513", "1993-12-24"),
    ("Максим", "Егоров", "+79161234514", "1991-07-15"),
    ("Вера", "Захарова", "+79161234515", "1998-01-30"),
    ("Артём", "Макаров", "+79161234516", "1990-04-03"),
]

client_profiles = []
for i, user in enumerate(client_users):
    fn, ln, ph, dob = client_info[i]
    profile, _ = ClientProfile.objects.update_or_create(
        user=user,
        defaults={
            "first_name": fn, "last_name": ln,
            "phone": ph, "date_of_birth": date.fromisoformat(dob),
        },
    )
    client_profiles.append(profile)
print(f"  ClientProfiles: {len(client_profiles)}")

# ================================================================
# 3. PSYCHOLOGIST PROFILES (16)
# ================================================================
psych_info = [
    ("Ирина", "Иванова", "Сергеевна", "+79261234501", 12,
     "МГУ, факультет психологии, 2012",
     "Специализируюсь на когнитивно-поведенческой терапии. Помогаю справиться с тревогой и депрессией.",
     Decimal("4500.00")),
    ("Андрей", "Смирнов", "Викторович", "+79261234502", 8,
     "СПбГУ, клиническая психология, 2016",
     "Работаю с семейными парами и индивидуальными клиентами. Гештальт-подход.",
     Decimal("5000.00")),
    ("Наталья", "Кузнецова", "Александровна", "+79261234503", 15,
     "МГППУ, психотерапия, 2009",
     "Психоаналитик с 15-летним опытом. Глубинная работа с бессознательным.",
     Decimal("6500.00")),
    ("Виктор", "Попов", "Дмитриевич", "+79261234504", 6,
     "НГУ, психология, 2018",
     "Помогаю подросткам и их родителям найти общий язык. Детская психология.",
     Decimal("3500.00")),
    ("Светлана", "Васильева", "Петровна", "+79261234505", 10,
     "КФУ, клиническая психология, 2014",
     "Работаю с зависимостями и расстройствами пищевого поведения.",
     Decimal("5500.00")),
    ("Екатерина", "Павлова", "Игоревна", "+79261234506", 7,
     "ЮФУ, психология, 2017",
     "Арт-терапевт. Использую творческие методы для работы с эмоциями.",
     Decimal("4000.00")),
    ("Михаил", "Семёнов", "Олегович", "+79261234507", 20,
     "МГУ, нейропсихология, 2004",
     "Нейропсихолог. Диагностика и коррекция когнитивных нарушений.",
     Decimal("7000.00")),
    ("Татьяна", "Голубева", "Николаевна", "+79261234508", 9,
     "СФУ, психология, 2015",
     "Специалист по травме и ПТСР. Метод EMDR.",
     Decimal("5000.00")),
    ("Ольга", "Романова", "Владимировна", "+79261234509", 11,
     "РУДН, психология, 2013",
     "Экзистенциальная терапия. Помогаю обрести смысл и направление в жизни.",
     Decimal("5500.00")),
    ("Дмитрий", "Титов", "Андреевич", "+79261234510", 5,
     "ТГУ, клиническая психология, 2019",
     "Работаю с тревожными расстройствами и паническими атаками.",
     Decimal("3000.00")),
    ("Алина", "Белова", "Михайловна", "+79261234511", 14,
     "МГУ, психология личности, 2010",
     "Семейный психолог. Помогаю парам и семьям наладить отношения.",
     Decimal("6000.00")),
    ("Константин", "Королёв", "Сергеевич", "+79261234512", 9,
     "МГППУ, детская психология, 2015",
     "Детский и подростковый психолог. Песочная терапия, игровая терапия.",
     Decimal("4500.00")),
    ("Елена", "Медведева", "Юрьевна", "+79261234513", 16,
     "СПбГУ, психиатрия, 2008",
     "Клинический психолог. Работаю с депрессией и биполярным расстройством.",
     Decimal("7500.00")),
    ("Игорь", "Воронов", "Александрович", "+79261234514", 7,
     "НГУ, психология, 2017",
     "Коуч и психолог. Помогаю с целеполаганием и преодолением прокрастинации.",
     Decimal("4000.00")),
    ("Марина", "Тарасова", "Дмитриевна", "+79261234515", 12,
     "КФУ, сексология, 2012",
     "Психолог-сексолог. Деликатный подход к интимным вопросам.",
     Decimal("6000.00")),
    ("Александр", "Григорьев", "Петрович", "+79261234516", 18,
     "МГУ, нейропсихология, 2006",
     "Нейропсихолог высшей категории. Работаю со сложными случаями.",
     Decimal("8000.00")),
]

psych_profiles = []
verified_at = timezone.now() - timedelta(days=30)
for i, user in enumerate(psych_users):
    fn, ln, pat, ph, exp, edu, bio, price = psych_info[i]
    profile, _ = PsychologistProfile.objects.update_or_create(
        user=user,
        defaults={
            "first_name": fn, "last_name": ln, "patronymic": pat,
            "phone": ph, "experience_years": exp, "education": edu,
            "bio": bio, "price": price,
            "is_verified": True, "verified_at": verified_at,
        },
    )
    psych_profiles.append(profile)
print(f"  PsychologistProfiles: {len(psych_profiles)}")

# ================================================================
# 4. PSYCHOLOGIST SPECIALIZATIONS (33)
# ================================================================
PsychologistSpecialization.objects.filter(
    psychologist__in=psych_profiles
).delete()

# Spec IDs: 1=Арт, 2=Гештальт, 3=Депрессия, 4=Детская, 5=Зависимости,
# 6=КПТ, 7=Нейро, 8=Психоанализ, 9=Психосоматика, 10=РПП,
# 11=Сексология, 12=Семейная, 13=Стресс, 14=Травма, 15=Тревожные
spec_map = {
    0: [(6, True), (15, False), (3, False)],
    1: [(2, True), (12, False)],
    2: [(8, True), (9, False), (3, False)],
    3: [(4, True), (12, False)],
    4: [(5, True), (10, False), (15, False)],
    5: [(1, True), (13, False)],
    6: [(7, True), (9, False)],
    7: [(14, True), (13, False), (15, False)],
    8: [(8, True), (13, False)],
    9: [(6, True), (15, False)],
    10: [(12, True), (2, False)],
    11: [(4, True)],
    12: [(3, True), (6, False)],
    13: [(13, True)],
    14: [(11, True)],
    15: [(7, True), (9, False)],
}

spec_count = 0
for idx, profile in enumerate(psych_profiles):
    for spec_id, is_primary in spec_map[idx]:
        PsychologistSpecialization.objects.get_or_create(
            psychologist=profile,
            specialization_id=spec_id,
            defaults={"is_primary": is_primary},
        )
        spec_count += 1
print(f"  PsychologistSpecializations: {spec_count}")

# ================================================================
# 5. TIME SLOTS (48+)
# ================================================================
TimeSlot.objects.filter(psychologist__in=psych_profiles).delete()

slots = []
hours = [
    (time(10, 0), time(11, 0)),
    (time(12, 0), time(13, 0)),
    (time(14, 0), time(15, 0)),
    (time(16, 0), time(17, 0)),
]

for idx, profile in enumerate(psych_profiles):
    base_day = 20 + (idx % 5)
    for day_off in range(3):
        d = date(2026, 4, base_day + day_off)
        st, et = hours[idx % 4]
        slot = TimeSlot.objects.create(
            psychologist=profile, date=d,
            start_time=st, end_time=et,
            is_available=True,
        )
        slots.append(slot)

# Additional past slots for completed appointments
for idx in range(16):
    profile = psych_profiles[idx % len(psych_profiles)]
    d = date(2026, 3, 1 + idx)
    slot = TimeSlot.objects.create(
        psychologist=profile, date=d,
        start_time=time(10, 0), end_time=time(11, 0),
        is_available=False,
    )
    slots.append(slot)

print(f"  TimeSlots: {len(slots)}")

# ================================================================
# 6. APPOINTMENTS (20)
# ================================================================
Appointment.objects.filter(client__in=client_profiles).delete()

statuses = (
    ["completed"] * 8
    + ["confirmed"] * 4
    + ["pending"] * 4
    + ["rejected"] * 2
    + ["cancelled"] * 2
)
comments = [
    "Хочу обсудить тревожность", "Проблемы в отношениях",
    "Не могу справиться со стрессом", "Панические атаки",
    "Проблемы с самооценкой", "Хочу разобраться в себе",
    "Сложности на работе", "Проблемы со сном",
    "Нужна поддержка", "Конфликты в семье",
    "Выгорание на работе", "Потеря мотивации",
    "Тревога перед экзаменами", "Проблемы с едой",
    "Пережил утрату", "Хочу начать терапию",
    "Нужна помощь с зависимостью", "Проблемы в общении",
    "Хочу улучшить самооценку", "Консультация по детской психологии",
]

appointments = []
# Use past slots (index 48+) for completed, future for rest
for i in range(20):
    client_p = client_profiles[i % len(client_profiles)]
    psych_p = psych_profiles[(i + 3) % len(psych_profiles)]

    if i < 8:
        # Completed: use past slots
        slot = slots[48 + i]
    else:
        # Others: use future slots
        slot = slots[i - 8]

    slot.is_available = False
    slot.save()

    appt = Appointment.objects.create(
        client=client_p, psychologist=psych_p,
        time_slot=slot, status=statuses[i],
        comment=comments[i],
    )
    appointments.append(appt)
print(f"  Appointments: {len(appointments)}")

# ================================================================
# 7. REVIEWS (15, for completed appointments only)
# ================================================================
review_texts = [
    "Отличный специалист! Помогла разобраться в моих проблемах. Рекомендую всем.",
    "Очень внимательный психолог, чувствуется профессионализм. Стало легче после первого сеанса.",
    "Прекрасный опыт. Наталья Александровна нашла подход и помогла увидеть ситуацию по-новому.",
    "Хороший психолог, но хотелось бы более конкретных рекомендаций. В целом доволен.",
    "Замечательный специалист! Работает мягко, но эффективно. Результат заметен.",
    "Профессиональный подход, комфортная атмосфера. Буду продолжать терапию.",
    "Очень помогли сессии. Научился справляться с тревогой самостоятельно.",
    "Рекомендую! Светлана Петровна — настоящий профессионал своего дела.",
    "Благодарна за помощь. Арт-терапия оказалась именно тем, что мне было нужно.",
    "Отличная работа! Помог разобраться с когнитивными проблемами.",
    "Спасибо за поддержку в трудный период. Чувствую себя гораздо лучше.",
    "Профессионально и по существу. Доволен результатом терапии.",
    "Хорошие сессии, но иногда не хватало времени. В целом положительный опыт.",
    "Замечательный специалист по травме. Очень помогла.",
    "Прекрасный психолог. Чуткий, внимательный, профессиональный подход.",
]
ratings = [5, 5, 5, 4, 5, 4, 5, 5, 5, 4, 5, 4, 3, 5, 5]

completed = [a for a in appointments if a.status == "completed"]
reviews = []
for i, appt in enumerate(completed[:15]):
    r, _ = Review.objects.get_or_create(
        appointment=appt,
        defaults={"rating": ratings[i], "text": review_texts[i]},
    )
    reviews.append(r)
print(f"  Reviews: {len(reviews)}")

# ================================================================
# 8. NOTIFICATIONS (16)
# ================================================================
all_users_list = client_users + psych_users
notif_data = [
    (client_users[0], "appointment_confirmed", "Запись подтверждена",
     "Ваша запись к психологу Ивановой И.С. подтверждена на 20 апреля в 10:00."),
    (client_users[1], "appointment_confirmed", "Запись подтверждена",
     "Ваша запись к психологу Смирнову А.В. подтверждена на 21 апреля в 12:00."),
    (client_users[2], "appointment_completed", "Сеанс завершён",
     "Ваш сеанс с психологом Кузнецовой Н.А. завершён. Спасибо!"),
    (client_users[3], "review_request", "Оставьте отзыв",
     "Пожалуйста, оставьте отзыв о сеансе с Поповым В.Д."),
    (client_users[4], "appointment_rejected", "Запись отклонена",
     "К сожалению, ваша запись на 22 апреля была отклонена."),
    (client_users[5], "appointment_cancelled", "Запись отменена",
     "Ваша запись на 23 апреля была отменена."),
    (client_users[6], "review_request", "Оставьте отзыв",
     "Пожалуйста, оцените прошедший сеанс."),
    (client_users[7], "appointment_confirmed", "Запись подтверждена",
     "Ваша запись подтверждена. Ждём вас!"),
    (psych_users[0], "verification_approved", "Верификация пройдена",
     "Ваш профиль верифицирован. Теперь вы видны в каталоге."),
    (psych_users[1], "verification_approved", "Верификация пройдена",
     "Поздравляем! Ваш профиль психолога подтверждён."),
    (psych_users[2], "system", "Добро пожаловать",
     "Добро пожаловать на платформу Психолог Онлайн!"),
    (psych_users[3], "system", "Новая запись",
     "К вам записался новый клиент. Проверьте раздел Записи."),
    (psych_users[4], "system", "Напоминание",
     "Напоминаем о предстоящем сеансе завтра в 10:00."),
    (psych_users[5], "verification_approved", "Верификация пройдена",
     "Ваш профиль успешно верифицирован."),
    (psych_users[6], "system", "Новый отзыв",
     "Вам оставили новый отзыв. Средний рейтинг: 4.8."),
    (psych_users[7], "system", "Обновление платформы",
     "На платформе появились новые функции."),
]

notifs = []
for user, ntype, title, msg in notif_data:
    n = Notification.objects.create(
        user=user, type=ntype, title=title,
        message=msg, is_read=False,
    )
    notifs.append(n)
print(f"  Notifications: {len(notifs)}")

# ================================================================
# 9. EMAIL CONFIRMATION TOKENS (32)
# ================================================================
for user in client_users + psych_users:
    EmailConfirmationToken.objects.get_or_create(
        user=user,
        defaults={
            "is_used": True,
            "expires_at": timezone.now() + timedelta(days=30),
        },
    )
print(f"  EmailConfirmationTokens: {len(client_users) + len(psych_users)}")

# Reconnect signal
post_save.connect(create_user_profile, sender=User)

print("\n=== Done! Database populated successfully. ===")

# Summary
print(f"\nSummary:")
print(f"  Users:              {User.objects.count()}")
print(f"  ClientProfiles:     {ClientProfile.objects.count()}")
print(f"  PsychologistProfiles: {PsychologistProfile.objects.count()}")
print(f"  Specializations:    {Specialization.objects.count()}")
print(f"  PsychSpecializations: {PsychologistSpecialization.objects.count()}")
print(f"  TimeSlots:          {TimeSlot.objects.count()}")
print(f"  Appointments:       {Appointment.objects.count()}")
print(f"  Reviews:            {Review.objects.count()}")
print(f"  Notifications:      {Notification.objects.count()}")
print(f"  EmailTokens:        {EmailConfirmationToken.objects.count()}")
