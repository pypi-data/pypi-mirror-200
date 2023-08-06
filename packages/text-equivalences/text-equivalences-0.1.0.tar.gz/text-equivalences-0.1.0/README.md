# text-equivalences

## Introduction

Introduces a formalism to express easily some sort of regular expressions that caries semantic information.
This could be used to align two versions of a text, or enumerate variations of one.

Take the following examples _First of January of twenty twenty one_, _Jan 1st 2021_, _01/01/2021_ as humans we understand that these are equivalent because we understand the concept behind it. In my experience I saw this problem bein tackled by doing some text replacements before comparing, this helps but it is difficult to track what happened. What if we could compare the different versions directly.


## Language support

The language is defined so that it can give another interpretation to python code.

### Literal input
Text can be quoted with single or double quotes, e.g. `'single'`, `"double"`, strings can be made case insensitive by adding the suffix `i`, e.g. `'he'i will match any of 'He', 'he', 'HE' or 'hE'.

### Equivalence operator `|` 

The `|` denotes equivalence between two inputs

```
      'first' | '1st'
```

If one of the terms in an alternative chain is matched, for two inputs, the inputs are considered equivalent.

### Alternative operator `/`

The `/` makes it possible to distinguish between two inputs

```
    'one' / 'two' / 'three' | '3'
```

### Sequence

Sequences are defined using the `+` operator.
e.g.
```
  'First' + 'of' + 'January'
```

### Quantifiers

Quantifiers are prefix operators that makes it possible to match variable number of occurrencies of the operand
 - `+`: at least one
 - `-`: at most one

This example makes it possible to accept both _millimetre_ and _millimetres_
```
   'millimetre' + -'s'
```

Concatenation with optional terms can be achieved by simply using `-` operator

```
   'milimetre' -'s'
```

Zero or more repetitions can be achieved by with `-+` prefix operator.

### Rule asignment

Grammar can be stored in local variables, e.g.
```
  first = 'first' | '1st'
```


# Ideas for future versions

### Capture groups (python 3.8)

The output a matched pattern can be assigned to different capture groups

```
(day:=Day + 'of'  -'the' (month:=Month)) | ((month:=Month) + (day:=Day))
```
In the above example two date formats are compared, given that the captured groups matches the outputs will be considered equivalent.

### Capture reference

Capture references allows to check the content at a given position against the content on the input in another position

```
size=Number -!unit 'by' Number (unit:=Unit);
```

### Mapping

Alternatively, the input can be mapped to in a more sophisticated ways by means of mapping rules

```
Digit = (('one' >> '1') / ('two' >> '2') / ('three' >> '3') / ('four' >> '4')
Size =   ((w:=Digit) ('by' | 'x') (h:=Digit)) >> (w ' x ' h)
```

This will translate `one by two` to `1 x 2`.
