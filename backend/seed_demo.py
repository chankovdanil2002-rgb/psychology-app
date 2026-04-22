import os
import sys
from datetime import date, time, timedelta
from decimal import Decimal

import django


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CURRENT_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
django.setup()

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.utils import timezone

from apps.appointments.models import Appointment
from apps.clients.models import ClientProfile
from apps.psychologists.models import PsychologistProfile
from apps.reviews.models import Review
from apps.schedule.models import TimeSlot
from apps.specializations.models import (
    PsychologistSpecialization,
    Specialization,
)
from apps.users.models import EmailConfirmationToken
from apps.users.signals import create_user_profile


User = get_user_model()

DEFAULT_PASSWORD = "Password123!"
ADMIN_EMAIL = "admin@young-psy.ru"

SPECIALIZATIONS = [
    ("individual-consulting", "Individual Consulting"),
    ("anxiety-support", "Anxiety Support"),
    ("stress-management", "Stress Management"),
    ("family-therapy", "Family Therapy"),
    ("student-adaptation", "Student Adaptation"),
    ("self-esteem", "Self-Esteem"),
    ("career-guidance", "Career Guidance"),
    ("burnout-recovery", "Burnout Recovery"),
    ("relationship-issues", "Relationship Issues"),
    ("crisis-support", "Crisis Support"),
    ("grief-support", "Grief Support"),
    ("teen-support", "Teen Support"),
    ("cbt", "CBT"),
    ("art-therapy", "Art Therapy"),
    ("trauma-support", "Trauma Support"),
]

PSYCHOLOGISTS = [
    {
        "email": "a.ivanova@young-psy.ru",
        "first_name": "Alina",
        "last_name": "Ivanova",
        "patronymic": "Sergeevna",
        "phone": "+79001000001",
        "experience_years": 3,
        "education": "Institute of Practical Psychology, 2023",
        "bio": "Works with anxiety, adaptation, and self-esteem questions.",
        "price": Decimal("2500.00"),
    },
    {
        "email": "m.smirnov@young-psy.ru",
        "first_name": "Maksim",
        "last_name": "Smirnov",
        "patronymic": "Andreevich",
        "phone": "+79001000002",
        "experience_years": 4,
        "education": "Institute of Practical Psychology, 2022",
        "bio": "Focuses on burnout, motivation, and student stress.",
        "price": Decimal("2600.00"),
    },
    {
        "email": "e.kozlova@young-psy.ru",
        "first_name": "Elena",
        "last_name": "Kozlova",
        "patronymic": "Igorevna",
        "phone": "+79001000003",
        "experience_years": 2,
        "education": "Institute of Practical Psychology, 2024",
        "bio": "Supports young adults in relationships and personal growth.",
        "price": Decimal("2400.00"),
    },
    {
        "email": "d.novikov@young-psy.ru",
        "first_name": "Daniil",
        "last_name": "Novikov",
        "patronymic": "Olegovich",
        "phone": "+79001000004",
        "experience_years": 5,
        "education": "Institute of Clinical Psychology, 2021",
        "bio": "Works with trauma, crisis situations, and adaptation.",
        "price": Decimal("2800.00"),
    },
    {
        "email": "v.fedorova@young-psy.ru",
        "first_name": "Vera",
        "last_name": "Fedorova",
        "patronymic": "Petrovna",
        "phone": "+79001000005",
        "experience_years": 3,
        "education": "Institute of Practical Psychology, 2023",
        "bio": "Helps with self-esteem and difficult life periods.",
        "price": Decimal("2550.00"),
    },
    {
        "email": "i.morozov@young-psy.ru",
        "first_name": "Ilya",
        "last_name": "Morozov",
        "patronymic": "Vladimirovich",
        "phone": "+79001000006",
        "experience_years": 4,
        "education": "Institute of Social Psychology, 2022",
        "bio": "Specializes in communication, boundaries, and conflict work.",
        "price": Decimal("2650.00"),
    },
    {
        "email": "k.volkova@young-psy.ru",
        "first_name": "Ksenia",
        "last_name": "Volkova",
        "patronymic": "Romanovna",
        "phone": "+79001000007",
        "experience_years": 3,
        "education": "Institute of Practical Psychology, 2023",
        "bio": "Uses a supportive, structured approach for student clients.",
        "price": Decimal("2500.00"),
    },
    {
        "email": "r.lebedev@young-psy.ru",
        "first_name": "Roman",
        "last_name": "Lebedev",
        "patronymic": "Dmitrievich",
        "phone": "+79001000008",
        "experience_years": 5,
        "education": "Institute of Clinical Psychology, 2021",
        "bio": "Works with anxiety, panic symptoms, and burnout.",
        "price": Decimal("2850.00"),
    },
    {
        "email": "o.orlova@young-psy.ru",
        "first_name": "Olga",
        "last_name": "Orlova",
        "patronymic": "Nikolaevna",
        "phone": "+79001000009",
        "experience_years": 2,
        "education": "Institute of Practical Psychology, 2024",
        "bio": "Supports students around exams and adaptation to change.",
        "price": Decimal("2350.00"),
    },
    {
        "email": "p.kovalev@young-psy.ru",
        "first_name": "Pavel",
        "last_name": "Kovalev",
        "patronymic": "Sergeevich",
        "phone": "+79001000010",
        "experience_years": 4,
        "education": "Institute of Practical Psychology, 2022",
        "bio": "Focuses on relationships and emotional regulation.",
        "price": Decimal("2700.00"),
    },
    {
        "email": "n.nikolaeva@young-psy.ru",
        "first_name": "Natalia",
        "last_name": "Nikolaeva",
        "patronymic": "Alekseevna",
        "phone": "+79001000011",
        "experience_years": 3,
        "education": "Institute of Practical Psychology, 2023",
        "bio": "Works with grief, loss, and inner stability.",
        "price": Decimal("2500.00"),
    },
    {
        "email": "a.andreev@young-psy.ru",
        "first_name": "Artem",
        "last_name": "Andreev",
        "patronymic": "Igorevich",
        "phone": "+79001000012",
        "experience_years": 4,
        "education": "Institute of Social Psychology, 2022",
        "bio": "Supports clients with communication and confidence issues.",
        "price": Decimal("2600.00"),
    },
    {
        "email": "y.sidorova@young-psy.ru",
        "first_name": "Yulia",
        "last_name": "Sidorova",
        "patronymic": "Olegovna",
        "phone": "+79001000013",
        "experience_years": 2,
        "education": "Institute of Practical Psychology, 2024",
        "bio": "Uses a warm approach for personal growth and reflection.",
        "price": Decimal("2300.00"),
    },
    {
        "email": "m.egorov@young-psy.ru",
        "first_name": "Mikhail",
        "last_name": "Egorov",
        "patronymic": "Petrovich",
        "phone": "+79001000014",
        "experience_years": 5,
        "education": "Institute of Clinical Psychology, 2021",
        "bio": "Works with stress recovery and crisis adaptation.",
        "price": Decimal("2800.00"),
    },
    {
        "email": "s.makarova@young-psy.ru",
        "first_name": "Sofia",
        "last_name": "Makarova",
        "patronymic": "Romanovna",
        "phone": "+79001000015",
        "experience_years": 3,
        "education": "Institute of Practical Psychology, 2023",
        "bio": "Helps with boundaries, relationships, and self-support.",
        "price": Decimal("2550.00"),
    },
]

