import pytest

phrase = input("Введите фразу: ")
assert len(phrase) < 15, "Фраза должна быть короче 15 символов"
