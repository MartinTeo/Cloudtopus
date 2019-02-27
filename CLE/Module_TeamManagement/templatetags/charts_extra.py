from django import template
from django.template.defaultfilters import stringfilter
from statistics import mean, median

register = template.Library()

@register.filter 
def get_item(dictionary, key): return dictionary.get(key)


@register.filter 
def get_index(list, key): return list[key]

@register.filter 
def getTotalClassPoints(dictionary): #sum class points
    classPoints = 0
    print(dictionary)
    for keys, values in dict(dictionary).items():
        classPoints += values["points"]
    return classPoints

@register.filter 
def getTotalClassBadges(dictionary): #sum class badges
    classBadges = 0
    for keys, values in dict(dictionary).items():
        classBadges += values["badges"]
    return classBadges

@register.filter
def getTotalNumStudents(dictionary):
    return len(dictionary.get('students'))

@register.filter
def describeSet(setValues):
    if setValues == []:
        return [0,0,0,0] #min , max , median , average
    else:
        return [min(setValues), max(setValues), median(setValues),mean(setValues)]

@register.filter
def replaceSpace(string):
    return string.replace(" ","")

@register.filter
def learning_tool_split(dictionary):
    return dictionary.split("_")