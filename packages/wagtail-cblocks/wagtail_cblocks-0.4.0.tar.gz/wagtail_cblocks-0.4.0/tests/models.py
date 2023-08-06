from wagtail.admin.panels import FieldPanel
from wagtail.blocks import ChoiceBlock, StreamBlock
from wagtail.fields import StreamField
from wagtail.models import Page

from wagtail_cblocks.blocks import (
    ButtonBlock,
    ColumnsBlock,
    HeadingBlock,
    ImageBlock,
    ParagraphBlock,
    Style,
    StylizedStructBlock,
)

BUTTON_STYLES = [
    Style('primary', "Primary", 'btn-primary'),
    Style('secondary', "Secondary", 'btn-secondary'),
    Style('primary-lg', "Large primary", 'btn-primary btn-lg'),
]
BUTTON_DEFAULT_STYLE = 'primary-lg'


class BaseBlock(StreamBlock):
    title_block = HeadingBlock()
    paragraph_block = ParagraphBlock()
    button_block = ButtonBlock(
        styles=BUTTON_STYLES, default_style=BUTTON_DEFAULT_STYLE
    )
    image_block = ImageBlock()


class RowColumnsBlock(ColumnsBlock):
    LAYOUT_CHOICES = [
        ('2', "2-columns"),
        ('3', "3-columns"),
        ('4', "4-columns"),
        ('auto', "natural width"),
    ]

    layout = ChoiceBlock(choices=LAYOUT_CHOICES, default='auto')

    class Meta:
        label = "Row columns"
        template = 'tests/blocks/row_columns_block.html'
        column_block = BaseBlock()


class HeroBlock(StylizedStructBlock):
    blocks = BaseBlock(
        local_blocks=[('columns_block', ColumnsBlock(BaseBlock()))],
        label="Content",
    )

    styles = [
        Style('centered', "Centered", 'my-5 text-center hero-centered'),
        Style('responsive', "Responsive", 'container col-xxl-8'),
        Style('dark', "Dark", 'bg-dark text-white text-center'),
    ]

    class Meta:
        label = "Hero"
        template = 'tests/blocks/hero_block.html'


class BodyBlock(BaseBlock):
    hero_block = HeroBlock()
    columns_block = ColumnsBlock(BaseBlock())
    row_columns_block = RowColumnsBlock()


class StandardPage(Page):
    body = StreamField(BodyBlock(), use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]
