# wagtail-cblocks

A collection of StreamField blocks to use in Wagtail CMS.

**Warning!** This project is still early on in its development lifecycle. It is
possible for breaking changes to occur between versions until reaching a stable
1.0. Feedback and pull requests are welcome.

## Requirements

wagtail-cblocks requires the following:
- **Wagtail** (4.1 LTS, 4.2)
- **Django** (3.2, 4.0, 4.1)
- **Python 3** (3.7, 3.8, 3.9, 3.10)

## Installation

1. Install using ``pip``:
   ```shell
   $ pip install wagtail-cblocks
   ```
2. Add ``wagtail_cblocks`` to your ``INSTALLED_APPS`` setting:
   ```python
   INSTALLED_APPS = [
       # ...
       'wagtail_cblocks',
       # ...
   ]
   ```

## Usage

Each block comes with a template made for Bootstrap 5 which is not shipped by
this plugin. If you plan to use them as is, you must have at least the Bootstrap
stylesheet loaded in your base template - refer as needed to the
[Bootstrap documentation](https://getbootstrap.com/).

In waiting for the documentation, here is a sample usage:

```python
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.blocks import StreamBlock
from wagtail.fields import StreamField
from wagtail.models import Page

from wagtail_cblocks.blocks import (
    ButtonBlock,
    ColumnsBlock,
    HeadingBlock,
    ImageBlock,
    ParagraphBlock,
)


class BaseBlock(StreamBlock):
    title_block = HeadingBlock()
    paragraph_block = ParagraphBlock()
    button_block = ButtonBlock()
    image_block = ImageBlock()


class BodyBlock(BaseBlock):
    columns_block = ColumnsBlock(BaseBlock())


class StandardPage(Page):
    body = StreamField(BodyBlock())

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]
```

Factories are also provided for some of the blocks to ease tests - see
[`wagtail_cblocks/factories.py`](wagtail_cblocks/factories.py). To make use of
them, install the extra *factories* requirements:

```shell
$ pip install wagtail-cblocks[factories]
```

## Development
### Quick start

To set up a development environment, ensure that Python 3 is installed on your
system. Then:

1. Clone this repository
2. Create a virtual environment and activate it:
   ```shell
   $ python3 -m venv venv
   $ source venv/bin/activate
   ```
3. Install this package and its requirements:
   ```shell
   (venv)$ pip install -r requirements-dev.txt
   ```

Finally, if you want to run the test application to preview the blocks, you will
have to create the database before running a development server:
```shell
(venv)$ ./tests/manage.py migrate
(venv)$ ./tests/manage.py runserver
```

### Contributing

The tests are written with [pytest] and code coverage is measured with [coverage].
You can use the following commands while developing:
- ``make test``: run the tests and output a quick report of code coverage
- ``make test-wip``: only run the tests marked as 'wip'
- ``make test-all``: run the tests on all supported versions of Django and
  Wagtail with [nox]

The Python code is formatted and linted thanks to [flake8], [isort] and [black].
All of these tools are configured in [pre-commit] and you should consider to
install its git hook scripts by running:
```shell
(venv)$ pre-commit install
```

When submitting a pull-request, please ensure that the code is well formatted
and covered, and that all the tests pass.

[pytest]: https://docs.pytest.org/
[coverage]: https://coverage.readthedocs.io/
[nox]: https://nox.thea.codes/
[flake8]: https://flake8.pycqa.org/
[isort]: https://pycqa.github.io/isort/
[black]: https://black.readthedocs.io/
[pre-commit]: https://pre-commit.com/

## License

This extension is mainly developed by [Cliss XXI](https://www.cliss21.com) and
licensed under the [AGPLv3+](LICENSE). Any contribution is welcome!
