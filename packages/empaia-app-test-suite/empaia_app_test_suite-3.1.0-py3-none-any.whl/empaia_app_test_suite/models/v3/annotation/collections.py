from __future__ import annotations

from enum import Enum
from typing import List, Literal, Optional, Union

from pydantic import UUID4, Field, ValidationError, conlist, validator

from ..commons import (
    DataCreatorType,
    Description,
    Id,
    IdObject,
    ItemCount,
    Message,
    Name,
    PostIdObjects,
    RestrictedBaseModel,
    Viewport,
    validate_reference,
)
from .annotations import (
    AnnotationListResponse,
    ArrowAnnotation,
    CircleAnnotation,
    LineAnnotation,
    NppViewing,
    PointAnnotation,
    PolygonAnnotation,
    PostArrowAnnotation,
    PostCircleAnnotation,
    PostLineAnnotation,
    PostPointAnnotation,
    PostPolygonAnnotation,
    PostRectangleAnnotation,
    RectangleAnnotation,
)
from .classes import Class, ClassListResponse, PostClass
from .primitives import (
    BoolPrimitive,
    FloatPrimitive,
    IntegerPrimitive,
    PostBoolPrimitive,
    PostFloatPrimitive,
    PostIntegerPrimitive,
    PostStringPrimitive,
    PrimitiveList,
    StringPrimitive,
)


class CollectionItemType(str, Enum):
    WSI = "wsi"
    INTEGER = "integer"
    FLOAT = "float"
    BOOL = "bool"
    STRING = "string"
    POINT = "point"
    LINE = "line"
    ARROW = "arrow"
    CIRCLE = "circle"
    RECTANGLE = "rectangle"
    POLYGON = "polygon"
    CLASS = "class"
    COLLECTION = "collection"


class CollectionReferenceType(str, Enum):
    ANNOTATION = "annotation"
    WSI = "wsi"


# Item type models


class SlideItem(RestrictedBaseModel):
    id: Id = Field(example="4967bf63-a2a1-421c-8789-bf616953537c", description="WSI ID")
    type: Literal["wsi"] = Field(example="wsi", description="WSI type")


TYPE_MAPPING = {
    "point": PostPointAnnotation,
    "line": PostLineAnnotation,
    "arrow": PostArrowAnnotation,
    "circle": PostCircleAnnotation,
    "rectangle": PostRectangleAnnotation,
    "polygon": PostPolygonAnnotation,
    "class": PostClass,
    "integer": PostIntegerPrimitive,
    "float": PostFloatPrimitive,
    "bool": PostBoolPrimitive,
    "string": PostStringPrimitive,
    "wsi": SlideItem,
}


def check_items(items, type_name):
    if items and len(items) > 0:
        if not TYPE_MAPPING[type_name].parse_obj(items[0]):
            raise ValidationError()
    return items


class PostPointAnnotations(RestrictedBaseModel):
    items: Optional[List[PostPointAnnotation]] = Field(description="List of point annotations")

    @validator("items", pre=True)
    def pre_check_item_list(cls, v):
        return check_items(v, "point")


class PostLineAnnotations(RestrictedBaseModel):
    items: Optional[List[PostLineAnnotation]] = Field(description="List of line annotations")

    @validator("items", pre=True)
    def pre_check_item_list(cls, v):
        return check_items(v, "line")


class PostArrowAnnotations(RestrictedBaseModel):
    items: Optional[List[PostArrowAnnotation]] = Field(description="List of arrow annotations")

    @validator("items", pre=True)
    def pre_check_item_list(cls, v):
        return check_items(v, "arrow")


class PostCircleAnnotations(RestrictedBaseModel):
    items: Optional[List[PostCircleAnnotation]] = Field(description="List of circle annotations")

    @validator("items", pre=True)
    def pre_check_item_list(cls, v):
        return check_items(v, "circle")


class PostRectangleAnnotations(RestrictedBaseModel):
    items: Optional[List[PostRectangleAnnotation]] = Field(description="List of rectangle annotations")

    @validator("items", pre=True)
    def pre_check_item_list(cls, v):
        return check_items(v, "rectangle")


