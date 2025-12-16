
greeter = Greeter()
greeter.for_name("Adam").with_exclamation().underlined().languange('EN').print()

# zadanie na szóstkę (with_exclamation i with_underline obsługiwane jedną funkcją)
greeter.for_Adam().with_exclamation().with_underline().in_english().print()

# zadanie na szóstkę+
greeter.for_Adam.with_exclamation.with_underline.in_english.print()

"""
Hello Adam !!!
--------------
"""

# podpowiedź: __getattr__