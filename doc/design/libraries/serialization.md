# libraries: serialization

This library provide fully templated helper classes to serialize and 
deserialize data to different formats. A different namespace is defined for
each format.
The formats currently implemented are JSON, text and binary. 
Text and binary format implementation are grouped inside the `stream` namespace.

## Design principles

The serialization module has been designed to have for each class or component 
in the data structure that needs to be serialized its equivalent 
`serializer` class. 

For example, a `std::vector` of 3D points needs, to be serialized, to have 
access to two different serializers: a `point_serializer` that will be in 
charge of storing 3D points individually, and a `sequence_serializer` that 
will manage the vector and call the `point_serializer` for each vector element.

Another example would be a `Person` class that contains a name and an age. 
To serialize this class, you will need a `integer_serializer` for the age, 
a `string_serializer` for the name, and a `Person_serializer` for 
the whole structure. 
The `integer_serializer` and `string_serializer` will be created as members 
of the `Person_serializer`, just as the name and age are members of 
the `Person` class.

```cpp
struct Person {
    int age;
    std::string name;
};

struct integer_serializer {
    // ...
};
struct string_serializer {
    // ...
};
struct Person_serializer {
    integer_serializer age_serializer;
    string_serializer  name_serializer;
    
    // ...
};
```

## Implementing new serializers

The `serialization` module provide ready-to-use serializers for:

- default types including integers, floating point numbers, 
  booleans and strings;
- containers, separated in two categories: sequential containers 
  (`std::vector`, `std::list`, etc) and associative containers (`std::map`);
- Some OpenCV and Boost types.

Serializers for other, more complex types have to be defined by the user, and
are expected to rely on basic serializers already implemented by the library.
For each format, two abstract classes are defined for respectively loading and
saving data. These base classes have to be subclassed depending on the features
needed in the new serializer (saving, loading, or both).

Each format will also have helpers specific to them. For example, binary format 
have serializers handling endianness of numbers, while JSON have helpers to 
save and load structured data from JSON objects. 

In addition, loading serializers can possess as template argument what we call
validators, that are functors that will look at the values just after loading 
to check if the data is consistent. 
For example, if you want to load a number that represent an array size, 
you can use the `integer_serializer` with a validator that will ensure that 
the number is postive.