class PostPolygonAnnotations(RestrictedBaseModel):
    items: Optional[List[PostPolygonAnnotation]] = Field(description="List of polygon annotations")

    @validator("items", pre=True)
    def pre_check_item_list(cls, v):
        return check_items(v, "polygon")


class PostClasses(RestrictedBaseModel):
    items: Optional[List[PostClass]] = Field(description="List of classes")

    @validator("items", pre=True)
    def pre_check_item_list(cls, v):
        return check_items(v, "class")


class PostIntegerPrimitives(RestrictedBaseModel):
    items: Optional[List[PostIntegerPrimitive]] = Field(description="List of integer primitives")

    @validator("items", pre=True)
    def pre_check_item_list(cls, v):
        return check_items(v, "integer")


class PostFloatPrimitives(RestrictedBaseModel):
    items: Optional[List[PostFloatPrimitive]] = Field(description="List of float primitives")

    @validator("items", pre=True)
    def pre_check_item_list(cls, v):
        return check_items(v, "float")


class PostBoolPrimitives(RestrictedBaseModel):
    items: Optional[List[PostBoolPrimitive]] = Field(description="List of bool primitives")

    @validator("items", pre=True)
    def pre_check_item_list(cls, v):
        return check_items(v, "bool")


class PostStringPrimitives(RestrictedBaseModel):
    items: Optional[List[PostStringPrimitive]] = Field(description="List of string primitives")

    @validator("items", pre=True)
    def pre_check_item_list(cls, v):
        return check_items(v, "string")


class PostSlideItems(RestrictedBaseModel):
    items: Optional[List[SlideItem]] = Field(description="List of items")

    @validator("items", pre=True)
    def pre_check_item_list(cls, v):
        return check_items(v, "wsi")


class SlideList(PostSlideItems):
    item_count: ItemCount = Field(example=12345, description="Count of all items")
    items: List[SlideItem] = Field(description="List of items")


# Post models


class PostCollectionBase(RestrictedBaseModel):
    id: Optional[UUID4] = Field(
        example="4967bf63-a2a1-421c-8789-bf616953537c",
        description="ID of type UUID4 (only needed in post if external Ids enabled)",
    )
    type: Literal["collection"] = Field(example="collection", description="Collection type")
    name: Optional[Name] = Field(example="Collection Name", description="Collection name")
    description: Optional[Description] = Field(example="Collection Description", description="Collection description")
    creator_id: Id = Field(
        example="b10648a7-340d-43fc-a2d9-4d91cc86f33f",
        description="Creator Id",
    )
    creator_type: DataCreatorType = Field(example=DataCreatorType.JOB, description="Creator type")
    reference_id: Optional[Id] = Field(
        example="b10648a7-340d-43fc-a2d9-4d91cc86f33f",
        description="Id of the object referenced by this collection",
    )
    reference_type: Optional[CollectionReferenceType] = Field(
        example=CollectionReferenceType.WSI, description="Refrence type"
    )

    # validator for reference
    @validator("reference_type", always=True, pre=True)
    def check_reference(cls, reference_type, values):
        reference_id = values.get("reference_id")
        validate_reference(reference_id, reference_type)
        return reference_type


class PostPointCollection(PostCollectionBase, PostPointAnnotations):
    item_type: Literal["point"] = Field(example="point", description="Item type of collection")


class PostLineCollection(PostCollectionBase, PostLineAnnotations):
    item_type: Literal["line"] = Field(example="line", description="Item type of collection")


class PostArrowCollection(PostCollectionBase, PostArrowAnnotations):
    item_type: Literal["arrow"] = Field(example="arrow", description="Item type of collection")


class PostCirceCollection(PostCollectionBase, PostCircleAnnotations):
    item_type: Literal["circle"] = Field(example="circle", description="Item type of collection")


class PostRectangleCollection(PostCollectionBase, PostRectangleAnnotations):
    item_type: Literal["rectangle"] = Field(example="rectangle", description="Item type of collection")


class PostPolygonCollection(PostCollectionBase, PostPolygonAnnotations):
    item_type: Literal["polygon"] = Field(example="polygon", description="Item type of collection")


