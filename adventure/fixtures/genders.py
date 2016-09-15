from adventure.models import Gender


male = Gender(
    gender='male',
    subject_pronoun='he',
    object_pronoun='him',
    possessive_pronoun='his',
)

female = Gender(
    gender='female',
    subject_pronoun='she',
    object_pronoun='her',
    possessive_pronoun='her',
)

unspecified = Gender(
    gender='unspecified',
    subject_pronoun='they',
    object_pronoun='them',
    possessive_pronoun='their',
)

creature = Gender(
    gender='creature',
    subject_pronoun='it',
    object_pronoun='it',
    possessive_pronoun='its',
)
