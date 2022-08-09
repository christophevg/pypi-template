from fire import Fire

from pypi_template import PyPiTemplate

def cli():
  try:
    Fire(PyPiTemplate(), name="pypi-template")
  except KeyboardInterrupt:
    pass

if __name__ == "__main__":
  cli()
