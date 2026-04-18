from django.db import migrations


SEED = [
    ('Монстера',      'Monstera deliciosa',       '🌴', 7,   730, 'Тропическая лиана. Любит рассеянный свет и умеренный полив.'),
    ('Кактус',        'Cactaceae',                '🌵', 14,  1095, 'Суккулент. Поливать редко, особенно зимой. Много солнца.'),
    ('Фикус',         'Ficus benjamina',          '🌳', 5,   730, 'Светолюбив, не любит сквозняки. Поливать по мере подсыхания.'),
    ('Орхидея',       'Phalaenopsis',             '🌸', 10,  730, 'Рассеянный свет, полив погружением раз в 1-2 недели.'),
    ('Спатифиллум',   'Spathiphyllum',            '🌿', 4,   365, 'Любит влагу и полутень. Опускает листья, когда хочет пить.'),
    ('Сансевиерия',   'Sansevieria trifasciata',  '🗡️', 14,  1095, 'Очень выносливая. Поливать редко, переносит тень.'),
    ('Фиалка',        'Saintpaulia',              '💜', 5,   365, 'Поливать в поддон тёплой водой. Не любит попадания воды на листья.'),
    ('Алоэ',          'Aloe vera',                '🪴', 14,  1095, 'Суккулент. Солнце и редкий полив. Целебный сок.'),
    ('Драцена',       'Dracaena',                 '🎋', 7,   730, 'Яркий рассеянный свет, умеренный полив, любит опрыскивание.'),
    ('Замиокулькас',  'Zamioculcas zamiifolia',   '🌱', 14,  730, 'Долларовое дерево. Неприхотливо, выдерживает засуху.'),
]


def forwards(apps, schema_editor):
    PlantType = apps.get_model('plants', 'PlantType')
    for name, latin, icon, water, repot, desc in SEED:
        PlantType.objects.update_or_create(
            name=name,
            defaults={
                'latin_name': latin,
                'icon': icon,
                'watering_interval_days': water,
                'repotting_interval_days': repot,
                'description': desc,
            },
        )


def backwards(apps, schema_editor):
    PlantType = apps.get_model('plants', 'PlantType')
    PlantType.objects.filter(name__in=[row[0] for row in SEED]).delete()


class Migration(migrations.Migration):
    dependencies = [('plants', '0001_initial')]
    operations = [migrations.RunPython(forwards, backwards)]