CLIENTS = [
    {"email": "client01@young-psy.ru", "first_name": "Anna", "last_name": "Petrova", "phone": "+79002000001", "date_of_birth": date(2004, 1, 10)},
    {"email": "client02@young-psy.ru", "first_name": "Dmitry", "last_name": "Sokolov", "phone": "+79002000002", "date_of_birth": date(2003, 2, 11)},
    {"email": "client03@young-psy.ru", "first_name": "Elena", "last_name": "Kuzmina", "phone": "+79002000003", "date_of_birth": date(2004, 3, 12)},
    {"email": "client04@young-psy.ru", "first_name": "Igor", "last_name": "Popov", "phone": "+79002000004", "date_of_birth": date(2005, 4, 13)},
    {"email": "client05@young-psy.ru", "first_name": "Maria", "last_name": "Volkova", "phone": "+79002000005", "date_of_birth": date(2003, 5, 14)},
    {"email": "client06@young-psy.ru", "first_name": "Sergey", "last_name": "Lebedev", "phone": "+79002000006", "date_of_birth": date(2004, 6, 15)},
    {"email": "client07@young-psy.ru", "first_name": "Olga", "last_name": "Smolina", "phone": "+79002000007", "date_of_birth": date(2002, 7, 16)},
    {"email": "client08@young-psy.ru", "first_name": "Alexey", "last_name": "Gromov", "phone": "+79002000008", "date_of_birth": date(2003, 8, 17)},
    {"email": "client09@young-psy.ru", "first_name": "Natalia", "last_name": "Mironova", "phone": "+79002000009", "date_of_birth": date(2004, 9, 18)},
    {"email": "client10@young-psy.ru", "first_name": "Pavel", "last_name": "Denisov", "phone": "+79002000010", "date_of_birth": date(2005, 10, 19)},
    {"email": "client11@young-psy.ru", "first_name": "Irina", "last_name": "Belova", "phone": "+79002000011", "date_of_birth": date(2003, 11, 20)},
    {"email": "client12@young-psy.ru", "first_name": "Roman", "last_name": "Kiselev", "phone": "+79002000012", "date_of_birth": date(2004, 12, 21)},
    {"email": "client13@young-psy.ru", "first_name": "Yana", "last_name": "Zaitseva", "phone": "+79002000013", "date_of_birth": date(2002, 1, 22)},
    {"email": "client14@young-psy.ru", "first_name": "Kirill", "last_name": "Sorokin", "phone": "+79002000014", "date_of_birth": date(2005, 2, 23)},
    {"email": "client15@young-psy.ru", "first_name": "Vera", "last_name": "Tarasova", "phone": "+79002000015", "date_of_birth": date(2003, 3, 24)},
]

