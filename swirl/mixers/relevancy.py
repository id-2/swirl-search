'''
@author:     Sid Probstein
@contact:    sid@swirl.today
'''

from sys import path
from os import environ
from datetime import datetime

import django
from django.core.exceptions import ObjectDoesNotExist

from swirl.utils import swirl_setdir
path.append(swirl_setdir()) # path to settings.py file
environ.setdefault('DJANGO_SETTINGS_MODULE', 'swirl_server.settings') 
django.setup()

from operator import itemgetter

from swirl.mixers.mixer import Mixer
from swirl.mixers.utils import * 

#############################################    
#############################################    

class RelevancyMixer(Mixer):

    type = 'RelevancyMixer'

    def order(self):

        # sort by score
        self.mixed_results = sorted(sorted(sorted(self.all_results, key=itemgetter('searchprovider_rank')), key=itemgetter('date_published'), reverse=True), key=itemgetter('swirl_score'), reverse=True)

#############################################    

class RelevancyNewItemsMixer(Mixer):

    type = 'RelevancyNewItemsMixer'

    def order(self):

        # filter to new=True
        self.new_results = [result for result in self.all_results if 'new' in result]

        # to do: handle 0 new items?!?

        self.found = len(self.new_results)
        self.mix_wrapper['info']['results']['retrieved_total'] = self.found
        self.mix_wrapper['messages'].append(f"[{datetime.now()}] RelevancyNewItemsMixer hid {len(self.all_results) - int(self.found)} old results")

        # sort by score
        self.mixed_results = sorted(sorted(sorted(self.new_results, key=itemgetter('searchprovider_rank')), key=itemgetter('date_published'), reverse=True), key=itemgetter('swirl_score'), reverse=True)

