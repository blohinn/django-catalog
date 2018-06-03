import collections

from django.core.exceptions import ValidationError


def validate_product_json_options(json):
    print(json)

    if 'options' not in json:
        raise ValidationError(
            "Missed 'options' key in options dictionary. Please, use editor for edit product options.")

    # check duplicated options groups

    option_keys = []
    for option in json['options']:
        try:
            option_keys.append(option['option'])
        except Exception as e:
            raise ValidationError('Look like you trying to add not defined option group.')

    duplicated_options = [item for item, count in collections.Counter(option_keys).items() if count > 1]

    if duplicated_options:
        raise ValidationError(
            'Options ({})'.format(
                ', '.join(duplicated_options)) + " are duplicated. OptionGroup should't be repeated in one product.")

    # check duplicated values in option group

    duplicated_values = {}

    for option in json['options']:
        values = []
        for value_dict in option['values']:
            values.append(value_dict['value'])
        _duplicated_values = [item for item, count in collections.Counter(values).items() if count > 1]
        if _duplicated_values:
            duplicated_values[option['option']] = _duplicated_values

    if duplicated_values:
        error_msg = 'Duplicated values in option groups: '
        for k, v in duplicated_values.items():
            error_msg += '{} ({}) '.format(k, ', '.join(v))
        error_msg += '.'
        raise ValidationError(error_msg)

    # check options groups on exist in db

    option_keys = list(set(option_keys))

    from .models import OptionGroup
    db_options_groups = OptionGroup.objects.all()
    db_options_groups_names = [o.name for o in db_options_groups]
    not_defined_options = []
    for o in option_keys:
        if o not in db_options_groups_names:
            not_defined_options.append(o)

    if not_defined_options:
        raise ValidationError(
            'Option group(s) ({}) not defined in options groups.'.format(', '.join(not_defined_options)))

    # check options values on exist in db and belong to its own group

    not_defined_values_by_group = {}
    for option in json['options']:
        values = []
        for value_dict in option['values']:
            values.append(value_dict['value'])

        values = list(set(values))
        db_values_by_option_group = OptionGroup.objects.filter(name=option['option']).first().values.all()
        db_values_by_option_group_names = [v.name for v in db_values_by_option_group]

        not_defined_values = []
        for v in values:
            if v not in db_values_by_option_group_names:
                not_defined_values.append(v)

        if not_defined_values:
            not_defined_values_by_group[option['option']] = not_defined_values

    if not_defined_values_by_group:
        error_msg = 'Values not defined: '
        for k, v in not_defined_values_by_group.items():
            error_msg += '{} ({}) '.format(k, ', '.join(v))
        error_msg += '.'
        raise ValidationError(error_msg)

    # check on empty values

    empty_option_groups = []
    for option in json['options']:
        if not option['values']:
            empty_option_groups.append(option['option'])

    if empty_option_groups:
        raise ValidationError('This options groups not contain any values: {}.'.format(', '.join(empty_option_groups)))
