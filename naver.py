#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from datetime import datetime
import threading, time

origin = 'https://m.place.naver.com'
referer = 'https://m.place.naver.com/rest/vaccine?vaccineFilter=used&x=126.862304&y=37.5153465&bounds=126.8587071%3B37.5134977%3B126.8659008%3B37.5171953'
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36'
newHeaders = {'Content-Type':'application/json', 'origin':origin, 'referer':referer, 'user-agent':user_agent }
values = '[{"operationName":"vaccineList","variables":{"input":{"keyword":"코로나백신위탁의료기관","x":"126.862304","y":"37.5153465"},"businessesInput":{"start":0,"display":100,"deviceType":"mobile","x":"126.862304","y":"37.5153465","bounds":"126.8587071;37.5134977;126.8659008;37.5171953","sortingOrder":"distance"},"isNmap":false,"isBounds":false},"query":"query vaccineList($input: RestsInput, $businessesInput: RestsBusinessesInput, $isNmap: Boolean!, $isBounds: Boolean!) {  rests(input: $input) {    businesses(input: $businessesInput) {      total      vaccineLastSave      isUpdateDelayed      items {        id        name        dbType        phone        virtualPhone        hasBooking        hasNPay        bookingReviewCount        description        distance        commonAddress        roadAddress        address        imageUrl        imageCount        tags        distance        promotionTitle        category        routeUrl        businessHours        x        y        imageMarker @include(if: $isNmap) {          marker          markerSelected          __typename        }        markerLabel @include(if: $isNmap) {          text          style          __typename        }        isDelivery        isTakeOut        isPreOrder        isTableOrder        naverBookingCategory        bookingDisplayName        bookingBusinessId        bookingVisitId        bookingPickupId        vaccineOpeningHour {          isDayOff          standardTime          __typename        }        vaccineQuantity {          totalQuantity          totalQuantityStatus          startTime          endTime          vaccineOrganizationCode          list {            quantity            quantityStatus            vaccineType            __typename          }          __typename        }        __typename      }      optionsForMap @include(if: $isBounds) {        maxZoom        minZoom        includeMyLocation        maxIncludePoiCount        center        __typename      }      __typename    }    queryResult {      keyword      vaccineFilter      categories      region      isBrandList      filterBooking      hasNearQuery      isPublicMask      __typename    }    __typename  }}"}]'
WAIT_TIME_SECONDS = 5


def call():
    resp = requests.post('https://api.place.naver.com/graphql', values.encode('utf-8'), headers=newHeaders)
    response_Json = resp.json()
    # print('response', response_Json[0]['data']['rests']['businesses']['items'])
    items = response_Json[0]['data']['rests']['businesses']['items']
    print('-----------------------------' , datetime.now().strftime('"%H:%M:%S"') , '----------------------')
    for item in items:
        sum  = int(item['vaccineQuantity']['totalQuantity'])
        if sum >  0:
            print(item['name'], item['vaccineQuantity']['totalQuantity'])
    


ticker = threading.Event()
while not ticker.wait(WAIT_TIME_SECONDS):
    call()