from pathlib import Path

def file_content(path, default=None):
  content = default
  try:
    content = (Path.cwd() / path).read_text()
    content.strip()
  except FileNotFoundError:
    pass
  return content
