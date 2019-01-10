# coding: utf-8

from modeltranslation.translator import translator, TranslationOptions
from postman.models import Information


class InformationTranslationOption(TranslationOptions):
    fields = ('title', 'text',)


translator.register(Information, InformationTranslationOption)
