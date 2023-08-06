from dataclasses import dataclass, field
from typing import List
from unittest import TestCase

from XsCore import Encrypt
from XsCore.DataClassBase import DataClassBase

data = {
    "id": "20531316728",
    "about": "The Facebook Page celebrates how our friends inspire us, support us, and help us discover the world when we connect.",
    "birthday": "02/04/2004",
    "name": "Facebook",
    "username": "facebookapp",
    "fan_count": 214643503,
    "cover": {
        "cover_id": "10158913960541729",
        "offset_x": 50,
        "offset_y": 50,
        "source": "https://scontent.xx.fbcdn.net/v/t1.0-9/s720x720/73087560_10158913960546729_8876113648821469184_o.jpg?_nc_cat=1&_nc_ohc=bAJ1yh0abN4AQkSOGhMpytya2quC_uS0j0BF-XEVlRlgwTfzkL_F0fojQ&_nc_ht=scontent.xx&oh=2964a1a64b6b474e64b06bdb568684da&oe=5E454425",
        "id": "10158913960541729"
    },
    "point_list": [
        {"x": 1, "y": 2},
        {"x": 3, "y": 4},
    ]
}


@dataclass
class Cover(DataClassBase):
    cover_id: str = field(repr=False, )
    offset_x: str = None
    offset_y: str = None
    source: str = None
    id: str = None


@dataclass
class Point(DataClassBase):
    x: int = None
    y: int = None


@dataclass
class Page(DataClassBase):
    id: str = None
    about: str =  field(default=None, repr=False)
    birthday: str = ''
    name: str = None
    username: str = None
    fan_count: int = 0
    cover: Cover = None # field(default=None, repr=False)
    point_list: List[Point] = field(default=None, repr=False)


class ClassDataTest(TestCase):

    def testFromDict(self):
        p = Page.from_dict(data)
        print(p)
        # print(p.cover)
        # print(p.point_list)
        #
        # print(p.to_dict())
        # print(p.to_json())

    def testReadList(self):
        p = Page.from_dict(data)
        print(p.point_list)
        for p in p.point_list:
            print('x:',p.x,'y:',p.y)

    def testReadDicObj(self):
        p = Page.from_dict(data)
        print(p.cover)
        print('cover_id:',p.cover.cover_id)
        print('source:', p.cover.source)
        print('offset_y:', p.cover.offset_y)

    def testToDict(self):
        p = Page.from_dict(data)
        print(p.to_dict())

    def testToJson(self):
        p = Page.from_dict(data)
        print(p.to_json())