class PostClassCollection(PostCollectionBase, PostClasses):
    item_type: Literal["class"] = Field(example="class", description="Item type of collection")


class PostIntegerCollection(PostCollectionBase, PostIntegerPrimitives):
    item_type: Literal["integer"] = Field(example="integer", description="Item type of collection")


class PostFloatCollection(PostCollectionBase, PostFloatPrimitives):
    item_type: Literal["float"] = Field(example="float", description="Item type of collection")


class PostBoolCollection(PostCollectionBase, PostBoolPrimitives):
    item_type: Literal["bool"] = Field(example="bool", description="Item type of collection")


class PostStringCollection(PostCollectionBase, PostStringPrimitives):
    item_type: Literal["string"] = Field(example="string", description="Item type of collection")


class PostSlideCollection(PostCollectionBase, PostSlideItems):
    item_type: Literal["wsi"] = Field(example="wsi", description="Item type of collection")


class PostIdCollection(PostCollectionBase, PostIdObjects):
    item_type: CollectionItemType = Field(example=CollectionItemType.POINT, description="Item type of collection")


class PostNestedCollectionBase(PostCollectionBase):
    item_type: Literal["collection"] = Field(example="collection", description="Item type of collection")


class PostNestedItems(RestrictedBaseModel):
    items: Optional[
        List[
            Union[
                PostPointCollection,
                PostLineCollection,
                PostArrowCollection,
                PostCirceCollection,
                PostRectangleCollection,
                PostPolygonCollection,
                PostClassCollection,
                PostIntegerCollection,
                PostFloatCollection,
                PostBoolCollection,
                PostStringCollection,
                PostSlideCollection,
                PostIdCollection,
                PostNestedCollection,
            ]
        ]
    ] = Field(description="List of items")


class PostNestedItemsApps(RestrictedBaseModel):
    items: Optional[
        List[
            Union[
                PostPointCollection,
                PostLineCollection,
                PostArrowCollection,
                PostCirceCollection,
                PostRectangleCollection,
                PostPolygonCollection,
                PostClassCollection,
                PostIntegerCollection,
                PostFloatCollection,
                PostBoolCollection,
                PostStringCollection,
                PostNestedCollection,
            ]
        ]
    ] = Field(description="List of items")


class PostNestedCollection(PostNestedCollectionBase, PostNestedItems):
    pass


PostNestedCollection.update_forward_refs()


class PostNestedCollectionApps(PostNestedCollectionBase, PostNestedItemsApps):
    pass


PostNestedCollectionApps.update_forward_refs()


PostCollection = Union[
    PostPointCollection,
    PostLineCollection,
    PostArrowCollection,
    PostCirceCollection,
    PostRectangleCollection,
    PostPolygonCollection,
    PostClassCollection,
    PostIntegerCollection,
    PostFloatCollection,
    PostBoolCollection,
    PostStringCollection,
    PostSlideCollection,
    PostIdCollection,
    PostNestedCollection,
]


PostCollectionApps = Union[
    PostPointCollection,
    PostLineCollection,
    PostArrowCollection,
    PostCirceCollection,
    PostRectangleCollection,
    PostPolygonCollection,
    PostClassCollection,
    PostIntegerCollection,
    PostFloatCollection,
    PostBoolCollection,
    PostStringCollection,
    PostNestedCollectionApps,
]


class PostCollections(PostNestedItems):
    pass


class PostCollectionsApps(PostNestedItemsApps):
    pass


# Full model


class Collection(PostCollectionBase):
    item_type: CollectionItemType = Field(example=CollectionItemType.POINT, description="Item type of collection")
    is_locked: Optional[bool] = Field(
        example="false",
        description="Flag to mark a collection as immutable",
    )
    item_count: Optional[ItemCount] = Field(example=42, description="The number of items in the collection")
    items: Optional[
        Union[
            List[PointAnnotation],
            List[LineAnnotation],
            List[ArrowAnnotation],
            List[CircleAnnotation],
            List[RectangleAnnotation],
            List[PolygonAnnotation],
            List[Class],
            List[IntegerPrimitive],
            List[FloatPrimitive],
            List[BoolPrimitive],
            List[StringPrimitive],
            List[SlideItem],
            List[IdObject],
            List[Collection],
        ]
    ] = Field(description="Items of the collection")
    item_ids: Optional[List[UUID4]] = Field(
        description="Ids of items in collection",
        example=[
            "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
        ],
    )