APPOINTMENT_COMMENTS = [
    "Need support with exam stress.",
    "Want to discuss anxiety and sleep.",
    "Looking for help with adaptation to studies.",
    "Need support after a breakup.",
    "Burnout and loss of motivation.",
    "Hard to manage emotions lately.",
    "Want to work on self-esteem.",
    "Need help with family pressure.",
    "Difficulties with concentration.",
    "Relationship conflict and boundaries.",
    "Feeling lonely and anxious.",
    "Need support after relocation.",
    "Trouble balancing study and work.",
    "Want to reduce panic symptoms.",
    "Need guidance during a crisis period.",
]

REVIEW_TEXTS = [
    "The session was calm and helpful.",
    "I felt heard and understood.",
    "The specialist explained things clearly.",
    "It became easier after the first meeting.",
    "Very supportive and professional.",
    "Helpful conversation with practical steps.",
    "Warm approach and good structure.",
    "I would continue working with this psychologist.",
    "The consultation helped me look at the problem differently.",
    "Good specialist for student-related stress.",
    "I liked the respectful and careful tone.",
    "The meeting gave me more confidence.",
    "Useful support in a difficult moment.",
    "Clear, calm, and very attentive work.",
    "The consultation met my expectations.",
]


def create_or_update_admin():
    admin, created = User.objects.get_or_create(
        email=ADMIN_EMAIL,
        defaults={
            "role": User.Role.ADMIN,
            "is_active": True,
            "is_staff": True,
            "is_superuser": True,
        },
    )
    changed = False

    if admin.role != User.Role.ADMIN:
        admin.role = User.Role.ADMIN
        changed = True
    if not admin.is_active:
        admin.is_active = True
        changed = True
    if not admin.is_staff:
        admin.is_staff = True
        changed = True
    if not admin.is_superuser:
        admin.is_superuser = True
        changed = True

    if created or not admin.check_password(DEFAULT_PASSWORD):
        admin.set_password(DEFAULT_PASSWORD)
        changed = True

    if changed:
        admin.save()

    return admin


def ensure_email_token(user):
    token, _ = EmailConfirmationToken.objects.get_or_create(
        user=user,
        defaults={
            "is_used": True,
            "expires_at": timezone.now() + timedelta(days=30),
        },
    )
    updated = False
    if not token.is_used:
        token.is_used = True
        updated = True
    if token.expires_at <= timezone.now():
        token.expires_at = timezone.now() + timedelta(days=30)
        updated = True
    if updated:
        token.save(update_fields=["is_used", "expires_at"])


def seed_specializations():
    result = []
    for slug, name in SPECIALIZATIONS:
        specialization, _ = Specialization.objects.update_or_create(
            slug=slug,
            defaults={
                "name": name,
                "description": f"{name} support direction for the center.",
                "icon": "brain",
            },
        )
        result.append(specialization)
    return result


def seed_psychologists(specializations):
    result = []
    for index, payload in enumerate(PSYCHOLOGISTS):
        user, created = User.objects.get_or_create(
            email=payload["email"],
            defaults={
                "role": User.Role.PSYCHOLOGIST,
                "is_active": True,
            },
        )
        changed = False
        if user.role != User.Role.PSYCHOLOGIST:
            user.role = User.Role.PSYCHOLOGIST
            changed = True
        if not user.is_active:
            user.is_active = True
            changed = True
        if created or not user.check_password(DEFAULT_PASSWORD):
            user.set_password(DEFAULT_PASSWORD)
            changed = True
        if changed:
            user.save()

        profile, _ = PsychologistProfile.objects.get_or_create(user=user)
        for field, value in payload.items():
            if field != "email":
                setattr(profile, field, value)
        profile.is_verified = True
        profile.verified_at = timezone.now()
        profile.save()
        ensure_email_token(user)

        primary = specializations[index % len(specializations)]
        secondary = specializations[(index + 5) % len(specializations)]
        PsychologistSpecialization.objects.update_or_create(
            psychologist=profile,
            specialization=primary,
            defaults={"is_primary": True},
        )
        PsychologistSpecialization.objects.update_or_create(
            psychologist=profile,
            specialization=secondary,
            defaults={"is_primary": False},
        )
        result.append(profile)
    return result


