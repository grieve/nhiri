from django.core.cache import cache
from django.conf import settings
from rest_framework import serializers
from django.utils.datastructures import SortedDict
from django.db import models
from nhiri.core import models as momentModels

import logging


class CachedSerializer(serializers.ModelSerializer):

    def to_native(self, obj):
        cache_key = "serial-cache-%s-%d" % (obj.__class__.__name__, obj.id)
        response = cache.get(cache_key)
        if response:
            return response
        logging.warning('CACHE MISS: %s' % cache_key)
        response = super(serializers.ModelSerializer, self).to_native(obj)
        cache.set(cache_key, response, settings.DEFAULT_SERIALIZER_CACHE)
        return response


class PolymorphicSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(PolymorphicSerializer, self).__init__(*args, **kwargs)
        self.opts.class_field_exclusions = getattr(self.Meta, 'class_field_exclusions', ())

    def get_default_fields(self):
        """
        Return all the fields that should be serialized for the model.
        """

        fields = []
        for cls in self.opts.model:
            assert cls is not None, \
                "Serializer class '%s' is missing 'model' Meta option" % self.__class__.__name__
            opts = serializers.get_concrete_model(cls)._meta
            pk_field = opts.pk

            # If model is a child via multitable inheritance, use parent's pk
            while pk_field.rel and pk_field.rel.parent_link:
                pk_field = pk_field.rel.to._meta.pk

            fields += [pk_field]
            fields += [field for field in opts.fields if field.serialize]
            fields += [field for field in opts.many_to_many if field.serialize]

        ret = SortedDict()
        nested = bool(self.opts.depth)
        is_pk = True  # First field in the list is the pk

        for model_field in fields:
            if is_pk:
                field = self.get_pk_field(model_field)
                is_pk = False
            elif model_field.rel and nested:
                field = self.get_nested_field(model_field)
            elif model_field.rel:
                to_many = isinstance(
                    model_field,
                    models.fields.related.ManyToManyField
                )
                field = self.get_related_field(model_field, to_many=to_many)
            else:
                field = self.get_field(model_field)

            if field:
                ret[model_field.name] = field

        for field_name in self.opts.read_only_fields:
            assert field_name in ret, \
                "read_only_fields on '%s' included invalid item '%s'" % \
                (self.__class__.__name__, field_name)
            ret[field_name].read_only = True

        return ret

    def to_native(self, obj):
        """
        Serialize objects -> primitives.

        Allows for fields being missing from some types.
        Allows for per class field exclusions.

        READ ONLY
        """
        cache_key = "serial-cache-%s-%d" % (obj.__class__.__name__, obj.id)
        response = cache.get(cache_key)
        if response:
            return response
        logging.warning('CACHE MISS: %s' % cache_key)
        ret = self._dict_class()
        ret.fields = {}

        if obj.__class__.__name__ in self.opts.class_field_exclusions:
            exclusions = self.opts.class_field_exclusions[obj.__class__.__name__]
        else:
            exclusions = []

        for field_name, field in self.fields.items():
            if hasattr(obj, field_name) and field_name not in exclusions:
                field.initialize(parent=self, field_name=field_name)
                key = self.get_field_key(field_name)
                value = field.field_to_native(obj, field_name)
                ret[key] = value
                ret.fields[key] = field
        ret['class'] = obj.__class__.__name__
        cache.set(cache_key, ret, settings.DEFAULT_SERIALIZER_CACHE)
        return ret

    def from_native(self, *args, **kwargs):
        raise Exception('Polymorphic serializer is READ ONLY')


class MomentSerializer(PolymorphicSerializer):
    class Meta:

        model = (
            momentModels.TwitterMoment,
            momentModels.GPSMoment
        )
        fields = (
            'id',
            'when',
            'tweet_id',
            'author',
            'retweet',
            'content',
            'original_author',
            'latitude',
            'longitude'
        )
        class_field_exclusions = {}


class CaffeineSerializer(serializers.ModelSerializer):
    class Meta:
        model = momentModels.CaffeineMoment
        fields = (
            'id',
            'when',
            'item',
            'milligrams'
        )
