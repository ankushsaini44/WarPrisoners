#!/usr/bin/env python3
#  -*- coding: UTF-8 -*-
"""
Mapping of CSV columns to RDF properties
"""

from converters import convert_dates, strip_dash
from namespaces import *


# Mapping dict. Person name is taken from the first field separately.

PRISONER_MAPPING = {
    'syntymäaika': {'uri': SCHEMA_NS.birth_date,
                    'converter': convert_dates,
                    'value_separator': '/',
                    'name_fi': 'Syntymäaika',
                    'name_en': 'Date of birth'},
    'syntymäpaikka': {'uri': SCHEMA_NS.birth_place,
                      'value_separator': '/',
                      'name_fi': 'Syntymäkunta',
                      'name_en': 'Municipality of birth'
                      },
    'kotipaikka': {'uri': SCHEMA_NS.home_place,
                   'value_separator': '/',
                   'name_fi': 'Kotikunta',
                   'name_en': 'Home municipality'
                   },
    'asuinpaikka': {'uri': SCHEMA_NS.residence_place,
                    'name_fi': 'Asuinpaikka',
                    'name_en': 'Municipality of residence',
                    'value_separator': '/'},
    'ammatti': {'uri': BIOC.has_occupation,
                'name_fi': 'Ammatti',
                'name_en': 'Occupation',
                'value_separator': '/'},
    'siviilisääty': {'uri': SCHEMA_NS.marital_status,
                     'name_fi': 'Siviilisääty',
                     'name_en': 'Marital Status',
                     'value_separator': '/'},
    'lasten lkm': {'uri': SCHEMA_NS.amount_children,
                   'converter': strip_dash,
                   'name_fi': 'Lasten lukumäärä',
                   'name_en': 'Amount of children',
                   'value_separator': '/'},
    'sotilasarvo': {'uri': SCHEMA_NS.rank,
                    'name_fi': 'Sotilasarvo',
                    'name_en': 'Military Rank',
                    'value_separator': '/'},
    'joukko-osasto': {'uri': SCHEMA_NS.unit,
                      'name_en': 'Military Unit',
                      'name_fi': 'Joukko-osasto'},
    'vangiksi aika': {'uri': SCHEMA_NS.time_captured,
                      'converter': convert_dates,
                      'value_separator': '/',
                      'name_en': 'Date captured',
                      'name_fi': 'Vangiksi jäämisen päivämäärä'},
    'vangiksi paikka, kunta': {'uri': SCHEMA_NS.place_captured_municipality,
                               'value_separator': '/',
                               'name_en': 'Municipality where captured',
                               'name_fi': 'Vangiksi jäämisen kunta'},
    'vangiksi paikka, kylä, kaupunginosa': {'uri': SCHEMA_NS.place_captured,
                                            'value_separator': '/',
                                            'name_en': 'Place where captured',
                                            'name_fi': 'Vangiksi jäämisen paikka'},
    'vangiksi, taistelupaikka': {'uri': SCHEMA_NS.place_captured_battle,
                                 'value_separator': '/',
                                 'name_en': 'Battle location where captured',
                                 'name_fi': 'Vangiksi jäämisen taistelupaikka'},
    'selvitys vangiksi jäämisestä': {'uri': SCHEMA_NS.explanation,
                                     'name_en': 'Description of capturing',
                                     'name_fi': 'Selvitys vangiksi jäämisestä'},
    'palannut': {'uri': SCHEMA_NS.returned_date,
                 'converter': convert_dates,
                 'value_separator': '/',
                 'name_en': 'Date of returning',
                 'name_fi': 'Palaamisaika'},
    'kuollut': {'uri': SCHEMA_NS.death_date,
                'converter': convert_dates,
                'value_separator': '/',
                'name_en': 'Date of death',
                'name_fi': 'Kuolinaika'},
    'kuolinsyy': {'uri': SCHEMA_NS.cause_of_death,
                  'name_en': 'Cause of death',
                  'name_fi': 'Kuolinsyy'},
    'kuolinpaikka': {'uri': SCHEMA_NS.death_place,  # epämääräinen muotoilu
                     'value_separator': '/',
                     'name_en': 'Place of death',
                     'name_fi': 'kuolinpaikka'},
    'hautauspaikka': {'uri': SCHEMA_NS.burial_place,
                      'value_separator': ';',
                      'name_en': 'Place of burial',
                      'name_fi': 'Hautauspaikka'},
    'vankeuspaikat': {'uri': SCHEMA_NS.camps_and_hospitals,
                      'value_separator': ';',
                      'reify_order_number': True,  # TODO: Implement this (as index * 10 for maintainability)
                      'name_en': 'Captivity locations',
                      'name_fi': 'Vankeuspaikat'},
    ' muita tietoja': {'uri': SCHEMA_NS.other_information,
                       'value_separator': ';',
                       'name_fi': 'Muita tietoja',
                       'name_en': 'Other information',
                       },
    # 'lisätietoja': {'uri': SCHEMA_NS.additional_information,
    #                 'value_separator': ';',
    #                 'name_en': 'Additional information',
    #                 'name_fi': 'Lisätietoja'},
    'palanneiden kuolinaika': {'uri': SCHEMA_NS.death_date,  # Property name given on previous usage
                               'converter': convert_dates,
                               'value_separator': '/'},
    # 'Sotavangit ry:n jäsen': {'uri': SCHEMA_NS.sotavangit_ry, 'value_separator': '/',
    #                           'name_en': 'Sotavangit ry membership',
    #                           'name_fi': 'Sotavangit ry:n jäsen'},
    'valokuva': {'uri': SCHEMA_NS.photograph, 'name_fi': 'Valokuva', 'name_en': 'Photograph'},
    # 'kantakortti tms.': {'uri': SCHEMA_NS.military_record,
    #                      'name_en': 'Military record',
    #                      'name_fi': 'Kantakortti'},
    'radiossa, PM:n valvontatoimiston radiokatsaukset': {'uri': SCHEMA_NS.radio_report,
                     'value_separator': ';',
                     'name_en': 'Radio report',
                     'name_fi': 'Radiokatsaus'},
    # 'katoamisdokumentit': {'uri': SCHEMA_NS.missing_person_documents,
    #                        'name_en': 'Missing person record',
    #                        'name_fi': 'Katoamisdokumentit'},
    'Jatkosodan VEN kuulustelulomakkeet F 473, palautetut': {'uri': SCHEMA_NS.russian_interrogation_sheets,
                                                       'value_separator': ';',
                                                       'name_en': 'Russian interrogation sheets',
                                                       'name_fi': 'Jatkosodan venäläiset kuulustelulomakkeet'},
    'Talvisodan kortisto': {'uri': SCHEMA_NS.winterwar_card_file,
                            'name_en': 'Winter War card file',
                            'name_fi': 'Talvisodan kortisto'},
    # 'kuulustelija': {'uri': SCHEMA_NS.interrogator,
    #                  'value_separator': ';',
    #                  'name_en': 'Interrogator',
    #                  'name_fi': 'Kuulustelija'},
    'takavarikoitu omaisuus, arvo markoissa':
        {'uri': SCHEMA_NS.confiscated_possessions,
         'name_en': 'Confiscated possessions',
         'name_fi': 'takavarikoitu omaisuus, arvo markoissa'},
    'suomenruotsalainen':
        {'uri': SCHEMA_NS.swedish_finn,
         'name_en': 'Swedish finn',
         'name_fi': 'Suomenruotsalainen'},
    'Karagandan kortisto':
        {'uri': SCHEMA_NS.karaganda_card_file,
         'name_en': 'Karaganda card file',
         'name_fi': 'Karagandan kortisto'},
    'Jatkosodan kortisto':
        {'uri': SCHEMA_NS.continuation_war_card_file,
         'name_en': 'Continuation War card file',
         'name_fi': 'Jatkosodan kortisto'},
    'Jatkosodan VEN kuulustelulomakkeet, kuolleet F 465':
        {'uri': SCHEMA_NS.continuation_war_russian_card_file,
         'name_en': 'Continuation War russian card file',
         'name_fi': 'Kuolleiden Jatkosodan venäläiset kuulustelulomakkeet'},
    'Talvisodan kokoelma':
        {'uri': SCHEMA_NS.winter_war_collection,
         'name_en': 'Winter War collection',
         'name_fi': 'Talvisodan kokoelma'},
    'Talvisodan kokoelma, Moskovasta tulevat':
        {'uri': SCHEMA_NS.winter_war_collection_from_moscow,
         'value_separator': ';',
         'name_en': 'Winter War collection (Moscow)',
         'name_fi': 'Talvisodan kokoelma (Moskovasta)'},
    'lentolehtinen':
        {'uri': SCHEMA_NS.flyer,
         'value_separator': ';',
         'name_en': 'Flyer',
         'name_fi': 'Lentolehtinen'},
    'muistelmat, lehtijutut, tietokirjat, tutkimukset, Kansa taisteli-lehti':
        {'uri': SCHEMA_NS.memoirs,
         'name_en': 'Memoirs',
         'name_fi': 'Muistelmat ja lehtijutut'},
    'TV-ja radio-ohjelmat, tallenne video/audio':
        {'uri': SCHEMA_NS.recording,
         'name_en': 'Recording (video/audio)',
         'name_fi': 'Tallenne (video/audio)'},
    'Karjalan kansallisarkiston dokumentit':
        {'uri': SCHEMA_NS.karelian_archive_documents,
         'name_en': 'Karelian archive documents',
         'name_fi': 'Karjalan kansallisarkiston dokumentit'},
}