def seed_clients():
    result = []
    for payload in CLIENTS:
        user, created = User.objects.get_or_create(
            email=payload["email"],
            defaults={
                "role": User.Role.CLIENT,
                "is_active": True,
            },
        )
        changed = False
        if user.role != User.Role.CLIENT:
            user.role = User.Role.CLIENT
            changed = True
        if not user.is_active:
            user.is_active = True
            changed = True
        if created or not user.check_password(DEFAULT_PASSWORD):
            user.set_password(DEFAULT_PASSWORD)
            changed = True
        if changed:
            user.save()

        profile, _ = ClientProfile.objects.get_or_create(user=user)
        profile.first_name = payload["first_name"]
        profile.last_name = payload["last_name"]
        profile.phone = payload["phone"]
        profile.date_of_birth = payload["date_of_birth"]
        profile.save()
        ensure_email_token(user)
        result.append(profile)
    return result


def seed_time_slots(psychologists):
    result = []
    today = timezone.localdate()
    hours = [
        (time(10, 0), time(11, 0)),
        (time(12, 0), time(13, 0)),
        (time(14, 0), time(15, 0)),
    ]

    for index, profile in enumerate(psychologists):
        for offset, (start, end) in enumerate(hours, start=1):
            slot_date = today + timedelta(days=index + offset + 1)
            slot, _ = TimeSlot.objects.update_or_create(
                psychologist=profile,
                date=slot_date,
                start_time=start,
                defaults={
                    "end_time": end,
                    "is_available": True,
                },
            )
            result.append(slot)

    return result


def seed_appointments(clients, psychologists):
    result = []
    for index in range(15):
        client = clients[index]
        psychologist = psychologists[index]
        slot_date = timezone.localdate() - timedelta(days=15 - index)
        slot, _ = TimeSlot.objects.update_or_create(
            psychologist=psychologist,
            date=slot_date,
            start_time=time(11, 0),
            defaults={
                "end_time": time(12, 0),
                "is_available": False,
            },
        )
        slot.is_available = False
        slot.save(update_fields=["is_available"])

        appointment, _ = Appointment.objects.update_or_create(
            client=client,
            psychologist=psychologist,
            time_slot=slot,
            defaults={
                "status": Appointment.Status.COMPLETED,
                "comment": APPOINTMENT_COMMENTS[index],
            },
        )
        result.append(appointment)
    return result


def seed_reviews(appointments):
    result = []
    for index, appointment in enumerate(appointments):
        review, _ = Review.objects.update_or_create(
            appointment=appointment,
            defaults={
                "rating": 5 if index % 3 else 4,
                "text": REVIEW_TEXTS[index],
            },
        )
        result.append(review)
    return result


def main():
    post_save.disconnect(create_user_profile, sender=User)
    try:
        admin = create_or_update_admin()
        ensure_email_token(admin)
        specializations = seed_specializations()
        psychologists = seed_psychologists(specializations)
        clients = seed_clients()
        appointments = seed_appointments(clients, psychologists)
        reviews = seed_reviews(appointments)
        future_slots = seed_time_slots(psychologists)

        print("Demo data is ready.")
        print(f"Admin: {admin.email} / {DEFAULT_PASSWORD}")
        print(f"Client: {clients[0].user.email} / {DEFAULT_PASSWORD}")
        print(f"Psychologist: {psychologists[0].user.email} / {DEFAULT_PASSWORD}")
        print("")
        print(f"Users: {User.objects.count()}")
        print(f"Client profiles: {ClientProfile.objects.count()}")
        print(f"Psychologist profiles: {PsychologistProfile.objects.count()}")
        print(f"Specializations: {Specialization.objects.count()}")
        print(f"Psychologist-specialization links: {PsychologistSpecialization.objects.count()}")
        print(f"Time slots: {TimeSlot.objects.count()}")
        print(f"Appointments: {Appointment.objects.count()}")
        print(f"Reviews: {Review.objects.count()}")
        print(f"Email tokens: {EmailConfirmationToken.objects.count()}")
        print(f"Future slots created: {len(future_slots)}")
        print(f"Completed appointments created: {len(appointments)}")
        print(f"Reviews created: {len(reviews)}")
    finally:
        post_save.connect(create_user_profile, sender=User)


if __name__ == "__main__":
    main()
