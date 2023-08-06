import logging
import jsonschema


def validate(instance, schema):
  logging.debug("[+] Validating parameters")
  try:
    jsonschema.validate(instance=instance, schema=schema)
  except Exception:
    logging.debug(" '-> Invalid parameters")
    return False
  logging.debug(" '-> Valid parameters")
  return True
