# -*- coding: utf-8 -*-

from distutils.version import StrictVersion

import django
from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from django.conf.urls import url

from .. import admin_views
from ..models import Publication, PublicationLink, PublicationFile, Catalog


class PublicationCatalogInline(admin.TabularInline):
    model = Catalog.publications.through


class PublicationLinkInline(admin.StackedInline):
    model = PublicationLink
    extra = 1
    max_num = 5


class PublicationFileInline(admin.StackedInline):
    model = PublicationFile
    extra = 1
    max_num = 5


class PublicationAdminForm(forms.ModelForm):
    class Meta:
        model = Publication
        # Fix for Django<1.7
        if StrictVersion(django.get_version()) >= StrictVersion('1.7.0'):
            fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PublicationAdminForm, self).__init__(*args, **kwargs)

        # give (usually) numeric fields appearance of IntegerField
        for field in ['volume', 'number', 'chapter', 'section']:
            self.fields[field].widget.attrs['class'] = 'vIntegerField'


class PublicationAdmin(admin.ModelAdmin):
    form = PublicationAdminForm
    list_display = ('type', 'first_author', 'title', 'type', 'year', 'journal_or_book_title',)
    list_display_links = ('title',)
    list_filter = ('year', 'journal',)
    change_list_template = 'admin/publications_bootstrap/publication_change_list.html'
    search_fields = (
        'title', 'journal', 'book_title', 'authors', 'tags', 'year', 'institution', 'school', 'organization')
    fieldsets = (
        (None, {
            'fields': ('type', 'title', 'authors', 'year', 'month', 'external')}),
        ('All available fields (overridden if set below)', {
            'classes': ('collapse',),
            'fields': (
                'book_title', 'publisher', 'editor', 'edition', 'institution', 'school', 'organization', 'location',
                'country', 'volume', 'number', 'series', 'chapter', 'section', 'pages', 'url')}),
        ('Journal', {
            'classes': ('collapse',),
            'fields': ('journal', 'volume', 'number', 'pages')}),
        ('Conference', {
            'classes': ('collapse',),
            'fields': (
                'book_title', 'editor', 'volume', 'number', 'series', 'pages', 'location', 'country', 'organization',
                'publisher')}),
        ('Technical Report', {
            'classes': ('collapse',),
            'fields': ('institution', 'number', 'location', 'country')}),
        ('Book or Manual', {
            'classes': ('collapse',),
            'fields': (
                'editor', 'publisher', 'volume', 'number', 'series', 'organization', 'location', 'country',
                'edition')}),
        ('In Book or Collection', {
            'classes': ('collapse',),
            'fields': ('book_title', 'editor', 'chapter', 'pages', 'publisher', 'volume', 'number',
                       'series', 'location', 'country', 'edition')}),
        ('Thesis', {
            'classes': ('collapse',),
            'fields': ('school', 'location', 'country')}),
        ('References', {
            'fields': ('citekey', 'tags', 'code', 'url', 'doi', 'isbn')}),
        ('Description', {
            'fields': ('abstract', 'note')}),
        ('Media', {
            'classes': ('collapse',),
            'fields': ('pdf', 'image', 'thumbnail')}),
    )
    inlines = [PublicationLinkInline, PublicationFileInline, PublicationCatalogInline]

    def get_urls(self):
        return [url(r'^import_bibtex/$', admin_views.import_bibtex, name='publications_publication_import_bibtex'),
                ] + super(PublicationAdmin, self).get_urls()

    