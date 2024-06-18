PAYMENT_METHODS = [
    ('credit', 'Tarjeta de crédito'),
    ('debit', 'Tarjeta de débito'),
]

PAYMENT_STATUS = [
    ('successful', 'Exitoso'),
    ('rejected', 'Rechazado')
]

SCHEDULING_STATUS = [
    ('paid', 'Pagado'),
    ('unpaid', 'No pagado')
]

CURRENCY_TYPES = [
    ('chilean-peso', 'Pesos chilenos'),
    ('us-dolar', 'Dólares estadounidenses')
]

PROFESSIONAL_OCCUPATIONS = [
    ("psychologist", "Psicólogo/a"),
    ("psychiatrist", "Psiquiatra"),
    ("pediatrician", "Pediatra"),
    ("geriatrician", "Geriatra"),
    ("midwife", "Matrón/a"),
    ("doctor", "Doctor/a"),
    ("family_doctor", "Médico/a familiar"),
    ("obstetrician", "Gineco-obstetra"),
    ("lawyer", "Abogado/a"),
    ("other", "Otro"),
]

CURRENCY_INFO = {
    'chilean-peso': {
        'to_spanish': 'Pesos chilenos',
        'equivalent_value_of_the_currency_to_one_chilean_peso': 1
    },
    'us-dolar': {
        'to_spanish': 'Dólares estadounidenses',
        'equivalent_value_of_the_currency_to_one_chilean_peso': 1/926
    }
}