Collection.update_forward_refs()


class CollectionList(RestrictedBaseModel):
    item_count: ItemCount = Field(example=12345, description="Count of items.")
    items: List[Collection] = Field(description="List of items.")


# Query model


class CollectionQuery(RestrictedBaseModel):
    creators: Optional[conlist(Id, min_items=1)] = Field(
        example=[
            "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
        ],
        description="List of creator Ids",
    )
    references: Optional[conlist(Id, min_items=1)] = Field(
        example=[
            "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
        ],
        description="List of reference Ids",
    )
    jobs: Optional[conlist(Id, min_items=1)] = Field(
        example=[
            "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
        ],
        description="List of job Ids",
    )
    item_types: Optional[conlist(CollectionItemType, min_items=1)] = Field(
        example=[CollectionItemType.INTEGER, CollectionItemType.FLOAT], description="List of item types"
    )


# Item models


PostItem = Union[
    PostPointAnnotation,
    PostLineAnnotation,
    PostArrowAnnotation,
    PostCircleAnnotation,
    PostRectangleAnnotation,
    PostPolygonAnnotation,
    PostClass,
    PostIntegerPrimitive,
    PostFloatPrimitive,
    PostBoolPrimitive,
    PostStringPrimitive,
    SlideItem,
    IdObject,
    PostCollection,
]


PostItemList = Union[
    PostPointAnnotations,
    PostLineAnnotations,
    PostArrowAnnotations,
    PostCircleAnnotations,
    PostRectangleAnnotations,
    PostPolygonAnnotations,
    PostClasses,
    PostIntegerPrimitives,
    PostFloatPrimitives,
    PostBoolPrimitives,
    PostStringPrimitives,
    PostSlideItems,
    PostIdObjects,
    PostCollections,
]

PostItemListApps = Union[
    PostPointAnnotations,
    PostLineAnnotations,
    PostArrowAnnotations,
    PostCircleAnnotations,
    PostRectangleAnnotations,
    PostPolygonAnnotations,
    PostClasses,
    PostIntegerPrimitives,
    PostFloatPrimitives,
    PostBoolPrimitives,
    PostStringPrimitives,
    PostCollections,
]


PostItems = Union[PostItem, PostItemList]


class ItemQueryList(RestrictedBaseModel):
    item_count: ItemCount = Field(example=12345, description="Count of all items")
    items: Union[
        List[IntegerPrimitive],
        List[FloatPrimitive],
        List[BoolPrimitive],
        List[StringPrimitive],
        List[PointAnnotation],
        List[LineAnnotation],
        List[ArrowAnnotation],
        List[CircleAnnotation],
        List[RectangleAnnotation],
        List[PolygonAnnotation],
        List[Class],
        List[Collection],
    ] = Field(description="Items returned by item query")


ItemPostResponse = Union[
    Message,
    PointAnnotation,
    LineAnnotation,
    ArrowAnnotation,
    CircleAnnotation,
    RectangleAnnotation,
    PolygonAnnotation,
    AnnotationListResponse,
    IntegerPrimitive,
    FloatPrimitive,
    BoolPrimitive,
    StringPrimitive,
    PrimitiveList,
    Class,
    ClassListResponse,
    SlideItem,
    SlideList,
    Collection,
    CollectionList,
]


# Item query model


class ItemQuery(RestrictedBaseModel):
    references: Optional[conlist(Id, min_items=1)] = Field(
        example=[
            "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
        ],
        description="List of reference Ids",
    )
    viewport: Optional[Viewport] = Field(
        example={"x": 180, "y": 240, "width": 1280, "height": 1024},
        description="The viewport (only used for annotations: only annotations within are returned)",
    )
    npp_viewing: Optional[NppViewing] = Field(
        example=[499.0, 7984.0],
        description="Resolution range in npp (nanometer per pixel) to filter annotations (only used for annotations)",
    )
