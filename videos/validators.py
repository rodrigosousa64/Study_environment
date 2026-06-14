from rest_framework import serializers

def no_bad_words(value):
    bad_words = ["apple", "banana", "cherry"]
    for word in bad_words:
        if word in value.lower():
            raise serializers.ValidationError("Bad word detected")
    return value