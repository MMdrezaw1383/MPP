def func_(x): x += 2; return x


exec("def func(x):\n\tx += 2\n\treturn x ** 2\nprint(func(4))")

exec("def max2(*args):\n\tm=float('-inf')\n\tfor i in args:\n\t\tif i>m:\n\t\t\tm=i\n\treturn m\nprint(max2(1,10,9))")
