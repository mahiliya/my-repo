def normalize_fields_and_counts(value):
	if isinstance(value, dict):
		value = [value]
	elif not isinstance(value, list):
		return []

	cleaned = []
	for item in value:
		if not isinstance(item, dict):
			continue
		field_name = item.get('field')
		if not field_name:
			continue
		count_value = item.get('count')
		try:
			count_value = int(count_value)
		except (TypeError, ValueError):
			continue

		cleaned.append({'field': field_name, 'count': count_value})

	return cleaned


def required_fields_map(value):
	return {
		item['field'].strip().lower(): item['count']
		for item in normalize_fields_and_counts(value)
	}
